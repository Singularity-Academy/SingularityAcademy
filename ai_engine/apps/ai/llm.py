"""
LLM (Large Language Model) implementation for the AI Engine.

This module provides a wrapper around LangChain's chat models for consistent
interaction with different LLM providers.
"""

import os
from typing import List, Optional, Dict, Any, Callable, Union, Type
from datetime import datetime
from loguru import logger
from pydantic import BaseModel, Field

from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain.tools import BaseTool, StructuredTool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from ai_engine.logging import log_exception

from ...config import load_llm_config

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
        self._chain = None
        self._achain = None
        self._tool_chain = None
        self._tool_achain = None
        
        logger.info(f"Initialized LLM with model: {self.config['name']} ({self.model_key})")
        
    def add_tool(self, tool: BaseTool) -> None:
        """
        Add a tool to the LLM instance.
        
        Args:
            tool: A LangChain BaseTool instance to add.
        """
        self.tools.append(tool)
        # Reset chains to force recreation with new tools
        self._tool_chain = None
        self._tool_achain = None
        logger.debug(f"Added tool: {tool.name}")

    @property
    def chain(self) -> ChatOpenAI:
        """
        Get or create the synchronous LCEL chain.
        
        Returns:
            ChatOpenAI: Configured synchronous chain instance.
            
        Note:
            The chain is created lazily on first access and reused for subsequent calls.
        """
        if self._chain is None:
            # Create the base model
            model = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
            
            # Create the LCEL chain
            self._chain = (
                RunnablePassthrough() 
                | model 
                | StrOutputParser()
            )
            
        return self._chain
        
    @property
    def tool_chain(self) -> AgentExecutor:
        """
        Get or create the synchronous tool-enabled LCEL chain.
        
        Returns:
            AgentExecutor: Configured synchronous tool-enabled chain instance.
        """
        if self._tool_chain is None and self.tools:
            model = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful AI assistant that can use tools when needed."),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
            
            agent = create_openai_functions_agent(model, self.tools, prompt)
            self._tool_chain = AgentExecutor(agent=agent, tools=self.tools)
            
        return self._tool_chain

    @property
    def achain(self) -> ChatOpenAI:
        """
        Get or create the asynchronous LCEL chain.
        
        Returns:
            ChatOpenAI: Configured asynchronous chain instance.
            
        Note:
            The chain is created lazily on first access and reused for subsequent calls.
        """
        if self._achain is None:
            # Create the base model
            model = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
            
            # Create the async LCEL chain
            self._achain = (
                RunnablePassthrough() 
                | model 
                | StrOutputParser()
            )
            
        return self._achain

    @property
    def tool_achain(self) -> AgentExecutor:
        """
        Get or create the asynchronous tool-enabled LCEL chain.
        
        Returns:
            AgentExecutor: Configured asynchronous tool-enabled chain instance.
        """
        if self._tool_achain is None and self.tools:
            model = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful AI assistant that can use tools when needed."),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
            
            agent = create_openai_functions_agent(model, self.tools, prompt)
            self._tool_achain = AgentExecutor(agent=agent, tools=self.tools)
            
        return self._tool_achain

    def generate_response(
        self, 
        messages: List[BaseMessage],
        use_tools: bool = False
    ) -> str:
        """
        Generate a response synchronously.
        
        Args:
            messages: List of messages to generate a response for.
                     Each message should be an instance of BaseMessage
                     (e.g., SystemMessage, HumanMessage, AIMessage).
            use_tools: Whether to use tools for generation. If True and no tools
                      are registered, falls back to normal generation.
            
        Returns:
            str: The generated response text.
            
        Raises:
            Exception: If generation fails after all retry attempts.
        """
        try:
            logger.debug(f"Generating response with {self.model_key} for {len(messages)} messages")
            if use_tools and self.tools:
                return self.tool_chain.invoke({"messages": messages})["output"]
            return self.chain.invoke(messages)
        except Exception as e:
            log_exception(e, f"Error generating response with {self.model_key}")

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
                     Each message should be an instance of BaseMessage
                     (e.g., SystemMessage, HumanMessage, AIMessage).
            callbacks: Optional list of callback handlers for streaming.
                      Useful for implementing streaming responses or
                      custom logging/monitoring.
            use_tools: Whether to use tools for generation. If True and no tools
                      are registered, falls back to normal generation.
            
        Returns:
            str: The generated response text.
            
        Raises:
            Exception: If generation fails after all retry attempts.
        """
        try:
            logger.debug(f"Generating async response with {self.model_key} for {len(messages)} messages")
            if use_tools and self.tools:
                return (await self.tool_achain.ainvoke(
                    {"messages": messages},
                    config={"callbacks": callbacks}
                ))["output"]
            return await self.achain.ainvoke(messages, config={"callbacks": callbacks})
        except Exception as e:
            log_exception(e, f"Error generating async response with {self.model_key}")

    def __repr__(self) -> str:
        """
        String representation of the LLM instance.
        
        Returns:
            str: A string showing the model name and key.
        """
        return f"LLM(model='{self.config['name']}', key='{self.model_key}')"
