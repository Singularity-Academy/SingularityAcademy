import asyncio
import websockets
import json
import os
from dotenv import load_dotenv
from agents.coordinator.agent import CoordinatorAgent
from agents.vision.agent import VisionTool
from memory.vector_store.store import VectorStore

load_dotenv()

class AIEngine:
    def __init__(self):
        self.vector_store = VectorStore()
        self.vision_tool = VisionTool()
        self.coordinator = CoordinatorAgent(tools=[self.vision_tool])
    
    async def process_stream(self, websocket):
        try:
            async for message in websocket:
                # Process incoming video/audio stream
                if isinstance(message, bytes):
                    # Handle binary data (video/audio)
                    response = await self.coordinator.process_stream({
                        "type": "frame",
                        "data": message
                    })
                    
                    # Store response in vector store
                    if response:
                        await self.vector_store.add_memory(
                            response,
                            metadata={"timestamp": asyncio.get_event_loop().time()}
                        )
                    
                    # Send response back to client
                    await websocket.send(json.dumps({
                        "type": "analysis",
                        "content": response
                    }))
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
        except Exception as e:
            print(f"Error in stream processing: {str(e)}")

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