"""
Module for AI-related functionality.
"""

import asyncio
import logging
import uuid
from typing import Optional, Tuple, Dict, Any
import ujson as json # Using ujson instead of json for faster performance
import os # Added for OPENAI_API_KEY

from openai import AsyncOpenAI # We'll need this later
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall # For type hinting
from tortoise.exceptions import DoesNotExist

from ai_engine.db import PrincipalChatHistory, User # Assuming User model is needed for association

logger = logging.getLogger(__name__)

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define a sample tool that the AI can call
TOOLS_AVAILABLE = [
    {
        "type": "function",
        "function": {
            "name": "get_course_details",
            "description": "Get details about a specific course given its name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_name": {
                        "type": "string",
                        "description": "The name of the course, e.g. 'Introduction to Python Programming'",
                    },
                },
                "required": ["course_name"],
            },
        },
    }
]

# --- Simulated local functions that the AI can trigger ---
def _simulate_get_course_details(course_name: str) -> dict:
    """Simulates fetching course details."""
    logger.info(f"Simulating get_course_details for: {course_name}")
    # In a real application, this would query a database or another service
    if "python" in course_name.lower():
        return {"course_id": "PY101", "title": course_name, "description": "A comprehensive course on Python.", "credits": 3}
    elif "history" in course_name.lower():
        return {"course_id": "HIST202", "title": course_name, "description": "A survey of world history.", "credits": 4}
    else:
        return {"error": "Course not found", "title": course_name}

AVAILABLE_FUNCTIONS_MAP = {
    "get_course_details": _simulate_get_course_details,
}
# --- End of simulated functions ---


