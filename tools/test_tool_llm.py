"""
Interactive test tool for the LLM class.

This module provides a command-line interface for testing the LLM class directly,
with support for:
- Interactive chat with the LLM
- Tool registration and testing
- Streaming responses
- Default configuration loading
"""

import asyncio
import sys
import argparse
import math
import random
import re
from typing import List, Optional, Any, Dict, Union, ClassVar
from datetime import datetime, timedelta
from pathlib import Path

from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.tools import BaseTool
from langchain.callbacks.base import BaseCallbackHandler
from pydantic import Field, BaseModel
from loguru import logger

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from ai_engine.apps.ai.llm import LLM
from ai_engine.config import load_llm_config

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test tool for LLM class")
    parser.add_argument(
        "--llm",
        choices=["gpt-4", "deepseek-v3"],
        default="gpt-4",
        help="LLM model to use (default: gpt-4)"
    )
    return parser.parse_args()

# Math Tools
class CalculatorTool(BaseTool):
    """Tool that performs basic mathematical calculations."""
    name: str = Field(default="calculator", description="Name of the tool")
    description: str = Field(
        default="""Perform mathematical calculations. 
        Input should be a string containing a mathematical expression.
        Supports basic operations (+, -, *, /, **, sqrt) and common math functions.
        Example: "2 + 2" or "sqrt(16)" or "sin(pi/2)" """,
        description="Tool description"
    )
    
    def _run(self, expression: str) -> str:
        """Run the tool."""
        logger.info(f"Running {self.name} with expression: {expression}")
        try:
            # Replace common math functions and constants
            expression = expression.replace("pi", str(math.pi))
            expression = expression.replace("e", str(math.e))
            expression = expression.replace("sqrt", "math.sqrt")
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("log", "math.log")
            
            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, {"math": math})
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating expression: {str(e)}"
        
    async def _arun(self, expression: str) -> str:
        """Run the tool asynchronously."""
        return self._run(expression)

class RandomNumberTool(BaseTool):
    """Tool that generates random numbers within a range."""
    name: str = Field(default="random_number", description="Name of the tool")
    description: str = Field(
        default="Generate a random number within a specified range. Input format: 'min max'",
        description="Tool description"
    )
    
    def _run(self, range_str: str) -> str:
        """Run the tool."""
        logger.info(f"Running {self.name} with range: {range_str}")
        try:
            min_val, max_val = map(float, range_str.split())
            result = random.uniform(min_val, max_val)
            return f"Random number between {min_val} and {max_val}: {result}"
        except Exception as e:
            return f"Error generating random number: {str(e)}"
        
    async def _arun(self, range_str: str) -> str:
        """Run the tool asynchronously."""
        return self._run(range_str)

# Text Tools
class TextAnalyzerTool(BaseTool):
    """Tool that analyzes text and provides statistics."""
    name: str = Field(default="text_analyzer", description="Name of the tool")
    description: str = Field(
        default="""Analyze text and provide statistics.
        Returns word count, character count, and other basic text metrics.""",
        description="Tool description"
    )
    
    def _run(self, text: str) -> str:
        """Run the tool."""
        logger.info(f"Running {self.name} with text length: {len(text)}")
        try:
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            stats = {
                "characters": len(text),
                "words": len(words),
                "sentences": len(sentences),
                "average_word_length": sum(len(w) for w in words) / len(words) if words else 0,
                "average_sentence_length": sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
            }
            
            return "\n".join(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}" 
                           for k, v in stats.items())
        except Exception as e:
            return f"Error analyzing text: {str(e)}"
        
    async def _arun(self, text: str) -> str:
        """Run the tool asynchronously."""
        return self._run(text)

