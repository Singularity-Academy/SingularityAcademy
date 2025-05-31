"""
Test implementation of LLM with example tools and a command-line interface.

This module demonstrates the usage of LLM with two simple tools:
1. A calculator that can perform basic arithmetic
2. A weather simulator that generates random weather forecasts
"""

import asyncio
import random
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Annotated
from loguru import logger
from pydantic import BaseModel, Field
import json

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
    level="INFO",
    colorize=True
)

from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain.tools import StructuredTool
from langchain_core.callbacks import BaseCallbackHandler
from ai_engine.apps.ai.llm import LLM

# Tool argument models
class CalculatorArgs(BaseModel):
    expression: Annotated[str, Field(description="The mathematical expression to calculate")]

class WeatherForecastArgs(BaseModel):
    location: Annotated[str, Field(description="The city or location to get weather for")]
    days: Annotated[Optional[int], Field(
        default=1,
        description="Number of days to forecast (1-5)",
        ge=1,
        le=5
    )] = 1

# Example tools
def calculate(expression: str) -> str:
    """
    Calculate the result of a mathematical expression.
    Supports basic arithmetic operations: +, -, *, /, **
    
    Args:
        expression: A string containing a mathematical expression
        
    Returns:
        The result of the calculation as a string
        
    Example:
        calculate("2 + 2 * 3") -> "8"
    """
    logger.info(f"Calculator tool called with expression: {expression}")
    
    try:
        # Using eval is safe here as we're only allowing basic arithmetic
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            logger.warning(f"Invalid characters in expression: {expression}")
            return "Error: Expression contains invalid characters"
        
        # Log the evaluation attempt
        logger.debug(f"Evaluating expression: {expression}")
        result = eval(expression)
        
        # Log the successful calculation
        logger.info(f"Calculation successful: {expression} = {result}")
        return f"The result of {expression} is {result}"
        
    except Exception as e:
        # Log the error with full context
        logger.error(f"Calculation error for expression '{expression}': {str(e)}", exc_info=True)
        return f"Error calculating expression: {str(e)}"

def get_weather_forecast(location: str, days: Optional[int] = 1) -> str:
    """
    Generate a simulated weather forecast for a location.
    
    Args:
        location: The city or location to get weather for
        days: Number of days to forecast (1-5)
        
    Returns:
        A weather forecast as a string
    """
    logger.info(f"Weather forecast tool called for location: {location}, days: {days}")
    
    weather_types = ["sunny", "cloudy", "rainy", "stormy", "snowy"]
    temperatures = range(-10, 35)  # Celsius
    
    try:
        # Validate and adjust days
        days = min(max(1, days), 5)
        logger.debug(f"Adjusted forecast days to: {days}")
        
        # Generate forecast
        forecast = []
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            weather = random.choice(weather_types)
            temp = random.choice(temperatures)
            day_forecast = f"{date.strftime('%Y-%m-%d')}: {weather}, {temp}°C"
            forecast.append(day_forecast)
            logger.debug(f"Generated forecast for {date.strftime('%Y-%m-%d')}: {weather}, {temp}°C")
        
        # Log the complete forecast
        forecast_str = "\n".join(forecast)
        logger.info(f"Generated forecast for {location}:\n{forecast_str}")
        
        return f"Weather forecast for {location}:\n{forecast_str}"
        
    except Exception as e:
        # Log the error with full context
        logger.error(f"Weather forecast error for {location}: {str(e)}", exc_info=True)
        return f"Error generating forecast: {str(e)}"