class Chat:
    """
    Manages a single chat session, including interaction with the database 
    (via PrincipalChatHistory), user input validation, and communication 
    with an AI model (e.g., OpenAI), including handling function calls.
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
        self._openai_client: Optional[AsyncOpenAI] = None # Will be initialized by _ensure_openai_client

        self._is_new_history = True # Flag to indicate if history_instance needs creation

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
        self.history_instance = PrincipalChatHistory(user=self.user, messages=[]) # Start with empty messages
        try:
            await self.history_instance.save()
            self.chat_history_id = self.history_instance.id # Store the new ID
            self._is_new_history = False # It's now saved
            logger.info(f"Created new chat history ID: {self.history_instance.id} for user ID: {self.user.id}")
        except Exception as e:
            logger.error(f"Failed to save new PrincipalChatHistory for user {self.user.id}: {e}")
            # In this case, history_instance remains unsaved, and subsequent operations might fail or retry.
            # Depending on desired behavior, could re-raise or handle.
            raise # Re-raise for now, as saving history is critical
        return self.history_instance

    def _ensure_openai_client(self) -> AsyncOpenAI:
        """Initializes and returns the OpenAI client, raising an error if no API key is found."""
        if not self._openai_client:
            if not self._openai_api_key:
                logger.error("OpenAI API key is not configured. Cannot make API calls.")
                raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY environment variable or pass it to Chat constructor.")
            self._openai_client = AsyncOpenAI(api_key=self._openai_api_key)
        return self._openai_client

    def _validate_user_input(self, user_message_content: str) -> Tuple[bool, str]:
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

    async def _prepare_initial_api_messages(self, db_messages: list) -> list:
        """
        Prepares the initial list of messages for the OpenAI API from DB history.
        Skips assistant messages that were tool call initiations to simplify context,
        as their corresponding tool responses are not stored in the DB.
        """
        api_messages = []
        for msg in db_messages:
            role = msg.get('role')
            content = msg.get('content')
            
            if role == 'user':
                api_messages.append({'role': 'user', 'content': content})
            elif role == 'assistant':
                # Only include assistant messages that have textual content and were not (primarily) tool calls.
                # This is a simplification: if a message had both text and calls, we only take text.
                if isinstance(content, dict) and content.get('text') and not content.get('calls'):
                    api_messages.append({'role': 'assistant', 'content': content.get('text')})
                elif isinstance(content, str): # Should ideally not happen for assistant with new model
                     api_messages.append({'role': 'assistant', 'content': content})
        return api_messages

    async def send_message(self, user_message_content: str, model_name: str = "gpt-4o-mini") -> Dict[str, Any]:
        """
        Processes a user's message, handles OpenAI API interaction including function calls,
        and saves messages to the database.
        """
        is_valid, validated_content = self._validate_user_input(user_message_content)
        if not is_valid:
            logger.warning(f"User input validation failed for user {self.user.id}: {validated_content}")
            return self._create_error_response(validated_content, "validation_error")

        try:
            history = await self._get_or_create_history_instance()
            client = self._ensure_openai_client()
        except ValueError as ve: # Handles API key not configured from _ensure_openai_client
            logger.error(f"Initialization error for user {self.user.id}: {ve}")
            return self._create_error_response(str(ve), "config_error")
        except Exception as e: # Handles DB errors from _get_or_create_history_instance
            logger.error(f"Failed to get/create chat history for user {self.user.id}: {e}")
            return self._create_error_response("Failed to initialize chat session.", "db_init_error")

        user_message_payload = PrincipalChatHistory.create_user_message_payload(content=validated_content)
        if not await history.insert_message(user_message_payload):
            logger.error(f"Failed to save user message for chat ID {history.id}")
            return self._create_error_response("Failed to save user message.", "db_error")

        messages_for_api = await self._prepare_initial_api_messages(history.messages)
        MAX_TOOL_CALL_ITERATIONS = 5
        
        for i in range(MAX_TOOL_CALL_ITERATIONS):
            logger.debug(f"OpenAI API call iteration {i+1}. Messages: {json.dumps(messages_for_api, indent=2)}")
            try:
                completion = await client.chat.completions.create(
                    model=model_name,
                    messages=messages_for_api,
                    tools=TOOLS_AVAILABLE,
                    tool_choice="auto", 
                )
                response_message = completion.choices[0].message
            except Exception as e:
                logger.error(f"OpenAI API call failed during iteration {i+1} for chat {history.id}: {e}")
                return self._create_error_response(f"AI service unavailable: {str(e)}", "api_error")

            ai_response_text = response_message.content
            tool_calls_from_api: Optional[list[ChatCompletionMessageToolCall]] = response_message.tool_calls
            
            db_calls_to_save = []
            if tool_calls_from_api:
                for tc in tool_calls_from_api:
                    db_calls_to_save.append({
                        "id": tc.id,
                        "type": tc.type,
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    })

            assistant_message_payload = PrincipalChatHistory.create_assistant_message_payload(
                text_content=ai_response_text or "", 
                calls_content=db_calls_to_save,
                request_message_id=user_message_payload["message_id"] 
            )

            if not await history.insert_message(assistant_message_payload):
                logger.error(f"Failed to save assistant message for chat ID {history.id}")
                return self._create_error_response("Failed to save assistant's response.", "db_error")
            
            api_assistant_msg_for_next_iteration = {'role': 'assistant', 'content': ai_response_text}
            if tool_calls_from_api:
                api_assistant_msg_for_next_iteration['tool_calls'] = [
                    {'id': tc.id, 'type': tc.type, 'function': {'name': tc.function.name, 'arguments': tc.function.arguments}}
                    for tc in tool_calls_from_api
                ]
                if not ai_response_text: 
                    api_assistant_msg_for_next_iteration['content'] = None
            
            messages_for_api.append(api_assistant_msg_for_next_iteration)

            if not tool_calls_from_api:
                logger.info(f"Assistant provided final text response for chat ID {history.id}.")
                return assistant_message_payload 

            logger.info(f"Assistant requested tool calls: {db_calls_to_save} for chat ID {history.id}")
            
            tool_response_messages_for_api = []
            for tool_call in tool_calls_from_api:
                function_name = tool_call.function.name
                function_args_str = tool_call.function.arguments
                tool_call_id = tool_call.id
                tool_content_str = ""

                try:
                    args = json.loads(function_args_str)
                    function_to_call = AVAILABLE_FUNCTIONS_MAP[function_name]
                    logger.info(f"Executing tool '{function_name}' with args: {args} (Call ID: {tool_call_id}) for chat {history.id}")
                    function_response_content = function_to_call(**args) # This is synchronous
                    tool_content_str = json.dumps(function_response_content)
                except json.JSONDecodeError as e:
                    logger.error(f"JSONDecodeError for tool {function_name} args '{function_args_str}' (Call ID: {tool_call_id}): {e}")
                    tool_content_str = json.dumps({"error": f"Invalid arguments format for {function_name}.", "details": str(e)})
                except KeyError:
                    logger.warning(f"Function {function_name} not found in AVAILABLE_FUNCTIONS_MAP (Call ID: {tool_call_id}) for chat {history.id}.")
                    tool_content_str = json.dumps({"error": f"Function {function_name} not available."})
                except Exception as e: # Catch errors from the function execution itself
                    logger.error(f"Error executing tool {function_name} (Call ID: {tool_call_id}) for chat {history.id}: {e}")
                    tool_content_str = json.dumps({"error": str(e), "details": "Function execution failed."})
                
                tool_response_messages_for_api.append({
                    "tool_call_id": tool_call_id,
                    "role": "tool",
                    "name": function_name, 
                    "content": tool_content_str
                })
            
            messages_for_api.extend(tool_response_messages_for_api)

        logger.error(f"Exceeded max tool call iterations ({MAX_TOOL_CALL_ITERATIONS}) for chat ID {history.id}.")
        return self._create_error_response("AI processing loop exceeded maximum iterations.", "loop_error")

    async def get_history_messages(self, limit: Optional[int] = None, offset: int = 0) -> list:
        """
        Retrieves messages from the current chat history.

        Args:
            limit: Maximum number of messages to return.
            offset: Number of messages to skip from the beginning of the history.

        Returns:
            A list of message dictionaries.
        """
        history = await self._get_or_create_history_instance() # Ensures history is loaded/created
        if not history.messages:
            return []
        
        if limit:
            return history.messages[offset : offset + limit]
        return history.messages[offset:]

# Example Usage (Illustrative - would typically be in a Sanic route or service layer)
async def example_chat_flow():
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY environment variable not set. Example cannot run OpenAI calls.")
        print("Set it and ensure your ai_engine.db models and database are initialized.")
        return

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger_ai_engine = logging.getLogger('ai_engine')
    logger_ai_engine.setLevel(logging.DEBUG) # More detailed logs from our chat module

    # --- Database Setup (minimal for example, replace with your app's setup) ---
    from tortoise import Tortoise
    try:
        await Tortoise.init(
            db_url='sqlite://:memory:', # Use in-memory SQLite for this example
            modules={'models': ['ai_engine.db', 'app.models']} # Ensure all models are found
        )
        await Tortoise.generate_schemas() # Create tables
        print("In-memory SQLite DB initialized and schemas generated.")

        # Create a dummy user for the chat
        try:
            user = await User.get_or_create(username="testuser_fn_caller", defaults={"email":"fn@example.com", "password_hash":" बदलना "})
            user = user[0] # get_or_create returns a tuple (object, created_bool)
            print(f"Using User ID: {user.id}")
        except Exception as e:
            print(f"Could not create/get dummy user: {e}")
            await Tortoise.close_connections()
            return
        
        # --- Scenario 1: Chat that might use a function call ---
        print("\n--- Starting Chat with Function Call Potential ---")
        chat_session = Chat(user=user) # API key from env
        
        # Message that should trigger the function call
        user_query1 = "Can you tell me about 'Introduction to Python Programming' course?"
        print(f"User: {user_query1}")
        response1 = await chat_session.send_message(user_query1)
        
        if response1.get("error"):
            print(f"AI Error: {response1['error']}")
        elif response1.get("content") and isinstance(response1["content"], dict):
            print(f"AI Response (Text): {response1['content'].get('text')}")
            if response1['content'].get('calls'):
                 print(f"AI Response (Calls Made by AI): {response1['content'].get('calls')}")
        else:
            print(f"AI Response: {response1}")

        # --- Scenario 2: Follow-up message ---
        print("\n--- Follow-up Message ---")
        user_query2 = "What about ancient history courses?"
        print(f"User: {user_query2}")
        response2 = await chat_session.send_message(user_query2)
        if response2.get("error"):
            print(f"AI Error: {response2['error']}")
        elif response2.get("content") and isinstance(response2["content"], dict):
             print(f"AI Response (Text): {response2['content'].get('text')}")
        else:
            print(f"AI Response: {response2}")


        # --- Scenario 3: Get all history for this chat session ---
        if chat_session.chat_history_id:
            print(f"\n--- Full History for Chat ID: {chat_session.chat_history_id} ---")
            all_msgs = await chat_session.get_history_messages()
            for i, msg_data in enumerate(all_msgs):
                role = msg_data.get('role')
                content = msg_data.get('content')
                print(f"  Msg {i+1} Role: {role}")
                if role == 'user':
                    print(f"    Content: {content}")
                elif role == 'assistant':
                    print(f"    Text: {content.get('text')}")
                    if content.get('calls'):
                        print(f"    Calls: {content.get('calls')}")
            print(f"Total messages in DB for this chat: {len(all_msgs)}")

    except ValueError as ve: # Catch API key error specifically
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An error occurred during the example chat flow: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if Tortoise._connections: # Check if connections were made
            await Tortoise.close_connections()
            print("DB connections closed.")

if __name__ == '__main__':
    print("Running ai.py example_chat_flow (requires OPENAI_API_KEY). Ensure DB models are compatible.")
    # This example now includes its own Tortoise init/close for standalone testing.
    asyncio.run(example_chat_flow())