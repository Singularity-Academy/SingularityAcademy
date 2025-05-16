"""
Module for AI-related functionality using LangChain.
This module implements chat functionality using LangChain abstractions.
"""

import asyncio
import os
import uuid
from typing import Optional, Dict, Any, List, AsyncGenerator, Set
from datetime import datetime, timezone

import ujson as json
from loguru import logger
from sanic import Websocket

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.runnables import RunnableConfig

from tortoise.exceptions import DoesNotExist

from .db import PrincipalChatHistory, User, Course
from .model_config import ModelConfig, model_manager, get_model_config
from .streaming import stream_with_buffer, StreamChunk

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define tools that the AI can call
@tool
async def get_course_details(course_name: str) -> Dict:
    """
    Get details about a specific course from the database.
    
    Args:
        course_name: The name of the course to search for
        
    Returns:
        A dictionary containing course details or an error message
    """
    logger.info(f"Fetching course details for: {course_name}")
    try:
        # Query the database for the course
        course = await Course.filter(name__icontains=course_name).first()
        
        if course:
            return {
                "course_id": course.id,
                "title": course.name,
                "description": course.desc,
                "created_at": course.created_at.isoformat(),
                "owner_id": course.owner_id
            }
        return {"error": "Course not found", "title": course_name}
    except Exception as e:
        logger.error(f"Error fetching course details: {e}")
        return {"error": "Failed to fetch course details", "title": course_name}

# Add new tools for course management
@tool
async def create_course(name: str, description: str = None) -> Dict:
    """
    Create a new course in the database.
    
    Args:
        name: The name of the course
        description: Optional description of the course
        
    Returns:
        A dictionary containing the created course details or an error message
    """
    logger.info(f"Creating new course: {name}")
    try:
        # Create the course
        course = await Course.create(
            name=name,
            desc=description
        )
        
        return {
            "course_id": course.id,
            "title": course.name,
            "description": course.desc,
            "created_at": course.created_at.isoformat(),
            "owner_id": course.owner_id
        }
    except Exception as e:
        logger.error(f"Error creating course: {e}")
        return {"error": "Failed to create course", "title": name}

@tool
async def list_courses() -> Dict:
    """
    List all available courses from the database.
    
    Returns:
        A dictionary containing a list of courses or an error message
    """
    logger.info("Listing all courses")
    try:
        courses = await Course.all()
        return {
            "courses": [
                {
                    "course_id": course.id,
                    "title": course.name,
                    "description": course.desc,
                    "created_at": course.created_at.isoformat(),
                    "owner_id": course.owner_id
                }
                for course in courses
            ],
            "count": len(courses)
        }
    except Exception as e:
        logger.error(f"Error listing courses: {e}")
        return {"error": "Failed to list courses"}

class StreamingCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming LLM responses."""
    
    def __init__(self, websocket: Optional[Websocket] = None):
        self.websocket = websocket
        self.active_websockets: Set[Websocket] = set()
        if websocket:
            self.active_websockets.add(websocket)
        logger.debug("Initialized StreamingCallbackHandler")
    
    def add_websocket(self, websocket: Websocket) -> None:
        """Add a websocket to receive stream updates."""
        self.active_websockets.add(websocket)
        logger.debug("Added websocket to handler")
    
    def remove_websocket(self, websocket: Websocket) -> None:
        """Remove a websocket from stream updates."""
        self.active_websockets.discard(websocket)
        logger.debug("Removed websocket from handler")
    
    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run on new LLM token."""
        # This is now just a pass-through as streaming is handled by stream_with_buffer
        pass

