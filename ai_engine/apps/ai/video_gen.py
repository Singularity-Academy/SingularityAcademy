"""
Manim-based video generation for AI Engine.

This module provides an async interface for generating educational videos using Manim.
It handles scene planning, code generation, and video rendering with LLM integration.
"""

import json
import os
import sys
import subprocess
import uuid
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import AsyncGenerator, Dict, Any, Optional, Tuple

from loguru import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import SystemMessage, HumanMessage

# Import configuration loaders for Manim and LLM settings
from ai_engine.config import load_manim_config, load_llm_config
# Import LLM wrapper for language model interactions
from .llm import LLM
# Import default values and templates
from .video_defaults import (
    DEFAULT_SCENE_PLANS,
    DEFAULT_SCENE_PLAN_TEMPLATE,
    DEFAULT_MANIM_CODE,
    SCENE_PLAN_PROMPT,
    CODE_GENERATION_PROMPT
)
# Import prompt loader
from .prompt_loader import default_loader as prompt_loader
from ai_engine.utils import strip_markdown_code_blocks

__all__ = ["AIVideoGenerator", "TaskState"]

class TaskState(Enum):
    """
    States for video generation task progress.
    
    This enum tracks the different stages of video generation:
    - INITIALIZING: Setting up the generator and loading configurations
    - PLANNING_SCENE: Using LLM to plan the video scene
    - GENERATING_CODE: Converting scene plan to Manim code
    - RENDERING_VIDEO: Executing Manim to create the video
    - COMPLETED: Video generation finished successfully
    - FAILED: An error occurred during generation
    """
    INITIALIZING = auto()    # Initial setup phase
    PLANNING_SCENE = auto()  # Scene planning with LLM
    GENERATING_CODE = auto() # Converting plan to Manim code
    RENDERING_VIDEO = auto() # Actual video rendering
    COMPLETED = auto()       # Success state
    FAILED = auto()          # Error state

