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
        await websocket.send_text(str(error))
        return
    except pydantic_core._pydantic_core.ValidationError as error:
        await websocket.send_text(str(error))
        return

    await websocket.accept()

    # 使用 asyncio.Event 来控制任务完成通知
    study_plan_event = asyncio.Event()

    # 标记学习计划是否生成完成
    generated = False

    async def generate_study_plan():
        nonlocal generated
        study_plan = await agent.generate_study_plan()
        if not study_plan:  # 如果学习计划为空
            await websocket.send_text("{\"message\": \"服务器繁忙。\"}")
        else:
            await websocket.send_text(json.dumps(study_plan))
        generated = True  # 标记学习计划生成完成
        study_plan_event.set()  # 任务完成，设置事件标志

    # 启动生成学习计划的任务
    asyncio.create_task(generate_study_plan())

    try:
        while True:
            # 等待客户端发送消息
            try:
                data = await websocket.receive_text()
            except KeyError:
                continue

            # 如果学习计划未生成，返回繁忙消息
            if not generated:
                await websocket.send_text("{\"message\": \"服务器繁忙。\"}")
                continue  # 等待下一次请求

            # 学习计划已经生成，处理用户输入
            try:
                response = agent.handle_user_input(data)
                await websocket.send_text(json.dumps(response))
            except json.decoder.JSONDecodeError:
                await websocket.send_text("{\"message\": \"服务器繁忙。\"}")
                continue
    except WebSocketDisconnect:
        print("Client disconnected.")