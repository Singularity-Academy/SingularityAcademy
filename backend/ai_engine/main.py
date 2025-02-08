from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from agents.dean_ai_agent import DeanAIAgent
import os
import json

from ai_engine.go_backend.user import User

app = FastAPI()

# Path where the Go backend saves uploaded files
UPLOADS_FOLDER = '../materials/'  # Adjust the path if necessary

@app.get("/")
async def root():
    return {"message": "AI Engine is running."}

@app.websocket("/ai/dean_ai/{token}")
async def dean_ai_endpoint(websocket: WebSocket, token: str):
    material = websocket.query_params.get("material", "")
    await websocket.accept()
    agent = DeanAIAgent(User(token).ID, material)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle user input
            response = agent.handle_user_input(data)
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("Client disconnected.")