class TextTransformTool(BaseTool):
    """Tool that transforms text in various ways."""
    name: str = Field(default="text_transform", description="Name of the tool")
    description: str = Field(
        default="""Transform text in various ways.
        Input format: 'operation text'
        Operations: uppercase, lowercase, title, reverse, shuffle""",
        description="Tool description"
    )
    
    def _run(self, input_str: str) -> str:
        """Run the tool."""
        logger.info(f"Running {self.name} with input: {input_str[:20]}...")
        try:
            operation, text = input_str.split(" ", 1)
            operations = {
                "uppercase": str.upper,
                "lowercase": str.lower,
                "title": str.title,
                "reverse": lambda x: x[::-1],
                "shuffle": lambda x: "".join(random.sample(x, len(x)))
            }
            
            if operation not in operations:
                return f"Unknown operation. Available operations: {', '.join(operations.keys())}"
                
            result = operations[operation](text)
            return f"Transformed text ({operation}): {result}"
        except Exception as e:
            return f"Error transforming text: {str(e)}"
        
    async def _arun(self, input_str: str) -> str:
        """Run the tool asynchronously."""
        return self._run(input_str)

# Time Tools
class TimeTool(BaseTool):
    """Tool that provides various time-related operations."""
    name: str = Field(default="time_tool", description="Name of the tool")
    description: str = Field(
        default="""Perform time-related operations.
        Operations: now, add_days, format
        Examples: 
        - 'now' - get current time
        - 'add_days 5' - get time 5 days from now
        - 'format 2024-03-20' - format a date""",
        description="Tool description"
    )
    
    def _run(self, operation: str) -> str:
        """Run the tool."""
        logger.info(f"Running {self.name} with operation: {operation}")
        try:
            if operation == "now":
                return f"Current time: {datetime.now().isoformat()}"
            
            parts = operation.split()
            if parts[0] == "add_days":
                days = int(parts[1])
                future = datetime.now() + timedelta(days=days)
                return f"Time {days} days from now: {future.isoformat()}"
            
            if parts[0] == "format":
                date_str = parts[1]
                date = datetime.fromisoformat(date_str)
                return f"Formatted date: {date.strftime('%B %d, %Y')}"
            
            return "Unknown operation. Available operations: now, add_days, format"
        except Exception as e:
            return f"Error processing time operation: {str(e)}"
        
    async def _arun(self, operation: str) -> str:
        """Run the tool asynchronously."""
        return self._run(operation)

# Fun Tools
class FortuneTool(BaseTool):
    """Tool that provides random fortunes."""
    name: str = Field(default="fortune", description="Name of the tool")
    description: str = Field(
        default="Get a random fortune or piece of wisdom.",
        description="Tool description"
    )
    
    fortunes: ClassVar[List[str]] = [
        "A beautiful, smart, and loving person will be coming into your life.",
        "A dubious friend may be an enemy in camouflage.",
        "A faithful friend is a strong defense.",
        "A fresh start will put you on your way.",
        "A golden egg of opportunity falls into your lap this month.",
        "A lifetime friend shall soon be made.",
        "A light heart carries you through all the hard times.",
        "A new perspective will come with the new year.",
        "A pleasant surprise is waiting for you.",
        "A short pencil is usually better than a long memory any day.",
    ]
    
    def _run(self, _: str = "") -> str:
        """Run the tool."""
        logger.info(f"Running {self.name}")
        return random.choice(self.fortunes)
        
    async def _arun(self, _: str = "") -> str:
        """Run the tool asynchronously."""
        return self._run()

class JokeTool(BaseTool):
    """Tool that tells random jokes."""
    name: str = Field(default="joke", description="Name of the tool")
    description: str = Field(
        default="Get a random programming or tech-related joke.",
        description="Tool description"
    )
    
    jokes: ClassVar[List[str]] = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the programmer quit their job? Because they didn't get arrays!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
        "Why was the JavaScript developer sad? Because they didn't know how to 'null' their feelings!",
        "Why do programmers always mix up Halloween and Christmas? Because Oct 31 == Dec 25!",
        "Why did the developer go broke? Because they used up all their cache!",
        "What do you call a computer that sings? A Dell!",
        "Why did the AI assistant go to therapy? It had too many deep learning issues!",
        "What's a programmer's favorite hangout place? The Foo Bar!",
        "Why did the database administrator leave their wife? She had one-to-many relationships!",
    ]
    
    def _run(self, _: str = "") -> str:
        """Run the tool."""
        logger.info(f"Running {self.name}")
        return random.choice(self.jokes)
        
    async def _arun(self, _: str = "") -> str:
        """Run the tool asynchronously."""
        return self._run()