class ChatInterface:
    """Simple command-line chat interface for testing LLM with tools."""
    
    def __init__(self):
        """Initialize the chat interface with tools."""
        logger.info("Initializing chat interface")
        self.llm = LLM()
        self.messages: List[BaseMessage] = []
        self._setup_tools()
        
    def _setup_tools(self):
        """Set up the available tools."""
        logger.info("Setting up tools")
        
        # Create calculator tool
        logger.debug("Creating calculator tool")
        calculator_tool = StructuredTool.from_function(
            func=calculate,
            name="calculate",
            description="""Calculate the result of a mathematical expression. 
            Supports basic arithmetic: +, -, *, /, **
            IMPORTANT: Always use this tool for any calculations, even simple ones.
            The expression must be in mathematical notation (e.g., "2 + 2", not "two plus two").
            Convert any word numbers to digits before using this tool.""",
            args_schema=CalculatorArgs
        )
        
        # Log the tool definition
        logger.info("Calculator tool definition:")
        logger.info(json.dumps({
            "name": calculator_tool.name,
            "description": calculator_tool.description,
            "args_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate"
                    }
                },
                "required": ["expression"]
            }
        }, indent=2))
        
        # Create weather forecast tool
        logger.debug("Creating weather forecast tool")
        weather_tool = StructuredTool.from_function(
            func=get_weather_forecast,
            name="get_weather_forecast",
            description="Get a simulated weather forecast for a location",
            args_schema=WeatherForecastArgs
        )
        
        # Log the weather tool definition
        logger.info("Weather tool definition:")
        logger.info(json.dumps({
            "name": weather_tool.name,
            "description": weather_tool.description,
            "args_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city or location to get weather for"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to forecast (1-5)",
                        "default": 1,
                        "minimum": 1,
                        "maximum": 5
                    }
                },
                "required": ["location"]
            }
        }, indent=2))
        
        # Add tools to LLM
        logger.debug("Adding tools to LLM")
        self.llm.add_tool(calculator_tool)
        self.llm.add_tool(weather_tool)
        
        # Set up initial system message
        logger.debug("Setting up initial system message")
        system_message = """You are a helpful AI assistant with access to a calculator and weather forecast tools.

IMPORTANT: You MUST use the calculator tool for ALL calculations. Never try to do calculations yourself.

When given a calculation:
1. First convert any word numbers to digits (e.g., "three million" -> "3000000")
2. Then IMMEDIATELY use the calculate tool with the mathematical expression
3. The tool MUST be called with the exact format: calculate(expression="3243976 * 67978")

For example, if asked "what is three million times two":
1. Convert to digits: "3000000 * 2"
2. Call the tool: calculate(expression="3000000 * 2")
3. Present the tool's result to the user

You can also help users with weather forecasts using the weather forecast tool.
If a user asks for something you can't help with, politely explain your limitations.

Remember: NEVER try to do calculations yourself. ALWAYS use the calculate tool."""
        
        logger.info("System message:")
        logger.info(system_message)
        
        self.messages.append(SystemMessage(content=system_message))
        logger.info("Tool setup complete")
    
    async def chat(self):
        """Run the chat interface."""
        logger.info("Starting chat interface")
        print("\nWelcome to the Tool-Enabled Chat Interface!")
        print("Type 'exit' or 'quit' to end the chat.")
        print("Try asking about calculations or weather forecasts!\n")
        
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            logger.debug(f"User input: {user_input}")
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                logger.info("User requested exit")
                print("\nGoodbye!")
                break
            
            # Add user message
            self.messages.append(HumanMessage(content=user_input))
            
            try:
                # Get AI response
                logger.debug("Requesting AI response")
                print("\nAI: ", end="", flush=True)
                
                # Create a callback to capture model decisions and tool usage
                class AgentCallback(BaseCallbackHandler):
                    def on_llm_start(self, serialized, prompts, **kwargs):
                        logger.info("Model starting with prompts:")
                        for i, prompt in enumerate(prompts):
                            logger.info(f"Prompt {i}:")
                            logger.info(prompt)
                    
                    def on_llm_new_token(self, token, **kwargs):
                        # Log tokens as they come in to see the model's thought process
                        logger.debug(f"Model token: {token}", end="")
                        print(token, end="", flush=True)
                    
                    def on_llm_end(self, response, **kwargs):
                        logger.info("Model finished generating")
                        if hasattr(response, 'llm_output'):
                            logger.info(f"Model output: {response.llm_output}")
                    
                    def on_tool_start(self, serialized, input_str, **kwargs):
                        logger.info(f"Tool started: {serialized['name']}")
                        logger.info(f"Tool input: {input_str}")
                        try:
                            # Try to parse and log the input as JSON
                            input_json = json.loads(input_str)
                            logger.info("Tool input (parsed):")
                            logger.info(json.dumps(input_json, indent=2))
                        except:
                            logger.info(f"Tool input (raw): {input_str}")
                    
                    def on_tool_end(self, output, **kwargs):
                        logger.info(f"Tool ended with output: {output}")
                    
                    def on_tool_error(self, error, **kwargs):
                        logger.error(f"Tool error: {error}")
                
                # Generate response with tools enabled
                response = await self.llm.agenerate_response(
                    self.messages,
                    callbacks=[AgentCallback()],
                    use_tools=True
                )
                
                # Add AI response to history
                self.messages.append(AIMessage(content=response))
                
            except Exception as e:
                logger.error(f"Error in chat: {str(e)}", exc_info=True)
                print(f"\nError: {str(e)}")
                print("Please try again.")

async def main():
    """Run the chat interface."""
    logger.info("Starting application")
    chat = ChatInterface()
    await chat.chat()
    logger.info("Application finished")

if __name__ == "__main__":
    # Run the chat interface
    asyncio.run(main()) 