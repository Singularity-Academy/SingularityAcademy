from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from agents.dean_ai_agent import DeanAIAgent
import os
import json

app = FastAPI()

# Path where the Go backend saves uploaded files
UPLOADS_FOLDER = '../uploads/'  # Adjust the path if necessary

@app.get("/")
async def root():
    return {"message": "AI Engine is running."}

@app.websocket("/ws/dean_ai/{user_id}")
async def dean_ai_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    agent = DeanAIAgent(user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle user input
            response = agent.handle_user_input(data)
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("Client disconnected.") 