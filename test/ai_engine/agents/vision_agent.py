from .base import BaseAgent
from langchain_community.chat_models import ChatDeepSeek
from langchain.schema import HumanMessage, SystemMessage
import cv2
import numpy as np
from PIL import Image
import io

class VisionAgent(BaseAgent):
    def __init__(self):
        self.model = ChatDeepSeek(
            model_name="deepseek-vision-v3",
            temperature=0.3
        )
        
    async def process(self, frame_data: bytes) -> Dict:
        try:
            image = Image.open(io.BytesIO(frame_data))
            
            messages = [
                SystemMessage(content="You are a visual analysis expert. Analyze the image and provide detailed educational insights."),
                HumanMessage(content=[
                    {"type": "text", "text": "Analyze this image for educational content:"},
                    {"type": "image_url", "image_url": {"url": image}}
                ])
            ]
            
            response = await self.model.ainvoke(messages)
            return {
                "type": "vision_analysis",
                "content": response.content,
                "confidence": response.additional_kwargs.get("confidence", 0.0)
            }
        except Exception as e:
            print(f"Error in vision processing: {str(e)}")
            return {"type": "error", "content": str(e)}

    async def generate_response(self, context: Dict) -> BaseMessage:
        return await self.model.ainvoke([
            SystemMessage(content="Generate educational content based on visual analysis."),
            HumanMessage(content=str(context))
        ]) 