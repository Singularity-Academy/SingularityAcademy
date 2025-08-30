import asyncio
import websockets
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from config.settings import settings
from agents.vision_agent import VisionAgent
from agents.audio_agent import AudioAgent
from agents.manim_agent import ManimAgent
from memory.rag_store import RAGStore
from utils.stream import StreamProcessor

load_dotenv()

class AIEngine:
    def __init__(self):
        self.vision_agent = VisionAgent()
        self.audio_agent = AudioAgent()
        self.manim_agent = ManimAgent(settings.MANIM_OUTPUT_PATH)
        self.rag_store = RAGStore(settings.VECTOR_STORE_PATH)
        self.stream_processor = StreamProcessor()
        
    async def process_stream(self, websocket):
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            async for message in websocket:
                if isinstance(message, bytes):
                    # Process stream data
                    stream_type = self.stream_processor.detect_type(message)
                    
                    if stream_type == "image":
                        response = await self.vision_agent.process(message)
                    elif stream_type == "audio":
                        response = await self.audio_agent.process(message)
                    else:
                        response = {"type": "error", "content": "Unsupported stream type"}
                    
                    # Store interaction in RAG
                    await self.rag_store.add_interaction({
                        "type": stream_type,
                        "content": response,
                        "timestamp": datetime.now().isoformat(),
                        "session_id": session_id
                    })
                    
                    # Generate educational content with Manim
                    if response["type"] not in ["error"]:
                        manim_script = await self.generate_manim_script(response)
                        animation = await self.manim_agent.process(manim_script)
                        response["animation"] = animation
                    
                    # Send response to client
                    await websocket.send(json.dumps(response))
                    
        except websockets.exceptions.ConnectionClosed:
            print(f"Connection closed for session {session_id}")
        except Exception as e:
            print(f"Error in session {session_id}: {str(e)}")
            
    async def generate_manim_script(self, analysis: Dict) -> Dict:
        # Generate Manim script based on analysis
        prompt = f"""
        Generate a Manim animation script based on this analysis:
        {json.dumps(analysis)}
        
        Return a JSON object with:
        1. manim_code: Python code for Manim scene
        2. description: Text description of the animation
        """
        
        response = await self.vision_agent.model.ainvoke([
            {"role": "system", "content": "You are a Manim expert. Generate animation code."},
            {"role": "user", "content": prompt}
        ])
        
        return json.loads(response.content)

async def main():
    ai_engine = AIEngine()
    async with websockets.serve(
        ai_engine.process_stream,
        "localhost",
        int(os.getenv("AI_ENGINE_PORT", "8765"))
    ):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main()) 