"""
Config module for AI Engine.

This module loads config from config.json, which provides config for Sanic.
"""
import os
import ujson as json
from sanic import Sanic
from typing import Dict, Any, Optional
from urllib.parse import quote_plus
from ..logging import logger, log_exception
from pathlib import Path

__all__ = [
    'load_app_config',
    'load_db_config',
    'load_llm_config',
    'load_manim_config',
    'construct_db_url',
    'CONFIG_DIR',
    'APP_CONFIG_PATH',
    'DB_CONFIG_PATH',
    'LLM_CONFIG_PATH',
    'MANIM_CONFIG_PATH'
]

# Get the directory where this file is located
CONFIG_DIR = Path(__file__).parent.absolute()

# Define absolute paths for config files
APP_CONFIG_PATH = CONFIG_DIR / "config.json"
DB_CONFIG_PATH = CONFIG_DIR / "db.json"
LLM_CONFIG_PATH = CONFIG_DIR / "models.json"
MANIM_CONFIG_PATH = CONFIG_DIR / "manim.json"

def load_app_config(app: Sanic) -> None:
    """Load application configuration from config.json."""
    try:
        with open(APP_CONFIG_PATH, "r") as f:
            CONFIG = json.load(f)
        app.config.update(CONFIG)
    except FileNotFoundError:
        logger.warning(f"Config file not found at {APP_CONFIG_PATH}")
        app.config.update({})
    except json.JSONDecodeError as e:
        log_exception(e, f"Invalid JSON in config file {APP_CONFIG_PATH}")

def load_db_config() -> Dict[str, Any]:
    """Load database configuration from db.json or environment variables."""
    # First try environment variables (for Docker deployment)
    if os.getenv("DB_HOST"):
        return {
            "type": "mysql",
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "name": os.getenv("DB_NAME"),
            "charset": "utf8mb4",
            "loc": "Local"
        }
    
    # Fallback to db.json file
    try:
        with open(DB_CONFIG_PATH, "r") as f:
            CONFIG = json.load(f)
        return CONFIG
    except FileNotFoundError:
        log_exception(FileNotFoundError(f"Database config file not found at {DB_CONFIG_PATH}"))
        raise
    except json.JSONDecodeError as e:
        log_exception(e, f"Invalid JSON in database config file {DB_CONFIG_PATH}")
        raise

def construct_db_url(config: Dict[str, Any]) -> str:
    """
    Construct a database URL from configuration.
    
    Args:
        config (Dict[str, Any]): Database configuration dictionary containing:
            - type: str, either "mysql" or "sqlite"
            - For MySQL:
                - user: str, database user
                - password: str, database password
                - host: str, database host
                - port: int, database port
                - name: str, database name
                - charset: str, optional, defaults to "utf8mb4"
            - For SQLite:
                - path: str, path to database file
    
    Returns:
        str: Database URL in the format required by Tortoise ORM
        
    Raises:
        ValueError: If required configuration is missing or invalid
    """
    db_type = config.get("type", "mysql").lower()
    
    if db_type == "mysql":
        # Required fields for MySQL
        required_fields = ["user", "password", "host", "port", "name"]
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValueError(f"Missing required MySQL configuration fields: {', '.join(missing_fields)}")
        
        # Optional fields with defaults
        charset = config.get("charset", "utf8mb4")
        
        # Construct MySQL URL with charset parameter only
        return (
            f"mysql://{quote_plus(config['user'])}:{quote_plus(config['password'])}"
            f"@{config['host']}:{config['port']}/{config['name']}"
            f"?charset={charset}"
        )
        
    elif db_type == "sqlite":
        if "path" not in config:
            raise ValueError("Missing required SQLite configuration field: path")
        
        # For SQLite, we use the sqlite:/// prefix followed by the path
        # The path can be relative or absolute
        path = config["path"]
        if path == ":memory:":
            return "sqlite://:memory:"
        return f"sqlite:///{path}"
        
    else:
        raise ValueError(f"Unsupported database type: {db_type}. Must be either 'mysql' or 'sqlite'")
    
