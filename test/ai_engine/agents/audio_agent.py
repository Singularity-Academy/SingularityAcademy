from .base import BaseAgent
import whisper_timestamped as whisper
from langchain_community.chat_models import ChatDeepSeek

class AudioAgent(BaseAgent):
    def __init__(self):
        self.model = ChatDeepSeek(model_name="deepseek-chat-v3")
        self.whisper_model = whisper.load_model("base")
        
    async def process(self, audio_data: bytes) -> Dict:
        try:
            # Process audio with Whisper
            result = self.whisper_model.transcribe(audio_data)
            
            # Analyze transcription
            response = await self.model.ainvoke([
                {"role": "system", "content": "Analyze this transcription for educational content:"},
                {"role": "user", "content": result["text"]}
            ])
            
            return {
                "type": "audio_analysis",
                "transcription": result["text"],
                "segments": result["segments"],
                "analysis": response.content
            }
        except Exception as e:
            return {"type": "error", "content": str(e)}

    async def generate_response(self, context: Dict) -> str:
        response = await self.model.ainvoke([
            {"role": "system", "content": "Generate educational content based on audio analysis."},
            {"role": "user", "content": str(context)}
        ])
        return response.content 