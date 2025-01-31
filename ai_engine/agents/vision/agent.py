import cv2
import numpy as np
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from PIL import Image
import io

class VisionAgent:
    def __init__(self, model_name: str = "gpt-4-vision-preview"):
        self.model = ChatOpenAI(model_name=model_name, max_tokens=1000)
        
    async def process_frame(self, frame_data: bytes):
        """Process video frame and return analysis"""
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(frame_data))
            
            # Analyze image using vision model
            response = await self.model.ainvoke(
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this frame and describe what you see:"},
                        {"type": "image_url", "image_url": {"url": image}}
                    ]
                }]
            )
            return response.content
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            return None

class VisionTool(BaseTool):
    name = "vision_analysis"
    description = "Analyzes video frames to understand visual content"
    
    def __init__(self):
        super().__init__()
        self.vision_agent = VisionAgent()
    
    async def arun(self, frame_data: bytes) -> str:
        return await self.vision_agent.process_frame(frame_data) 