def load_llm_config() -> Dict[str, Any]:
    """
    Load LLM configuration from models.json.
    
    The configuration file should contain settings for different LLM models,
    including API keys, model parameters, and other model-specific settings.
    
    Expected structure:
    {
        "default_model": str,  # Key of the default model to use
        "models": {
            "model_key": {  # This key is used as the model identifier
                "name": str,  # Display name of the model
                "model_id": str,  # Actual model identifier for the API
                "api_key": str | null,  # API key for the model (null if not set)
                "api_base": str,  # Base URL for API
                "temperature": float,  # Temperature for generation
                "max_tokens": int,  # Maximum tokens to generate
                "streaming": bool,  # Whether to use streaming responses
                "timeout": int,  # API timeout in seconds
                "retry_attempts": int,  # Number of retry attempts
                "max_tool_calls": int,  # Maximum number of tool call iterations
                "description": str  # Human-readable description of the model
            }
        }
    }
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - "models": Dict of model configurations
            - "default_model": str, key of the default model to use
        
    Raises:
        FileNotFoundError: If models.json is not found
        json.JSONDecodeError: If models.json contains invalid JSON
        ValueError: If required configuration is missing or invalid
    """
    try:
        with open(LLM_CONFIG_PATH, "r") as f:
            config = json.load(f)
            
        # Validate default_model field
        if "default_model" not in config or not isinstance(config["default_model"], str):
            raise ValueError("Missing or invalid 'default_model' field in LLM configuration")
            
        # Validate models field
        if "models" not in config or not isinstance(config["models"], dict):
            raise ValueError("Missing or invalid 'models' field in LLM configuration")
            
        if not config["models"]:
            raise ValueError("No models defined in configuration")
            
        # Validate that default_model exists in models
        if config["default_model"] not in config["models"]:
            raise ValueError(f"Default model '{config['default_model']}' not found in models configuration")
            
        # Validate each model's configuration
        required_fields = [
            "name", "model_id", "api_base", "temperature", "max_tokens",
            "streaming", "timeout", "retry_attempts", "max_tool_calls", "description"
        ]
        
        for model_key, model_config in config["models"].items():
            # Check for missing required fields
            missing_fields = [field for field in required_fields if field not in model_config]
            if missing_fields:
                raise ValueError(f"Model '{model_key}' missing required fields: {', '.join(missing_fields)}")
            
            # Validate field types
            if not isinstance(model_config["name"], str):
                raise ValueError(f"Model '{model_key}' 'name' must be a string")
            if not isinstance(model_config["model_id"], str):
                raise ValueError(f"Model '{model_key}' 'model_id' must be a string")
            if not isinstance(model_config["api_base"], str):
                raise ValueError(f"Model '{model_key}' 'api_base' must be a string")
            if not isinstance(model_config["temperature"], (int, float)):
                raise ValueError(f"Model '{model_key}' 'temperature' must be a number")
            if not isinstance(model_config["max_tokens"], int):
                raise ValueError(f"Model '{model_key}' 'max_tokens' must be an integer")
            if not isinstance(model_config["streaming"], bool):
                raise ValueError(f"Model '{model_key}' 'streaming' must be a boolean")
            if not isinstance(model_config["timeout"], int):
                raise ValueError(f"Model '{model_key}' 'timeout' must be an integer")
            if not isinstance(model_config["retry_attempts"], int):
                raise ValueError(f"Model '{model_key}' 'retry_attempts' must be an integer")
            if not isinstance(model_config["max_tool_calls"], int):
                raise ValueError(f"Model '{model_key}' 'max_tool_calls' must be an integer")
            if not isinstance(model_config["description"], str):
                raise ValueError(f"Model '{model_key}' 'description' must be a string")
            
            # Validate numeric ranges
            if not 0 <= model_config["temperature"] <= 2:
                raise ValueError(f"Model '{model_key}' 'temperature' must be between 0 and 2")
            if model_config["max_tokens"] <= 0:
                raise ValueError(f"Model '{model_key}' 'max_tokens' must be positive")
            if model_config["timeout"] <= 0:
                raise ValueError(f"Model '{model_key}' 'timeout' must be positive")
            if model_config["retry_attempts"] < 0:
                raise ValueError(f"Model '{model_key}' 'retry_attempts' must be non-negative")
            if model_config["max_tool_calls"] <= 0:
                raise ValueError(f"Model '{model_key}' 'max_tool_calls' must be positive")
            
        logger.info(f"Successfully loaded LLM configuration with {len(config['models'])} models")
        return {
            "models": config["models"],
            "default_model": config["default_model"]
        }
        
    except FileNotFoundError:
        log_exception(FileNotFoundError(f"LLM configuration file not found at {LLM_CONFIG_PATH}"))
        raise
    except json.JSONDecodeError as e:
        log_exception(e, f"Invalid JSON in LLM configuration file {LLM_CONFIG_PATH}")
        raise
    except ValueError as e:
        log_exception(e, "Invalid LLM configuration")
        raise
    except Exception as e:
        log_exception(e, "Unexpected error loading LLM configuration")
        raise

