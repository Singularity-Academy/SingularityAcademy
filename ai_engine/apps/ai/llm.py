"""
LLM (Large Language Model) implementation for the AI Engine.

This module provides a wrapper around LangChain's chat models for consistent
interaction with different LLM providers.
"""

import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger

from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from ai_engine.logging import log_exception

from ...config import load_llm_config

# Load model configurations
CONFIG = load_llm_config()
MODEL_CONFIGS = CONFIG["models"]
DEFAULT_MODEL = CONFIG["default_model"]

class LLM:
    """
    LLM interface for generating responses using configured language models.
    
    This class provides a unified interface for both synchronous and asynchronous
    generation using LangChain's ChatOpenAI implementation. It supports:
    - Multiple model configurations
    - Streaming responses
    - Callback handling
    - Retry logic
    - Response caching
    
    Example:
        ```python
        # Create an LLM instance with default model
        llm = LLM()
        
        # Generate a response
        messages = [
            SystemMessage(content="You are a helpful AI assistant."),
            HumanMessage(content="Hello, how are you?")
        ]
        response = llm.generate_response(messages)
        
        # Generate a response asynchronously with streaming
        async def stream_handler(token: str):
            print(token, end="", flush=True)
            
        callbacks = [StreamingCallbackHandler(stream_handler)]
        response = await llm.agenerate_response(messages, callbacks=callbacks)
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
        
        if self.model_key not in MODEL_CONFIGS:
            raise ValueError(
                f"Model '{self.model_key}' not found in configuration. "
                f"Available models: {', '.join(MODEL_CONFIGS.keys())}"
            )
            
        self.config = MODEL_CONFIGS[self.model_key]
        self._client = None
        self._aclient = None
        
        logger.info(f"Initialized LLM with model: {self.config['name']} ({self.model_key})")
        
    @property
    def client(self) -> ChatOpenAI:
        """
        Get or create the synchronous ChatOpenAI client.
        
        Returns:
            ChatOpenAI: Configured synchronous client instance.
            
        Note:
            The client is created lazily on first access and reused for subsequent calls.
        """
        if self._client is None:
            self._client = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
        return self._client
        
    @property
    def aclient(self) -> ChatOpenAI:
        """
        Get or create the asynchronous ChatOpenAI client.
        
        Returns:
            ChatOpenAI: Configured asynchronous client instance.
            
        Note:
            The client is created lazily on first access and reused for subsequent calls.
        """
        if self._aclient is None:
            self._aclient = ChatOpenAI(
                model_name=self.config["model_id"],
                openai_api_key=self.config["api_key"],
                openai_api_base=self.config["api_base"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                streaming=self.config["streaming"],
                request_timeout=self.config["timeout"],
                max_retries=self.config["retry_attempts"],
            )
        return self._aclient

    def generate_response(self, messages: List[BaseMessage]) -> str:
        """
        Generate a response synchronously.
        
        Args:
            messages: List of messages to generate a response for.
                     Each message should be an instance of BaseMessage
                     (e.g., SystemMessage, HumanMessage, AIMessage).
            
        Returns:
            str: The generated response text.
            
        Raises:
            Exception: If generation fails after all retry attempts.
        """
        try:
            logger.debug(f"Generating response with {self.model_key} for {len(messages)} messages")
            response = self.client.invoke(messages)
            return response.content
        except Exception as e:
            log_exception(e, f"Error generating response with {self.model_key}")

    async def agenerate_response(
        self,
        messages: List[BaseMessage],
        callbacks: Optional[List[BaseCallbackHandler]] = None
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
            
        Returns:
            str: The generated response text.
            
        Raises:
            Exception: If generation fails after all retry attempts.
        """
        try:
            logger.debug(f"Generating async response with {self.model_key} for {len(messages)} messages")
            response = await self.aclient.agenerate([messages], callbacks=callbacks)
            return response.generations[0][0].text
        except Exception as e:
            log_exception(e, f"Error generating async response with {self.model_key}")

    def __repr__(self) -> str:
        """
        String representation of the LLM instance.
        
        Returns:
            str: A string showing the model name and key.
        """
        return f"LLM(model='{self.config['name']}', key='{self.model_key}')"
