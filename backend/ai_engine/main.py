import pydantic_core
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from agents.dean_ai_agent import DeanAIAgent
import json

from go_backend.user import User

app = FastAPI()

# Path where the Go backend saves uploaded files
UPLOADS_FOLDER = '../materials/'  # Adjust the path if necessary

@app.get("/")
async def root():
    return {"message": "AI Engine is running."}

@app.websocket("/ai/dean_ai/{token}")
async def dean_ai_endpoint(websocket: WebSocket, token: str):
    material = websocket.query_params.get("material", "")
    try:
        agent = DeanAIAgent(User(token).ID, material)
    except RuntimeError as error:
        return str(error)
    except pydantic_core._pydantic_core.ValidationError as error:
        return str(error)

    await websocket.accept()

    try:
        while True:
            try:
                data = await websocket.receive_text()
            except KeyError:
                continue
            # Handle user input
            response = agent.handle_user_input(data)
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("Client disconnected.")