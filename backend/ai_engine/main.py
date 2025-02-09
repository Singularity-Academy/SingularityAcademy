import asyncio

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

    study_plan_event = asyncio.Event()

    async def generate_study_plan():
        study_plan = await agent.generate_study_plan()
        if study_plan == {}:
            await websocket.send_text("{\"message\": \"服务器繁忙。\"}")
        else:
            await websocket.send_text(json.dumps(study_plan))
        study_plan_event.set()

    asyncio.create_task(generate_study_plan())

    try:
        while True:
            await study_plan_event.wait()
            try:
                data = await websocket.receive_text()
            except KeyError:
                continue
            # Handle user input
            try:
                response = agent.handle_user_input(data)
            except json.decoder.JSONDecodeError:
                await websocket.send_text("{\"message\": \"服务器繁忙。\"}")
                continue
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("Client disconnected.")