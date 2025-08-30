#!/usr/bin/env python3
"""
Video Generation Tool

A command-line tool for generating educational videos using AI.
This tool provides an interactive interface for video generation with progress tracking.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from ai_engine.apps.ai.video_gen import AIVideoGenerator, TaskState
from loguru import logger

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",  # Set to DEBUG level
    colorize=True
)
logger.add(
    "logs/video_gen_{time}.log",
    rotation="1 day",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",  # Set to DEBUG level
    encoding="utf-8"
)

def setup_logging():
    """Configure logging for the tool."""
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="DEBUG"
    )

def get_user_input() -> Optional[str]:
    """
    Get user input for video generation.
    
    Returns:
        Optional[str]: User's input or None if they want to exit.
    """
    print("\n=== AI Video Generation Tool ===")
    print("Enter your video description (or 'q' to quit):")
    print("Example: 'Explain Newton's First Law of Motion'")
    print("Example: 'Show how a pendulum's motion changes with different lengths'")
    print("Example: 'Demonstrate the relationship between force and acceleration'")
    print("\nYour input: ", end="")
    
    user_input = input().strip()
    if user_input.lower() in ('q', 'quit', 'exit'):
        return None
    return user_input

def display_progress(progress: dict):
    """
    Display progress updates in a user-friendly format.
    
    Args:
        progress: Progress update dictionary from the generator.
    """
    state = progress["state"]
    message = progress["message"]
    task_uuid = progress["task_uuid"]
    
    # Map states to progress percentages
    progress_map = {
        TaskState.INITIALIZING: 0,
        TaskState.PLANNING_SCENE: 25,
        TaskState.GENERATING_CODE: 50,
        TaskState.RENDERING_VIDEO: 75,
        TaskState.COMPLETED: 100,
        TaskState.FAILED: -1
    }
    
    # Get progress percentage
    progress_pct = progress_map.get(state, 0)
    
    # Create progress bar
    if progress_pct >= 0:
        bar_length = 30
        filled_length = int(bar_length * progress_pct / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        progress_display = f"[{bar}] {progress_pct}%"
    else:
        progress_display = "[Failed]"
    
    # Display status
    print(f"\r{progress_display} | {message}", end="", flush=True)
    
    # Add newline for completed or failed states
    if state in (TaskState.COMPLETED, TaskState.FAILED):
        print()

async def generate_video():
    """Main video generation function."""
    generator = AIVideoGenerator()
    
    while True:
        # Get user input
        user_input = get_user_input()
        if user_input is None:
            print("\nExiting...")
            break
        
        print("\nGenerating video...")
        try:
            async for progress in generator.generate_video(user_input):
                display_progress(progress)
                
                if progress["state"] == TaskState.COMPLETED:
                    video_path = progress["video_path"]
                    code_path = progress["code_path"]
                    print(f"\n\nVideo generated successfully!")
                    print(f"Video saved at: {video_path}")
                    print(f"Code saved at: {code_path}")
                    print("\nPress Enter to generate another video or 'q' to quit...")
                    if input().lower() in ('q', 'quit', 'exit'):
                        return
                    
                elif progress["state"] == TaskState.FAILED:
                    print(f"\n\nGeneration failed: {progress['message']}")
                    print("\nPress Enter to try again or 'q' to quit...")
                    if input().lower() in ('q', 'quit', 'exit'):
                        return
                    
        except Exception as e:
            logger.exception(f"Unexpected error during video generation: {e}")
            print("\nPress Enter to try again or 'q' to quit...")
            if input().lower() in ('q', 'quit', 'exit'):
                return

def main():
    """Main entry point for the tool."""
    setup_logging()
    
    try:
        asyncio.run(generate_video())
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 