def load_manim_config() -> Dict[str, Any]:
    """
    Load Manim configuration from manim.json.
    
    The configuration file contains settings for Manim animations, including:
    - Quality settings and options
    - Output settings
    - Generation settings
    - UI settings
    
    Returns:
        Dict[str, Any]: Dictionary containing all Manim-related configuration
        
    Raises:
        FileNotFoundError: If manim.json is not found
        json.JSONDecodeError: If manim.json contains invalid JSON
        ValueError: If required configuration is missing or invalid
    """
    try:
        with open(MANIM_CONFIG_PATH, "r") as f:
            config = json.load(f)
            
        # Validate required sections
        required_sections = ["manim_settings", "output_settings", "generation_settings", "ui_settings"]
        missing_sections = [section for section in required_sections if section not in config]
        if missing_sections:
            raise ValueError(f"Missing required sections in Manim configuration: {', '.join(missing_sections)}")
            
        # Validate manim_settings
        manim_settings = config["manim_settings"]
        if "quality" not in manim_settings or manim_settings["quality"] not in manim_settings["quality_options"]:
            raise ValueError("Invalid or missing 'quality' setting in manim_settings")
            
        # Validate output_settings
        output_settings = config["output_settings"]
        required_output_fields = ["output_dir", "video_format", "max_video_duration"]
        missing_output_fields = [field for field in required_output_fields if field not in output_settings]
        if missing_output_fields:
            raise ValueError(f"Missing required fields in output_settings: {', '.join(missing_output_fields)}")
            
        # Validate generation_settings
        generation_settings = config["generation_settings"]
        if "scene_planning" not in generation_settings or "code_generation" not in generation_settings:
            raise ValueError("Missing required sections in generation_settings")
            
        # Validate ui_settings
        ui_settings = config["ui_settings"]
        required_ui_fields = ["language", "show_progress", "verbose_logging"]
        missing_ui_fields = [field for field in required_ui_fields if field not in ui_settings]
        if missing_ui_fields:
            raise ValueError(f"Missing required fields in ui_settings: {', '.join(missing_ui_fields)}")
            
        logger.info("Successfully loaded Manim configuration")
        return config
        
    except FileNotFoundError:
        log_exception(FileNotFoundError(f"Manim configuration file not found at {MANIM_CONFIG_PATH}"))
        raise
    except json.JSONDecodeError as e:
        log_exception(e, f"Invalid JSON in Manim configuration file {MANIM_CONFIG_PATH}")
        raise
    except ValueError as e:
        log_exception(e, "Invalid Manim configuration")
        raise
    except Exception as e:
        log_exception(e, "Unexpected error loading Manim configuration")
        raise