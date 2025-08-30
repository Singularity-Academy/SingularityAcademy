"""
LLM (Large Language Model) implementation for the AI Engine.

This module provides a wrapper around LangChain's chat models for consistent
interaction with different LLM providers.
"""

import os
from typing import List, Optional, Dict, Any, Callable, Union, Type, Tuple
from datetime import datetime
from loguru import logger
from pydantic import BaseModel, Field

from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain.tools import BaseTool, StructuredTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from ai_engine.logging import log_exception

from ai_engine.config import load_llm_config
from .tools import TOOLS

# Load model configurations
CONFIG = load_llm_config()
MODEL_CONFIGS = CONFIG["models"]
DEFAULT_MODEL = CONFIG["default_model"]

class LLM:
    """
    Modern LCEL-based LLM implementation for the AI Engine.
    
    This class provides a unified interface for both synchronous and asynchronous
    generation using LangChain's ChatOpenAI implementation with LCEL pipelines.
    It supports:
    - Multiple model configurations
    - Streaming responses
    - Callback handling
    - Retry logic
    - Response caching
    - Tool calling (when enabled)
    
    Example:
        ```python
        # Create an LLM instance with default model
        llm = LLM()
        
        # Add a tool
        llm.add_tool(my_tool)
        
        # Generate a response with tools
        messages = [
            SystemMessage(content="You are a helpful AI assistant."),
            HumanMessage(content="Hello, how are you?")
        ]
        response = llm.generate_response(messages, use_tools=True)
        ```
    """
    
    def __init__(self, model_key: Optional[str] = None):
        """
        Initialize the LLM with a specific model configuration.
        
        Args:
            model_key: The key of the model to use from the configuration.
                      If None, uses the default model from configuration.
                      Must be one of the keys in the models.json configuration.
                      
        Raises:
            ValueError: If the specified model_key is not found in the configuration.
        """
        self.model_key = model_key or DEFAULT_MODEL
        self.tools: List[BaseTool] = []
        
        if self.model_key not in MODEL_CONFIGS:
            raise ValueError(
                f"Model '{self.model_key}' not found in configuration. "
                f"Available models: {', '.join(MODEL_CONFIGS.keys())}"
            )
            
        self.config = MODEL_CONFIGS[self.model_key]
        self._model = None
        self._amodel = None
        
        logger.info(f"Initialized LLM with model: {self.config['name']} ({self.model_key})")
        
    def add_tool(self, tool: BaseTool) -> None:
        """
        Add a tool to the LLM instance.
        
        Args:
            tool: A LangChain BaseTool instance to add.
        """
        self.tools.append(tool)
        # Reset models to force recreation with new tools
        self._model = None
        self._amodel = None
        logger.debug(f"Added tool: {tool.name}")

    @property
    def model(self) -> ChatOpenAI:
        """
        Get or create the synchronous model with bound tools.
        
        Returns:
            ChatOpenAI: Configured model instance with bound tools if any.
            
        Note:
            The model is created lazily on first access and reused for subsequent calls.
        """
        if self._model is None:
            # Create the base model
            base_model = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
            
            # Bind tools if any are available
            self._model = base_model.bind_tools(self.tools) if self.tools else base_model
            
        return self._model
        
    @property
    def amodel(self) -> ChatOpenAI:
        """
        Get or create the asynchronous model with bound tools.
        
        Returns:
            ChatOpenAI: Configured async model instance with bound tools if any.
            
        Note:
            The model is created lazily on first access and reused for subsequent calls.
        """
        if self._amodel is None:
            # Create the base model
            base_model = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
            
            # Bind tools if any are available
            self._amodel = base_model.bind_tools(self.tools) if self.tools else base_model
            
        return self._amodel

    @property
    def base_model(self) -> ChatOpenAI:
        """
        Get or create the base model without bound tools.
        
        Returns:
            ChatOpenAI: Configured model instance without tools.
            
        Note:
            The model is created lazily on first access and reused for subsequent calls.
        """
        if not hasattr(self, '_base_model'):
            self._base_model = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
        return self._base_model

    @property
    def abase_model(self) -> ChatOpenAI:
        """
        Get or create the base async model without bound tools.
        
        Returns:
            ChatOpenAI: Configured async model instance without tools.
            
        Note:
            The model is created lazily on first access and reused for subsequent calls.
        """
        if not hasattr(self, '_abase_model'):
            self._abase_model = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
        return self._abase_model

    def _handle_tool_calls_sync(self, response: AIMessage) -> List[BaseMessage]:
        """
        Handle tool calls from a model response synchronously.
        
        Args:
            response: The AIMessage containing tool calls.
            
        Returns:
            List of messages including tool results.
        """
        if not response.tool_calls:
            return []
            
        tool_messages = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            args = tool_call["args"]
            
            # Find the tool
            tool = next((t for t in self.tools if t.name == tool_name), None)
            if tool:
                try:
                    logger.debug(f"Running tool {tool_name} with args {args}")

                    # Execute the tool synchronously
                    result = tool.invoke(args)
                    tool_messages.append(
                        ToolMessage(
                            content=str(result),
                            tool_call_id=tool_call["id"],
                            name=tool_name
                        )
                    )
                except Exception as e:
                    logger.error(f"Tool {tool_name} failed: {e}")
                    tool_messages.append(
                        ToolMessage(
                            content=f"Tool {tool_name} failed: {str(e)}",
                            tool_call_id=tool_call["id"],
                            name=tool_name
                        )
                    )
            else:
                logger.warning(f"Tool {tool_name} not found")
                tool_messages.append(
                    ToolMessage(
                        content=f"Tool {tool_name} not available",
                        tool_call_id=tool_call["id"],
                        name=tool_name
                    )
                )
                
        return tool_messages

    async def _handle_tool_calls_async(self, response: AIMessage) -> List[BaseMessage]:
        """
        Handle tool calls from a model response asynchronously.
        
        Args:
            response: The AIMessage containing tool calls.
            
        Returns:
            List of messages including tool results.
        """
        if not response.tool_calls:
            return []
            
        tool_messages = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            args = tool_call["args"]
            
            # Find the tool
            tool = next((t for t in self.tools if t.name == tool_name), None)
            if tool:
                logger.debug(f"Running tool {tool_name} with args {args}")
                try:
                    # Execute the tool asynchronously
                    result = await tool.ainvoke(args)
                    tool_messages.append(
                        ToolMessage(
                            content=str(result),
                            tool_call_id=tool_call["id"],
                            name=tool_name
                        )
                    )
                except Exception as e:
                    logger.error(f"Tool {tool_name} failed: {e}")
                    tool_messages.append(
                        ToolMessage(
                            content=f"Tool {tool_name} failed: {str(e)}",
                            tool_call_id=tool_call["id"],
                            name=tool_name
                        )
                    )
            else:
                logger.warning(f"Tool {tool_name} not found")
                tool_messages.append(
                    ToolMessage(
                        content=f"Tool {tool_name} not available",
                        tool_call_id=tool_call["id"],
                        name=tool_name
                    )
                )
                
        return tool_messages

    def generate_response(
        self, 
        messages: List[BaseMessage],
        use_tools: bool = False,
        callbacks: Optional[List[BaseCallbackHandler]] = None
    ) -> str:
        """
        Generate a response synchronously.
        
        Args:
            messages: List of messages to generate a response for.
            use_tools: Whether to use tools for generation.
            callbacks: Optional list of callback handlers for streaming.
            
        Returns:
            str: The generated response text.
            
        Raises:
            Exception: If generation fails after all retry attempts.
        """
        try:
            logger.debug(f"Generating response with {self.model_key} for {len(messages)} messages")
            
            if not use_tools or not self.tools:
                # Simple case: no tools, just generate response using base model
                return self.base_model.invoke(messages, config={"callbacks": callbacks}).content
            
            # Get initial response from model with tools
            current_messages = messages.copy()
            response = self.model.invoke(current_messages, config={"callbacks": callbacks})
            
            # If no tool calls, we're done
            if not response.tool_calls:
                return response.content
                
            # Tool-enabled case: handle tool calls
            max_iterations = self.config["max_tool_calls"]
            iteration = 0
            
            while iteration < max_iterations:
                logger.debug(f"Tool loop iteration {iteration + 1}")
                
                # Handle tool calls from previous response synchronously
                tool_messages = self._handle_tool_calls_sync(response)
                
                # Add response and tool results to conversation
                current_messages.extend([
                    AIMessage(content="", tool_calls=response.tool_calls),
                    *tool_messages
                ])
                
                # Get next response from model
                response = self.model.invoke(current_messages, config={"callbacks": callbacks})
                
                # If no more tool calls, we're done
                if not response.tool_calls:
                    return response.content
                    
                iteration += 1
            
            # If we get here, we hit max iterations
            logger.warning(f"Maximum tool iterations ({max_iterations}) reached")
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    async def agenerate_response(
        self,
        messages: List[BaseMessage],
        callbacks: Optional[List[BaseCallbackHandler]] = None,
        use_tools: bool = False
    ) -> str:
        """
        Generate a response asynchronously.
        
        Args:
            messages: List of messages to generate a response for.
            callbacks: Optional list of callback handlers for streaming.
            use_tools: Whether to use tools for generation.
            
        Returns:
            str: The generated response text.
            
        Raises:
            Exception: If generation fails after all retry attempts.
        """
        try:
            logger.debug(f"Generating async response with {self.model_key} for {len(messages)} messages")
            
            if not use_tools or not self.tools:
                # Simple case: no tools, just generate response using base model
                return (await self.abase_model.ainvoke(
                    messages,
                    config={"callbacks": callbacks}
                )).content
            
            # Get initial response from model with tools
            current_messages = messages.copy()
            response = await self.amodel.ainvoke(current_messages, config={"callbacks": callbacks})
            
            # If no tool calls, we're done
            if not response.tool_calls:
                return response.content
                
            # Tool-enabled case: handle tool calls
            max_iterations = self.config["max_tool_calls"]
            iteration = 0
            
            while iteration < max_iterations:
                logger.debug(f"Tool loop iteration {iteration + 1}")
                
                # Handle tool calls from previous response asynchronously
                tool_messages = await self._handle_tool_calls_async(response)
                
                # Add response and tool results to conversation
                current_messages.extend([
                    AIMessage(content="", tool_calls=response.tool_calls),
                    *tool_messages
                ])
                
                # Get next response from model
                response = await self.amodel.ainvoke(current_messages, config={"callbacks": callbacks})
                
                # If no more tool calls, we're done
                if not response.tool_calls:
                    return response.content
                    
                iteration += 1
            
            # If we get here, we hit max iterations
            logger.warning(f"Maximum tool iterations ({max_iterations}) reached")
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating async response: {str(e)}")
            raise

    def __repr__(self) -> str:
        """
        String representation of the LLM instance.
        
        Returns:
            str: A string showing the model name and key.
        """
        return f"LLM(model='{self.config['name']}', key='{self.model_key}')"
    
    def load_default_tools(self) -> None:
        """
        Load the default tools for the LLM instance.
        """
        for tool in TOOLS:
            self.add_tool(tool)
        logger.info(f"[{self.model_key}] Loaded {len(TOOLS)} default tools")