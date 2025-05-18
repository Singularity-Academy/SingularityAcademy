"""
Model configuration module for AI Engine.
Defines settings and configurations for different LLM models.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from functools import lru_cache
import os
import json
from pathlib import Path
from loguru import logger

@dataclass
class ModelConfig:
    """Configuration for a single model."""
    name: str  # Display name
    model_id: str  # Model identifier (e.g., "gpt-4")
    api_key: Optional[str] = None  # API key (can be None if using env var)
    api_base: str = "https://api.openai.com/v1"  # API base URL
    api_version: Optional[str] = None  # API version if needed
    temperature: float = 0.7
    max_tokens: int = 1500
    streaming: bool = True
    cache_size: int = 30  # Number of characters to cache before sending
    timeout: int = 30  # Request timeout in seconds
    retry_attempts: int = 3  # Number of retry attempts
    retry_delay: float = 1.0  # Delay between retries in seconds
    description: str = ""  # Description of the model

class ModelManager:
    """Manages model configurations and provides access to model settings."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the model manager.
        
        Args:
            config_path: Optional path to model configuration file.
                        If not provided, uses default path.
        """
        self._config_path = config_path or os.path.join(
            os.path.dirname(__file__), 
            'config', 
            'models.json'
        )
        self._config: Dict[str, Any] = {}
        self._models: Dict[str, ModelConfig] = {}
        self._default_model: Optional[str] = None
        
        # Load configurations
        self._load_configurations()
        
        logger.info(f"ModelManager initialized with {len(self._models)} models")
        logger.info(f"Default model: {self._default_model}")
    
    def _load_configurations(self) -> None:
        """Load model configurations from file or use defaults."""
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r') as f:
                    self._config = json.load(f)
                    
                # Load models
                for model_id, model_data in self._config.get('models', {}).items():
                    self._models[model_id] = ModelConfig(
                        name=model_data['name'],
                        model_id=model_data['model_id'],
                        api_key=model_data.get('api_key'),
                        api_base=model_data['api_base'],
                        temperature=float(model_data['temperature']),
                        max_tokens=int(model_data['max_tokens']),
                        streaming=bool(model_data['streaming']),
                        cache_size=int(model_data['cache_size']),
                        timeout=int(model_data['timeout']),
                        retry_attempts=int(model_data['retry_attempts']),
                        retry_delay=float(model_data['retry_delay']),
                        description=model_data['description']
                    )
                
                # Set default model
                self._default_model = self._config.get('default_model')
                if self._default_model and self._default_model not in self._models:
                    logger.warning(f"Default model {self._default_model} not found in configuration")
                    self._default_model = next(iter(self._models.keys())) if self._models else None
            else:
                logger.warning(f"Model config file not found at {self._config_path}, using defaults")
                self._load_default_config()
                
        except Exception as e:
            logger.error(f"Error loading model config from {self._config_path}: {e}")
            self._load_default_config()
    
    def _load_default_config(self) -> None:
        """Load default model configurations."""
        # Default to GPT-4 if config file is not available
        self._models = {
            "gpt-4": ModelConfig(
                name="GPT-4",
                model_id="gpt-4",
                api_key=None,
                api_base="https://api.openai.com/v1",
                temperature=0.7,
                max_tokens=1500,
                streaming=True,
                cache_size=30,
                timeout=60,
                retry_attempts=3,
                retry_delay=1.0,
                description="OpenAI's most capable model, optimized for complex tasks"
            )
        }
        self._default_model = "gpt-4"
    
    def get_model_config(self, model_id: str) -> Optional[ModelConfig]:
        """Get configuration for a specific model."""
        return self._models.get(model_id)
    
    def get_default_model(self) -> Optional[ModelConfig]:
        """Get the default model configuration."""
        if not self._default_model:
            return None
        return self._models.get(self._default_model)
    
    def list_models(self) -> Dict[str, ModelConfig]:
        """List all available model configurations."""
        return self._models.copy()
    
    def set_default_model(self, model_id: str) -> bool:
        """
        Set the default model.
        
        Args:
            model_id: ID of the model to set as default
            
        Returns:
            True if successful, False if model not found
        """
        if model_id not in self._models:
            logger.warning(f"Model {model_id} not found in configuration")
            return False
            
        self._default_model = model_id
        logger.info(f"Default model set to {model_id}")
        return True
    
    @lru_cache(maxsize=32)
    def get_static_file(self, file_path: str) -> str:
        """
        Get contents of a static file with caching.
        
        Args:
            file_path: Path to the static file
            
        Returns:
            Contents of the file as string
        """
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading static file {file_path}: {e}")
            return ""

# Create singleton instance
model_manager = ModelManager()

def get_model_config(model_id: Optional[str] = None) -> Optional[ModelConfig]:
    """
    Get model configuration.
    
    Args:
        model_id: Optional model ID. If not provided, returns default model config.
        
    Returns:
        ModelConfig object or None if model not found
    """
    if model_id:
        return model_manager.get_model_config(model_id)
    return model_manager.get_default_model()

# Export commonly used functions
def get_model_config(model_id: str) -> Optional[ModelConfig]:
    """Get configuration for a specific model."""
    return model_manager.get_model_config(model_id)

def get_default_model_config() -> Optional[ModelConfig]:
    """Get the default model configuration."""
    return model_manager.get_default_model()

def list_available_models() -> Dict[str, ModelConfig]:
    """List all available model configurations."""
    return model_manager.list_models() 