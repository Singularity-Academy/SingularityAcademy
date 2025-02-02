from .base import BaseAgent
from manim import *
import json
import asyncio
from pathlib import Path

class ManimAgent(BaseAgent):
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
    async def process(self, script_data: Dict) -> Dict:
        try:
            # Generate Manim code from script
            scene_code = self.generate_scene_code(script_data)
            
            # Execute Manim code
            scene_path = await self.render_scene(scene_code)
            
            return {
                "type": "animation",
                "path": str(scene_path),
                "script": script_data
            }
        except Exception as e:
            return {"type": "error", "content": str(e)}
            
    def generate_scene_code(self, script_data: Dict) -> str:
        # Template for Manim scene
        return f"""
from manim import *

class EducationalScene(Scene):
    def construct(self):
        {script_data['manim_code']}
        """
        
    async def render_scene(self, scene_code: str) -> Path:
        # Save scene code
        temp_file = self.output_path / "temp_scene.py"
        temp_file.write_text(scene_code)
        
        # Render scene asynchronously
        proc = await asyncio.create_subprocess_exec(
            "manim", "-pql", str(temp_file), "EducationalScene",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()
        
        return self.output_path / "media" / "videos" / "temp_scene" / "1080p60" / "EducationalScene.mp4"

    async def generate_response(self, context: Dict) -> Dict:
        return await self.process(context) 