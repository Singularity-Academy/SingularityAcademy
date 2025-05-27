"""Utility for loading and managing prompts from text files."""

import os
from pathlib import Path
from typing import Dict, Optional
from loguru import logger

class PromptLoader:
    """Handles loading and caching of prompts from text files."""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        """Initialize the prompt loader.
        
        Args:
            prompts_dir: Optional path to prompts directory. If None, uses default location.
        """
        if prompts_dir is None:
            # Default to prompts directory in same folder as this file
            self.prompts_dir = Path(__file__).parent / "prompts"
        else:
            self.prompts_dir = Path(prompts_dir)
            
        self._prompt_cache: Dict[str, str] = {}
        logger.info(f"Initialized PromptLoader with prompts directory: {self.prompts_dir}")
        
    def get_prompt(self, prompt_name: str) -> str:
        """Load a prompt from a text file.
        
        Args:
            prompt_name: Name of the prompt file without extension (e.g., 'scene_plan')
            
        Returns:
            The prompt text content
            
        Raises:
            FileNotFoundError: If prompt file doesn't exist
            ValueError: If prompt file is empty
        """
        # Check cache first
        if prompt_name in self._prompt_cache:
            return self._prompt_cache[prompt_name]
            
        # Construct file path
        prompt_path = self.prompts_dir / f"{prompt_name}.txt"
        
        # Load and validate prompt
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if not content:
                raise ValueError(f"Prompt file {prompt_name}.txt is empty")
                
            # Cache the prompt
            self._prompt_cache[prompt_name] = content
            logger.debug(f"Loaded prompt '{prompt_name}' from {prompt_path}")
            return content
            
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {prompt_path}")
            raise FileNotFoundError(f"Prompt file '{prompt_name}.txt' not found in {self.prompts_dir}")
            
    def format_prompt(self, prompt_name: str, **kwargs) -> str:
        """Load a prompt and format it with the given parameters.
        
        Args:
            prompt_name: Name of the prompt file without extension
            **kwargs: Parameters to format the prompt with
            
        Returns:
            The formatted prompt text
        """
        prompt = self.get_prompt(prompt_name)
        try:
            return prompt.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing required parameter {e} for prompt '{prompt_name}'")
            raise ValueError(f"Missing required parameter {e} for prompt '{prompt_name}'")
        except Exception as e:
            logger.error(f"Error formatting prompt '{prompt_name}': {str(e)}")
            raise

# Create a default instance
default_loader = PromptLoader() 