class Chat:
    """
    LangChain implementation of chat functionality.
    Manages a single chat session, including interaction with the database 
    (via PrincipalChatHistory), user input validation, and communication 
    with an AI model using LangChain.
    """

    def __init__(self, user: User, chat_history_id: Optional[int] = None, model_id: Optional[str] = None):
        """
        Initializes a Chat instance.

        Args:
            user: The User object associated with this chat.
            chat_history_id: Optional ID of an existing PrincipalChatHistory record to load.
            model_id: Optional model ID to use. If not provided, uses the default model.
        """
        self.user = user
        self.chat_history_id: Optional[int] = chat_history_id
        self.history_instance: Optional[PrincipalChatHistory] = None
        self._is_new_history = True
        
        # Get model configuration
        self.model_config = get_model_config(model_id) if model_id else model_manager.get_default_model()
        if not self.model_config:
            raise ValueError(f"Model {model_id} not found in configuration")
        
        # Load the system prompt from prompt.txt (using cached version)
        self.system_prompt = model_manager.get_static_file(
            os.path.join(os.path.dirname(__file__), 'prompt.txt')
        ).strip()
        if not self.system_prompt:
            logger.warning("Failed to load system prompt, using default")
            self.system_prompt = "You are an assistant that helps with educational queries."
            
        # Initialize LangChain components
        self._init_langchain()
    
    def _init_langchain(self):
        """Initialize LangChain components."""
        if not self.model_config.api_key and not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OpenAI API key not configured")
        
        # Initialize LLM with model configuration
        self.llm = ChatOpenAI(
            api_key=self.model_config.api_key or os.getenv("OPENAI_API_KEY"),
            temperature=self.model_config.temperature,
            model=self.model_config.model_id,
            max_tokens=self.model_config.max_tokens,
            streaming=False,
            timeout=self.model_config.timeout
        )
        
        # Initialize streaming LLM
        self.streaming_llm = ChatOpenAI(
            api_key=self.model_config.api_key or os.getenv("OPENAI_API_KEY"),
            temperature=self.model_config.temperature,
            model=self.model_config.model_id,
            max_tokens=self.model_config.max_tokens,
            streaming=True,
            timeout=self.model_config.timeout
        )
        
        # Initialize tools - always include course tools
        self.tools = [
            get_course_details,
            list_courses
        ]
    
    def update_model(self, model_id: str) -> bool:
        """
        Update the model being used by this chat instance.
        
        Args:
            model_id: ID of the model to use
            
        Returns:
            True if successful, False if model not available
        """
        new_config = get_model_config(model_id)
        if not new_config:
            logger.warning(f"Model {model_id} not found in configuration")
            return False
            
        self.model_config = new_config
        
        # Update LLM instances with new configuration
        self.llm.model_name = new_config.model_id
        self.llm.temperature = new_config.temperature
        self.llm.max_tokens = new_config.max_tokens
        self.llm.timeout = new_config.timeout
        
        self.streaming_llm.model_name = new_config.model_id
        self.streaming_llm.temperature = new_config.temperature
        self.streaming_llm.max_tokens = new_config.max_tokens
        self.streaming_llm.timeout = new_config.timeout
        
        logger.info(f"Updated chat model to {new_config.name}")
        return True

    async def _get_or_create_history_instance(self) -> PrincipalChatHistory:
        """
        Retrieves the existing PrincipalChatHistory instance or creates a new one
        if it hasn't been loaded/created yet. Saves the new instance to the DB.
        """
        if self.history_instance:
            return self.history_instance

        if self.chat_history_id:
            try:
                self.history_instance = await PrincipalChatHistory.get(id=self.chat_history_id, user=self.user)
                self._is_new_history = False
                logger.info(f"Loaded existing chat history ID: {self.chat_history_id} for user ID: {self.user.id}")
                return self.history_instance
            except DoesNotExist:
                logger.warning(f"Chat history ID {self.chat_history_id} not found for user ID: {self.user.id}. Creating a new one.")
                # Fall through to create a new one
        
        # Create a new history instance
        self.history_instance = PrincipalChatHistory(user=self.user, messages=[])  # Start with empty messages
        try:
            await self.history_instance.save()
            self.chat_history_id = self.history_instance.id  # Store the new ID
            self._is_new_history = False  # It's now saved
            
            # Add the system prompt as the first message for new chats
            system_message = {
                "message_id": f"system-{uuid.uuid4()}",
                "role": "system",
                "content": self.system_prompt,
                "timestamp": datetime.now(timezone.utc).isoformat(timespec='seconds') + "Z"
            }
            await self.history_instance.insert_message(system_message)
            logger.info(f"Created new chat history ID: {self.history_instance.id} with system prompt for user ID: {self.user.id}")
            
        except Exception as e:
            logger.error(f"Failed to save new PrincipalChatHistory for user {self.user.id}: {e}")
            raise  # Re-raise for now, as saving history is critical
        return self.history_instance

    def _validate_user_input(self, user_message_content: str) -> tuple[bool, str]:
        """
        Validates the user's message content.

        Args:
            user_message_content: The raw text input from the user.

        Returns:
            A tuple (is_valid, error_message_or_sanitized_content).
            If valid, error_message is the sanitized content (e.g. stripped).
            If invalid, error_message contains a description of the error.
        """
        if not isinstance(user_message_content, str):
            return False, "Input must be a string."
        
        stripped_content = user_message_content.strip()
        if not stripped_content:
            return False, "Message content cannot be empty or just whitespace."
        
        # Add any other validation rules here (e.g., length limits)
        # For now, basic non-empty check is sufficient.
        
        return True, stripped_content

    def _create_error_response(self, message: str, error_type: str, role: str = "system") -> Dict[str, Any]:
        """Creates a standardized error response dictionary."""
        return {"error": message, "role": role, "type": error_type}

    async def _convert_db_messages_to_langchain(self, db_messages: List[Dict]) -> List[Any]:
        """
        Convert database messages to LangChain message types.
        
        Args:
            db_messages: List of message dictionaries from the database
            
        Returns:
            List of LangChain message objects
        """
        langchain_messages = []
        
        for msg in db_messages:
            role = msg.get('role')
            content = msg.get('content')
            
            if role == 'system':
                langchain_messages.append(SystemMessage(content=content))
            elif role == 'user':
                langchain_messages.append(HumanMessage(content=content))
            elif role == 'assistant':
                # For assistant messages with a dictionary content
                if isinstance(content, dict):
                    # Extract text content
                    text_content = content.get('text', '')
                    langchain_messages.append(AIMessage(content=text_content))
                # For legacy assistant messages with string content
                elif isinstance(content, str):
                    langchain_messages.append(AIMessage(content=content))
            # Tool messages would be handled here if needed
            
        logger.debug(f"Converted {len(langchain_messages)} messages for LangChain")
        return langchain_messages

    async def send_message(self, user_message_content: str, model_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes a user's message using LangChain, handles tool calls,
        and saves messages to the database.
        
        Args:
            user_message_content: The message from the user
            model_id: Optional model ID to use for this message only. 
                        If provided, temporarily switches to this model.
        """
        is_valid, validated_content = self._validate_user_input(user_message_content)
        if not is_valid:
            logger.warning(f"User input validation failed for user {self.user.id}: {validated_content}")
            return self._create_error_response(validated_content, "validation_error")

        # Handle optional model switching
        original_model = self.model_config.model_id
        if model_id and model_id != original_model:
            if not self.update_model(model_id):
                logger.warning(f"Failed to switch to model {model_id}, using {original_model}")

        try:
            history = await self._get_or_create_history_instance()
                
        except Exception as e:
            logger.error(f"Failed to initialize chat for user {self.user.id}: {e}")
            
            # Restore original model if we switched
            if model_id and original_model != self.model_config.model_id:
                self.update_model(original_model)
                
            return self._create_error_response(str(e), "init_error")

        # Save user message to database
        user_message_payload = PrincipalChatHistory.create_user_message_payload(content=validated_content)
        if not await history.insert_message(user_message_payload):
            logger.error(f"Failed to save user message for chat ID {history.id}")
            
            # Restore original model if we switched
            if model_id and original_model != self.model_config.model_id:
                self.update_model(original_model)
                
            return self._create_error_response("Failed to save user message.", "db_error")

        try:
            # Convert database messages to LangChain format
            langchain_messages = await self._convert_db_messages_to_langchain(history.messages)
            
            # Create a message ID for the assistant response
            assistant_message_id = f"prinmsg-{uuid.uuid4()}"
            
            # Set up the chain with tools
            chain = self.llm.bind(tools=self.tools)
            
            # Run the chain
            response = await chain.ainvoke(
                langchain_messages,
                config={"tool_choice": "auto"}
            )
            
            ai_response_text = response.content
            tool_calls = getattr(response, "tool_calls", None)
            
            # Process tool calls if present
            db_calls_to_save = []
            if tool_calls:
                for tc in tool_calls:
                    # Extract tool call details
                    tool_name = tc.name
                    tool_args = tc.args
                    
                    # Call the tool
                    tool_function = next((t for t in self.tools if t.name == tool_name), None)
                    if tool_function:
                        tool_result = await tool_function.ainvoke(tool_args)
                        # Add tool result as a message
                        langchain_messages.append(ToolMessage(content=str(tool_result), name=tool_name))
                    
                    # Save call details for database
                    db_calls_to_save.append({
                        "id": str(uuid.uuid4()),
                        "type": "function",
                        "function": {"name": tool_name, "arguments": json.dumps(tool_args)}
                    })
                
                # Get final response after tool calls
                if db_calls_to_save:
                    final_response = await chain.ainvoke(langchain_messages)
                    ai_response_text = final_response.content
            
            # Save assistant message to database
            assistant_message_payload = PrincipalChatHistory.create_assistant_message_payload(
                text_content=ai_response_text or "",
                calls_content=db_calls_to_save,
                request_message_id=user_message_payload["message_id"],
                message_id=assistant_message_id
            )
            
            if not await history.insert_message(assistant_message_payload):
                logger.error(f"Failed to save assistant message for chat ID {history.id}")
                return self._create_error_response("Failed to save assistant's response.", "db_error")
            
            return assistant_message_payload
            
        except Exception as e:
            logger.error(f"Error in LangChain processing for chat ID {history.id}: {e}")
            return self._create_error_response(f"AI service error: {str(e)}", "langchain_error")
        finally:
            # Restore original model if we switched
            if model_id and original_model != self.model_config.model_id:
                self.update_model(original_model)

    async def stream_message(
        self, 
        user_message_content: str, 
        model_id: Optional[str] = None,
        websocket: Optional[Websocket] = None
    ) -> AsyncGenerator[StreamChunk, None]:
        """
        Processes a user's message and streams the response using LangChain.
        
        Args:
            user_message_content: The message from the user
            model_id: Optional model ID to use for this message only.
                     If provided, temporarily switches to this model.
            websocket: Optional WebSocket connection to stream responses to.
            
        Yields:
            StreamChunk objects containing the assistant's response
        """
        is_valid, validated_content = self._validate_user_input(user_message_content)
        if not is_valid:
            logger.warning(f"User input validation failed for user {self.user.id}: {validated_content}")
            yield StreamChunk(
                content="",
                message_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                is_final=True,
                error=validated_content
            )
            return

        # Handle optional model switching
        original_model = self.model_config.model_id
        if model_id and model_id != original_model:
            if not self.update_model(model_id):
                logger.warning(f"Failed to switch to model {model_id}, using {original_model}")

        try:
            history = await self._get_or_create_history_instance()
                
        except Exception as e:
            logger.error(f"Failed to initialize chat for user {self.user.id}: {e}")
            
            # Restore original model if we switched
            if model_id and original_model != self.model_config.model_id:
                self.update_model(original_model)
                
            yield StreamChunk(
                content="",
                message_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                is_final=True,
                error=str(e)
            )
            return

        # Save user message to database
        user_message_payload = PrincipalChatHistory.create_user_message_payload(content=validated_content)
        if not await history.insert_message(user_message_payload):
            logger.error(f"Failed to save user message for chat ID {history.id}")
            
            # Restore original model if we switched
            if model_id and original_model != self.model_config.model_id:
                self.update_model(original_model)
                
            yield StreamChunk(
                content="",
                message_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                is_final=True,
                error="Failed to save user message"
            )
            return

        try:
            # Convert database messages to LangChain format
            langchain_messages = await self._convert_db_messages_to_langchain(history.messages)
            
            # Create a message ID for tracking
            message_id = str(uuid.uuid4())
            
            # Create callback handler for streaming
            stream_handler = StreamingCallbackHandler(websocket)
            
            # Create an empty placeholder message in the database
            assistant_message_payload = PrincipalChatHistory.create_assistant_message_payload(
                text_content="",
                calls_content=[],
                request_message_id=user_message_payload["message_id"],
                message_id=message_id
            )
            await history.insert_message(assistant_message_payload)
            
            # Set up the streaming chain
            streaming_chain = self.streaming_llm.bind(tools=self.tools)
            
            # Process the stream with buffering
            async for chunk in stream_with_buffer(
                streaming_chain.astream(
                    langchain_messages,
                    config={"callbacks": [stream_handler]}
                ),
                message_id=message_id,
                buffer_size=self.model_config.cache_size,
                websocket=websocket
            ):
                # Update the message in the database if this is the final chunk
                if chunk.is_final and not chunk.error:
                    await history.update_message_content(
                        message_id=message_id,
                        new_content={"text": chunk.content, "courses": []}
                    )
                yield chunk
            
        except Exception as e:
            logger.error(f"Error in LangChain streaming for chat ID {history.id}: {e}")
            yield StreamChunk(
                content="",
                message_id=message_id,
                timestamp=datetime.now(),
                is_final=True,
                error=f"AI streaming error: {str(e)}"
            )
        finally:
            # Restore original model if we switched
            if model_id and original_model != self.model_config.model_id:
                self.update_model(original_model)

    async def get_history_messages(self, limit: Optional[int] = None, offset: int = 0) -> list:
        """
        Retrieves messages from the current chat history.

        Args:
            limit: Maximum number of messages to return.
            offset: Number of messages to skip from the beginning of the history.

        Returns:
            A list of message dictionaries.
        """
        history = await self._get_or_create_history_instance()  # Ensures history is loaded/created
        if not history.messages:
            return []
        
        if limit:
            return history.messages[offset: offset + limit]
        return history.messages[offset:]


# Example usage
async def example_langchain_chat_flow():
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY environment variable not set. Example cannot run.")
        return

    # --- Database Setup (minimal for example) ---
    from tortoise import Tortoise
    try:
        await Tortoise.init(
            db_url='sqlite://:memory:',  # Use in-memory SQLite for this example
            modules={'models': ['ai_engine.db']}  # Ensure all models are found
        )
        await Tortoise.generate_schemas()  # Create tables
        logger.info("In-memory SQLite DB initialized and schemas generated.")

        # Create a dummy user for the chat
        try:
            user = await User.get_or_create(username="testuser_langchain", defaults={"email":"langchain@example.com", "password_hash":"placeholder"})
            user = user[0]  # get_or_create returns a tuple (object, created_bool)
            logger.info(f"Using User ID: {user.id}")
        except Exception as e:
            logger.error(f"Could not create/get dummy user: {e}")
            await Tortoise.close_connections()
            return
        
        # Create a chat session with default model
        logger.info("Starting LangChain Chat")
        chat_session = Chat(user=user)  # API key from env
        logger.info(f"Using model: {chat_session.model_config.name}")
        
        # List available models
        logger.info("Available models:")
        for model_id, model_info in get_model_config().items():
            logger.info(f"  - {model_id}: {model_info['name']} - {model_info['description']}")
        
        # Send a message with default model
        user_query = "Can you tell me about 'Introduction to Python Programming' course?"
        logger.info(f"User: {user_query}")
        response = await chat_session.send_message(user_query)
        
        if response.get("error"):
            logger.error(f"AI Error: {response['error']}")
        elif response.get("content") and isinstance(response["content"], dict):
            logger.info(f"AI Response (Text): {response['content'].get('text')}")
            if response['content'].get('calls'):
                logger.info(f"AI Response (Calls Made by AI): {response['content'].get('calls')}")
        else:
            logger.info(f"AI Response: {response}")

        # Test streaming with a different model
        logger.info("Testing Streaming Response with Different Model")
        user_query2 = "What about history courses for beginners?"
        logger.info(f"User: {user_query2}")
        logger.info("Switching to gpt-3.5-turbo for this message...")
        logger.info("AI (streaming): ", end="", flush=True)
        
        async for chunk in chat_session.stream_message(user_query2, model_id="gpt-3.5-turbo"):
            if chunk.get("type") == "text" and chunk.get("content"):
                logger.info(chunk["content"], end="", flush=True)
            elif chunk.get("type") == "done":
                logger.info("\n[Stream completed]")
            elif chunk.get("error"):
                logger.error(f"\nError: {chunk['error']}")
                
        logger.info(f"Current model after streaming: {chat_session.model_config.name}")  # Should be back to default

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        logger.exception("Full traceback:")
    finally:
        if Tortoise._connections:  # Check if connections were made
            await Tortoise.close_connections()
            logger.info("DB connections closed.")

if __name__ == '__main__':
    logger.info("Running LangChain example chat flow (requires OPENAI_API_KEY).")
    asyncio.run(example_langchain_chat_flow()) 