class AIVideoGenerator:
    """
    Manim-based video generation for AI Engine.
    
    This class provides an async interface for generating educational videos.
    It combines:
    - Configuration management (Manim and LLM settings)
    - LLM integration for scene planning and code generation
    - Progress tracking through async generators
    - Direct video generation capabilities
    
    The generator follows a pipeline:
    1. Load configurations and initialize components
    2. Plan scene using LLM
    3. Generate Manim code
    4. Render video
    5. Return results with progress updates
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the video generator with configuration.
        
        This constructor:
        1. Loads both Manim and LLM configurations
        2. Initializes the LLM for scene planning
        3. Sets up the output directory structure
        
        Args:
            config_path: Optional path to custom config file. 
                        If None, uses default config from config directory.
        """
        # Load configurations for both Manim and LLM settings
        self.manim_config = load_manim_config()
        self.llm_config = load_llm_config()
        
        # Initialize LLM with default model from config
        self.llm = LLM()
        
        # Set up base output directory from Manim config
        self.base_output_dir = Path(self.manim_config["output_settings"]["output_dir"])
        self.base_output_dir.mkdir(exist_ok=True)
        
        # Use current Python interpreter path for Manim execution
        self.python_path = sys.executable

    def _create_scene_prompt(self) -> str:
        """
        Create the prompt template for scene planning.
        
        Returns:
            str: Formatted prompt for scene planning.
        """
        return prompt_loader.get_prompt("scene_plan")

    def _create_code_prompt(self) -> str:
        """
        Create the prompt template for Manim code generation.
        
        Returns:
            str: Formatted prompt for code generation.
        """
        return prompt_loader.get_prompt("code_generation")

    def _extract_class_name(self, code: str) -> str:
        """
        Extract the scene class name from generated code.
        
        Args:
            code: The generated Manim code.
            
        Returns:
            str: The name of the scene class.
        """
        lines = code.split('\n')
        for line in lines:
            if 'class ' in line and '(Scene)' in line:
                class_line = line.strip()
                class_name = class_line.split('class ')[1].split('(')[0]
                return class_name
        return "GeneratedScene"

    def _get_output_paths(self, task_uuid: str) -> Tuple[Path, Path]:
        """
        Get the output paths for a specific task.
        
        Args:
            task_uuid: UUID of the generation task.
            
        Returns:
            Tuple[Path, Path]: Paths for code and video files.
        """
        # Create task-specific directory
        task_dir = self.base_output_dir / task_uuid
        task_dir.mkdir(exist_ok=True)
        
        # Define paths for code and video files
        code_path = task_dir / "scene.py"
        video_dir = task_dir / "media"
        
        return code_path, video_dir

    def _find_video_file(self, task_uuid: str, scene_name: str) -> str:
        """
        Find the generated video file.
        
        The actual directory structure is:
        {base_output_dir}/{task_uuid}/media/videos/scene/{quality}/{scene_name}.mp4
        
        Args:
            task_uuid: UUID of the generation task.
            scene_name: Name of the scene class.
            
        Returns:
            str: Path to the video file if found, error message otherwise.
        """
        task_dir = self.base_output_dir / task_uuid
        # Updated path to include 'scene' directory
        media_dir = task_dir / "media" / "videos" / "scene"
        
        # First check if media directory exists
        if not media_dir.exists():
            logger.error(f"Media directory not found at {media_dir}")
            return "Video file not found"
            
        # Search through all quality subdirectories (like 720p30, 1080p60, etc.)
        for quality_dir in media_dir.iterdir():
            if not quality_dir.is_dir():
                continue
                
            video_path = quality_dir / f"{scene_name}.mp4"
            if video_path.exists():
                logger.debug(f"Found video at {video_path}")
                return str(video_path)
        
        # If we get here, no video file was found
        logger.error(f"No video file found for scene {scene_name} in {media_dir}")
        return "Video file not found"

    async def generate_scene_plan(self, user_input: str) -> str:
        """
        Generate a scene plan using LLM asynchronously.
        
        Args:
            user_input: User's description of the desired video.
            
        Returns:
            str: Generated scene plan.
        """
        try:
            prompt = prompt_loader.format_prompt("scene_plan", user_input=user_input)
            messages = [
                SystemMessage(content="You are an expert in creating educational video scene plans."),
                HumanMessage(content=prompt)
            ]
            response = await self.llm.agenerate_response(messages)
            if not response or not response.strip():
                logger.error("Empty response from LLM during scene planning")
                return self._get_fallback_scene_plan(user_input)
            return response
        except Exception as e:
            logger.error(f"Scene planning failed: {e}")
            return self._get_fallback_scene_plan(user_input)

    def _validate_manim_code(self, code: str) -> str:
        """
        Validate and fix common Manim code issues.
        
        Args:
            code: The generated Manim code.
            
        Returns:
            str: Validated and fixed code.
        """
        # Add common imports if not present
        required_imports = [
            "from manim import *",
            "import numpy as np"
        ]
        
        # Add FRAME_WIDTH and other constants if used but not defined
        constants = {
            "FRAME_WIDTH": "config.frame_width",
            "FRAME_HEIGHT": "config.frame_height",
            "FRAME_X_RADIUS": "config.frame_width / 2",
            "FRAME_Y_RADIUS": "config.frame_height / 2"
        }
        
        lines = code.split('\n')
        fixed_lines = []
        imports_added = False
        
        # Add imports at the start
        for line in lines:
            if not imports_added and not line.startswith(('from ', 'import ')):
                for imp in required_imports:
                    if imp not in code:
                        fixed_lines.append(imp)
                imports_added = True
            fixed_lines.append(line)
            
            # Check if this line uses any constants that need to be defined
            for const, value in constants.items():
                if const in line and f"{const} = " not in code:
                    # Add constant definition after imports
                    if not any(f"{const} = " in l for l in fixed_lines):
                        fixed_lines.insert(len(required_imports), f"{const} = {value}")
        
        return '\n'.join(fixed_lines)

    async def generate_manim_code(self, scene_plan: str) -> str:
        """
        Generate Manim code from a scene plan using LLM.
        
        Args:
            scene_plan: The scene plan to convert to Manim code.
            
        Returns:
            str: Generated Manim code.
        """
        try:
            # Create the system prompt for code generation
            system_prompt = self._create_code_prompt()
            
            # Create the human message with the scene plan
            human_message = f"Scene Plan:\n{scene_plan}\n\nPlease generate the Manim code for this scene."
            
            # Create the message list
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_message)
            ]
            
            # Generate response using LLM
            response = await self.llm.agenerate_response(messages)
            if not response or not response.strip():
                logger.error("Empty response from LLM during code generation")
                return self._get_fallback_code()
            
            # Clean up code (remove markdown if present)
            code = strip_markdown_code_blocks(response)
            
            # Validate and fix common issues
            code = self._validate_manim_code(code.strip())
            return code
            
        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return self._get_fallback_code()

    def save_and_render(self, code: str, scene_name: str, task_uuid: str) -> Tuple[str, str]:
        """
        Save the generated code and render the video.
        
        Args:
            code: The Manim code to save and render.
            scene_name: Name of the scene class.
            task_uuid: UUID of the generation task.
            
        Returns:
            Tuple[str, str]: Paths to the code file and video file.
        """
        # Get output paths for this task
        code_path, video_dir = self._get_output_paths(task_uuid)
        
        # Save code file
        with open(code_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.info(f"Code saved to: {code_path}")
        
        try:
            logger.info("Starting video rendering...")
            
            # Get quality settings
            quality = self.manim_config["manim_settings"]["quality"]
            quality_flag = "-m"  # Default to medium quality
            
            if "quality_options" in self.manim_config["manim_settings"]:
                quality_config = self.manim_config["manim_settings"]["quality_options"].get(quality, {})
                quality_flag = quality_config.get("flag", "-m")
            
            # Build render command for Manim v0.19.0
            # Format: python -m manim -m scene.py SceneName
            cmd = [
                self.python_path,
                "-m", "manim",
                quality_flag,
                str(code_path.absolute()),
                scene_name
            ]
            
            logger.debug(f"Executing render command: {' '.join(cmd)}")
            
            # Execute render with timeout
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=str(code_path.parent.absolute()),  # Run from task directory
                    timeout=300  # 5 minute timeout
                )
                
                # Check if video was generated despite non-zero return code
                video_path = self._find_video_file(task_uuid, scene_name)
                if video_path != "Video file not found":
                    logger.success("Video rendering completed successfully")
                    return str(code_path), video_path
                
                # If we get here, either the return code was non-zero or no video was found
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                stdout_msg = result.stdout.strip() if result.stdout else "No output"
                
                # Try to extract the actual error from the traceback
                if "Traceback" in error_msg:
                    # Get the last error line from the traceback
                    error_lines = error_msg.split('\n')
                    for line in reversed(error_lines):
                        if line.strip() and not line.startswith('│') and not line.startswith('╰'):
                            error_msg = line.strip()
                            break
                
                # Log the error only once at debug level
                logger.debug(f"Manim render output: {stdout_msg}")
                logger.debug(f"Manim render error: {error_msg}")
                    
                # Return a more descriptive error message
                return str(code_path), f"Manim rendering failed: {error_msg}"
                
            except subprocess.TimeoutExpired:
                logger.error("Rendering timed out after 5 minutes")
                return str(code_path), "Manim rendering timed out after 5 minutes"
                
        except Exception as e:
            logger.exception(f"Rendering error: {e}")
            return str(code_path), f"Error during rendering: {str(e)}"

    def _get_fallback_scene_plan(self, user_input: str) -> str:
        """
        Get a fallback scene plan if LLM generation fails.
        
        Args:
            user_input: Original user input.
            
        Returns:
            str: Fallback scene plan.
        """
        # Check for matching preset plan
        for key in DEFAULT_SCENE_PLANS:
            if key in user_input:
                return DEFAULT_SCENE_PLANS[key]
        
        # Use template for unknown topics
        return DEFAULT_SCENE_PLAN_TEMPLATE.format(user_input=user_input)

    def _get_fallback_code(self) -> str:
        """
        Get fallback Manim code if generation fails.
        
        Returns:
            str: Fallback Manim code.
        """
        return DEFAULT_MANIM_CODE

    async def generate_video(self, user_input: str, task_uuid: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Generate a video based on user input.
        
        This is the main async generator method that:
        1. Takes a user's input describing the desired video
        2. Yields progress updates at each stage
        3. Uses async LLM calls for scene planning and code generation
        4. Renders the final video
        5. Yields the final state with video path information
        
        Args:
            user_input: The user's input describing the video to generate.
                       This is passed to the LLM for scene planning.
            task_uuid: Optional UUID for the generation task. If not provided,
                      a new UUID will be generated.
            
        Yields:
            Dict containing task state and progress information at each stage.
            For COMPLETED state, includes video_path and code_path.
            For FAILED state, includes error message.
            
        Raises:
            Exception: Any error during video generation is yielded as a FAILED state
                     and then re-raised for proper error handling.
        """
        # Generate or use provided task UUID
        task_uuid = task_uuid or str(uuid.uuid4())
        logger.info(f"Starting video generation task {task_uuid}")
        logger.debug(f"User input: {user_input}")
        
        try:
            # Start the generation process
            logger.info("Initializing video generation...")
            yield {
                "state": TaskState.INITIALIZING,
                "message": "Initializing video generation...",
                "task_uuid": task_uuid
            }
            
            # Use LLM to plan the scene asynchronously
            logger.info("Planning scene...")
            yield {
                "state": TaskState.PLANNING_SCENE,
                "message": "Planning scene...",
                "task_uuid": task_uuid
            }
            scene_plan = await self.generate_scene_plan(user_input)
            logger.debug(f"Scene planning completed: {scene_plan[:100]}...")
            
            # Convert scene plan to Manim code asynchronously
            logger.info("Generating Manim code...")
            yield {
                "state": TaskState.GENERATING_CODE,
                "message": "Generating Manim code...",
                "task_uuid": task_uuid
            }
            code = await self.generate_manim_code(scene_plan)
            logger.debug(f"Code generation completed, length: {len(code)} characters")
            
            # Extract the scene class name from generated code
            scene_name = self._extract_class_name(code)
            logger.debug(f"Scene class name: {scene_name}")
            
            # Start the actual video rendering process
            logger.info("Starting video rendering...")
            yield {
                "state": TaskState.RENDERING_VIDEO,
                "message": "Rendering video...",
                "task_uuid": task_uuid
            }
            
            # Save the code and render the video
            code_path, video_path = self.save_and_render(
                code=code,
                scene_name=scene_name,
                task_uuid=task_uuid
            )
            
            # Check if video generation was successful
            if isinstance(video_path, str) and Path(video_path).exists():
                logger.success(f"Video generation completed: {video_path}")
                yield {
                    "state": TaskState.COMPLETED,
                    "message": "Video generation completed successfully",
                    "code_path": code_path,
                    "video_path": video_path,
                    "task_uuid": task_uuid
                }
            else:
                # Log the error only once at error level
                logger.error(f"Video generation failed: {video_path}")
                yield {
                    "state": TaskState.FAILED,
                    "message": video_path,  # Use the error message directly
                    "code_path": code_path,
                    "task_uuid": task_uuid
                }
                
        except Exception as e:
            # Log the error only once at error level
            logger.error(f"Error during video generation: {e}")
            yield {
                "state": TaskState.FAILED,
                "message": str(e),
                "task_uuid": task_uuid
            }
            raise