class SimpleCallbackHandler(BaseCallbackHandler):
    """Simple callback handler for streaming responses."""
    
    def __init__(self):
        super().__init__()
        self.collected_tokens = []
        self.run_inline = True  # Required by LangChain
        
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        """Handle start of LLM."""
        pass
        
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Handle new token."""
        print(token, end="", flush=True)
        self.collected_tokens.append(token)
        
    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """Handle end of LLM response."""
        print("\n")  # Add newline after response
        
    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Handle LLM error."""
        logger.error(f"LLM error: {error}")
        
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """Handle start of chain."""
        pass
        
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Handle end of chain."""
        pass
        
    def on_chain_error(self, error: Exception, **kwargs: Any) -> None:
        """Handle chain error."""
        logger.error(f"Chain error: {error}")
        
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
        """Handle start of tool."""
        logger.info(f"Calling tool: {serialized['name']}")
        
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Handle end of tool."""
        pass
        
    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Handle tool error."""
        logger.error(f"Tool error: {error}")
        
    def get_content(self) -> str:
        """Get the complete collected response."""
        return "".join(self.collected_tokens)

async def chat_loop(llm: LLM, system_message: Optional[str] = None) -> None:
    """
    Run an interactive chat loop with the LLM.
    
    Args:
        llm: LLM instance to use
        system_message: Optional system message to set context
    """
    messages: List[BaseMessage] = []
    
    # Add system message if provided
    if system_message:
        messages.append(SystemMessage(content=system_message))
        print(f"System: {system_message}\n")
    
    print("Starting chat (type 'exit' to quit, 'tools' to list available tools)")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle special commands
            if user_input.lower() == "exit":
                break
            elif user_input.lower() == "tools":
                print("\nAvailable tools:")
                for tool in llm.tools:
                    print(f"- {tool.name}: {tool.description}")
                continue
            elif not user_input:
                continue
                
            # Add user message
            messages.append(HumanMessage(content=user_input))
            
            # Create callback handler for streaming
            callback = SimpleCallbackHandler()
            
            # Generate response
            print("\nAssistant: ", end="", flush=True)
            response = await llm.agenerate_response(
                messages=messages,
                callbacks=[callback],
                use_tools=True  # Enable tools by default
            )
            
            # Add assistant message
            messages.append(AIMessage(content=response))
            
        except KeyboardInterrupt:
            print("\nExiting chat...")
            break
        except Exception as e:
            logger.error(f"Error in chat loop: {e}")
            print(f"\nError: {str(e)}")

async def main():
    """Main entry point for the test tool."""
    try:
        # Parse command line arguments
        args = parse_args()
        
        # Load default LLM configuration
        config = load_llm_config()
        print(f"Loaded LLM configuration with default model: {config['default_model']}")
        print(f"Using model: {args.llm}")
        
        # Initialize LLM with specified model
        llm = LLM(model_key=args.llm)
        
        # Register all tools
        llm.add_tool(CalculatorTool())
        llm.add_tool(RandomNumberTool())
        llm.add_tool(TextAnalyzerTool())
        llm.add_tool(TextTransformTool())
        llm.add_tool(TimeTool())
        llm.add_tool(FortuneTool())
        llm.add_tool(JokeTool())
        
        # Use a more comprehensive system message
        system_message = """You are a test assistant for the LLM class with access to various tools.
Your role is to help test the LLM implementation and demonstrate tool usage.

Available tools:
- calculator: Perform mathematical calculations
- random_number: Generate random numbers in a range
- text_analyzer: Analyze text and provide statistics
- text_transform: Transform text (uppercase, lowercase, title, reverse, shuffle)
- time_tool: Time operations (now, add_days, format)
- fortune: Get random fortunes
- joke: Tell programming jokes

Keep your responses concise and focused on demonstrating tool functionality.
When using tools, explain what you're doing and why."""

        # Start chat loop
        await chat_loop(llm, system_message)
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Configure logging
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG"
    )
    
    # Run the async main function
    asyncio.run(main()) 