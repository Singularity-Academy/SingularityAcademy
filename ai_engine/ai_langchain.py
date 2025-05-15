"""
Module for AI-related functionality using LangChain.
This module implements the same functionality as ai.py but using LangChain abstractions.
"""

import asyncio
import logging
import os
import uuid
from typing import Optional, Dict, Any, List, AsyncGenerator
from datetime import datetime, timezone

import ujson as json

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.utils import ConfigurableFieldSpec

from tortoise.exceptions import DoesNotExist

from ai_engine.db import PrincipalChatHistory, User

logger = logging.getLogger(__name__)

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define tools that the AI can call
@tool
def get_course_details(course_name: str) -> Dict:
    """
    Get details about a specific course given its name.
    
    Args:
        course_name: The name of the course, e.g. 'Introduction to Python Programming'
        
    Returns:
        A dictionary containing course details
    """
    logger.info(f"get_course_details called for: {course_name}")
    # In a real application, this would query a database or another service
    if "python" in course_name.lower():
        return {"course_id": "PY101", "title": course_name, "description": "A comprehensive course on Python.", "credits": 3}
    elif "history" in course_name.lower():
        return {"course_id": "HIST202", "title": course_name, "description": "A survey of world history.", "credits": 4}
    else:
        return {"error": "Course not found", "title": course_name}


class StreamingCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming LLM responses."""
    
    def __init__(self, message_id: str):
        self.message_id = message_id
        self.chunks = []
        
    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.chunks.append(token)
        # In a real implementation, you would yield this token to a websocket
        
    def get_full_response(self) -> str:
        """Get the full response from collected chunks."""
        return "".join(self.chunks)


class Chat:
    """
    LangChain implementation of chat functionality.
    Manages a single chat session, including interaction with the database 
    (via PrincipalChatHistory), user input validation, and communication 
    with an AI model using LangChain.
    """

    def __init__(self, user: User, chat_history_id: Optional[int] = None, openai_api_key: Optional[str] = None):
        """
        Initializes a Chat instance.

        If chat_history_id is provided, it attempts to load an existing chat history.
        Otherwise, a new PrincipalChatHistory record is prepared (but not saved until the first message).

        Args:
            user: The User object associated with this chat.
            chat_history_id: Optional ID of an existing PrincipalChatHistory record to load.
            openai_api_key: Optional OpenAI API key. If not provided, it attempts to load
                            from the OPENAI_API_KEY environment variable.
        """
        self.user = user
        self.chat_history_id: Optional[int] = chat_history_id
        self.history_instance: Optional[PrincipalChatHistory] = None
        
        self._openai_api_key = openai_api_key or OPENAI_API_KEY
        self._is_new_history = True  # Flag to indicate if history_instance needs creation
        
        # Load the system prompt from prompt.txt
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompt.txt')
        try:
            with open(prompt_path, 'r') as f:
                self.system_prompt = f.read().strip()
            logger.info("Loaded system prompt from prompt.txt")
        except Exception as e:
            logger.warning(f"Failed to load system prompt from {prompt_path}: {e}")
            self.system_prompt = "You are an assistant that helps with educational queries."
            
        # Initialize LangChain components
        self._init_langchain()
    
    def _init_langchain(self):
        """Initialize LangChain components."""
        if not self._openai_api_key:
            logger.error("OpenAI API key is not configured. Cannot make API calls.")
            raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY environment variable or pass it to Chat constructor.")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            api_key=self._openai_api_key,
            temperature=0.7,
            model="gpt-4o-mini",
            streaming=False
        )
        
        # Initialize streaming LLM
        self.streaming_llm = ChatOpenAI(
            api_key=self._openai_api_key,
            temperature=0.7,
            model="gpt-4o-mini",
            streaming=True
        )
        
        # Initialize tools
        self.tools = [get_course_details]

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

    async def send_message(self, user_message_content: str, model_name: str = "gpt-4o-mini") -> Dict[str, Any]:
        """
        Processes a user's message using LangChain, handles tool calls,
        and saves messages to the database.
        """
        is_valid, validated_content = self._validate_user_input(user_message_content)
        if not is_valid:
            logger.warning(f"User input validation failed for user {self.user.id}: {validated_content}")
            return self._create_error_response(validated_content, "validation_error")

        try:
            history = await self._get_or_create_history_instance()
            
            # Update LLM model if different from default
            if model_name != "gpt-4o-mini":
                self.llm.model_name = model_name
                self.streaming_llm.model_name = model_name
                
        except Exception as e:
            logger.error(f"Failed to initialize chat for user {self.user.id}: {e}")
            return self._create_error_response(str(e), "init_error")

        # Save user message to database
        user_message_payload = PrincipalChatHistory.create_user_message_payload(content=validated_content)
        if not await history.insert_message(user_message_payload):
            logger.error(f"Failed to save user message for chat ID {history.id}")
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

    async def stream_message(self, user_message_content: str, model_name: str = "gpt-4o-mini") -> AsyncGenerator[Dict[str, Any], None]:
        """
        Processes a user's message and streams the response using LangChain.
        
        Args:
            user_message_content: The message from the user
            model_name: The name of the model to use
            
        Yields:
            Chunks of the assistant's response
        """
        is_valid, validated_content = self._validate_user_input(user_message_content)
        if not is_valid:
            logger.warning(f"User input validation failed for user {self.user.id}: {validated_content}")
            yield self._create_error_response(validated_content, "validation_error")
            return

        try:
            history = await self._get_or_create_history_instance()
            
            # Update LLM model if different from default
            if model_name != "gpt-4o-mini":
                self.streaming_llm.model_name = model_name
                
        except Exception as e:
            logger.error(f"Failed to initialize chat for user {self.user.id}: {e}")
            yield self._create_error_response(str(e), "init_error")
            return

        # Save user message to database
        user_message_payload = PrincipalChatHistory.create_user_message_payload(content=validated_content)
        if not await history.insert_message(user_message_payload):
            logger.error(f"Failed to save user message for chat ID {history.id}")
            yield self._create_error_response("Failed to save user message.", "db_error")
            return

        try:
            # Convert database messages to LangChain format
            langchain_messages = await self._convert_db_messages_to_langchain(history.messages)
            
            # Create a message ID for the assistant response
            assistant_message_id = f"prinmsg-{uuid.uuid4()}"
            
            # Create callback handler for streaming
            stream_handler = StreamingCallbackHandler(message_id=assistant_message_id)
            
            # Create an empty placeholder message in the database
            assistant_message_payload = PrincipalChatHistory.create_assistant_message_payload(
                text_content="",
                calls_content=[],
                request_message_id=user_message_payload["message_id"],
                message_id=assistant_message_id
            )
            await history.insert_message(assistant_message_payload)
            
            # Set up the streaming chain
            streaming_chain = self.streaming_llm.bind(tools=self.tools)
            
            # Start streaming
            async for chunk in streaming_chain.astream(
                langchain_messages,
                config={"callbacks": [stream_handler]}
            ):
                if hasattr(chunk, 'content') and chunk.content:
                    yield {
                        "type": "text",
                        "content": chunk.content,
                        "message_id": assistant_message_id
                    }
            
            # Get the full response from the handler
            full_response = stream_handler.get_full_response()
            
            # Update the message in the database with the complete text
            await history.update_message_content(
                message_id=assistant_message_id,
                new_content={"text": full_response, "courses": []}
            )
            
            # Signal completion
            yield {"type": "done", "message_id": assistant_message_id}
            
        except Exception as e:
            logger.error(f"Error in LangChain streaming for chat ID {history.id}: {e}")
            yield self._create_error_response(f"AI streaming error: {str(e)}", "langchain_stream_error")

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
        print("OPENAI_API_KEY environment variable not set. Example cannot run.")
        return

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger_ai_engine = logging.getLogger('ai_engine')
    logger_ai_engine.setLevel(logging.DEBUG)  # More detailed logs from our chat module

    # --- Database Setup (minimal for example) ---
    from tortoise import Tortoise
    try:
        await Tortoise.init(
            db_url='sqlite://:memory:',  # Use in-memory SQLite for this example
            modules={'models': ['ai_engine.db']}  # Ensure all models are found
        )
        await Tortoise.generate_schemas()  # Create tables
        print("In-memory SQLite DB initialized and schemas generated.")

        # Create a dummy user for the chat
        try:
            user = await User.get_or_create(username="testuser_langchain", defaults={"email":"langchain@example.com", "password_hash":"placeholder"})
            user = user[0]  # get_or_create returns a tuple (object, created_bool)
            print(f"Using User ID: {user.id}")
        except Exception as e:
            print(f"Could not create/get dummy user: {e}")
            await Tortoise.close_connections()
            return
        
        # Create a chat session
        print("\n--- Starting LangChain Chat ---")
        chat_session = Chat(user=user)  # API key from env
        
        # Send a message
        user_query = "Can you tell me about 'Introduction to Python Programming' course?"
        print(f"User: {user_query}")
        response = await chat_session.send_message(user_query)
        
        if response.get("error"):
            print(f"AI Error: {response['error']}")
        elif response.get("content") and isinstance(response["content"], dict):
            print(f"AI Response (Text): {response['content'].get('text')}")
            if response['content'].get('calls'):
                print(f"AI Response (Calls Made by AI): {response['content'].get('calls')}")
        else:
            print(f"AI Response: {response}")

        # Test streaming (in a real application, this would stream to a websocket)
        print("\n--- Testing Streaming Response ---")
        user_query2 = "What about history courses for beginners?"
        print(f"User: {user_query2}")
        print("AI (streaming): ", end="", flush=True)
        async for chunk in chat_session.stream_message(user_query2):
            if chunk.get("type") == "text" and chunk.get("content"):
                print(chunk["content"], end="", flush=True)
            elif chunk.get("type") == "done":
                print("\n[Stream completed]")
            elif chunk.get("error"):
                print(f"\nError: {chunk['error']}")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if Tortoise._connections:  # Check if connections were made
            await Tortoise.close_connections()
            print("DB connections closed.")

if __name__ == '__main__':
    print("Running LangChain example chat flow (requires OPENAI_API_KEY).")
    asyncio.run(example_langchain_chat_flow()) 