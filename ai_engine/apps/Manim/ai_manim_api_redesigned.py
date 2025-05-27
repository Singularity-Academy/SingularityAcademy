import os
import uuid
import json
from datetime import datetime
from pathlib import Path
from sanic import Sanic, response, Blueprint
from sanic_ext import Extend
from sanic_cors import CORS
from loguru import logger
from ai_video_generator import AIVideoGenerator
import asyncio

app = Sanic("AI_Manim_Video_Generator")
Extend(app)
CORS(app)

API_CONFIG = {
    "output_dir": "api_output",
    "max_content_length": 300,
    "port": 8888
}

Path(API_CONFIG["output_dir"]).mkdir(exist_ok=True)

try:
    ai_generator = AIVideoGenerator()
    logger.info("✅ AI视频生成器初始化成功")
    ai_available = True
except Exception as e:
    logger.error(f"⚠️ AI生成器初始化失败: {e}")
    ai_generator = None
    ai_available = False

@app.get("/")
async def home(request):
    return response.json({
        "service": "🎥 AI Manim 视频生成器 API",
        "version": "2.0.0",
        "description": "WebSocket 输入文字需求，AI 自动生成教育动画视频",
        "status": "online",
        "ai_status": "available" if ai_available else "offline",
        "endpoints": {
            "WebSocket /ws": "提交任务，实时反馈状态",
            "GET /checkstatus/<video_id>": "断线后重新连接获取状态",
            "GET /video/<video_id>": "下载视频文件",
            "GET /status": "查看API状态"
        }
    })

@app.get("/status")
async def status(request):
    return response.json({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "ai_generator": "available" if ai_available else "offline",
        "config": API_CONFIG,
        "models": list(ai_generator.list_available_models().keys()) if ai_generator else []
    })

@app.websocket("/ws")
async def websocket_handler(request, ws):
    try:
        while True:
            data = await ws.recv()
            request_data = json.loads(data)

            text = request_data.get("text", "").strip()
            title = request_data.get("title", "").strip()
            model = request_data.get("model", "").strip()
            video_id = str(uuid.uuid4())[:8]

            if not text:
                await ws.send(json.dumps({"error": "文字内容不能为空"}))
                continue
            if len(text) > API_CONFIG["max_content_length"]:
                await ws.send(json.dumps({"error": f"内容过长，最大支持{API_CONFIG['max_content_length']}字符"}))
                continue

            task_context = {
                "video_id": video_id,
                "text": text,
                "title": title,
                "model": model,
                "ws": ws
            }

            await ws.send(json.dumps({"status": "pending", "video_id": video_id}))
            asyncio.create_task(handle_task_via_ws(task_context))

    except Exception as e:
        logger.warning(f"WebSocket connection lost: {e}")

async def handle_task_via_ws(ctx):
    video_id = ctx["video_id"]
    ws = ctx["ws"]
    text = ctx["text"]
    title = ctx["title"]
    model = ctx["model"]

    try:
        if model and ai_generator:
            ai_generator.switch_model(model)

        for attempt in range(5):
            try:
                result = await ai_generator.generate_video(text)
                if result.get("video_path") and os.path.exists(result['video_path']):
                    video_path = "ai-principal-presentation.mp4"
                    import shutil
                    shutil.copy2(result['video_path'], video_path)
                    video_size = os.path.getsize(video_path)

                    info_file = Path(API_CONFIG["output_dir"]) / f"{video_id}_info.json"
                    with open(info_file, 'w', encoding='utf-8') as f:
                        json.dump({
                            "video_id": video_id,
                            "input_text": text,
                            "title": title,
                            "model_used": ai_generator.config.get("default_model", "unknown"),
                            "generated_at": datetime.now().isoformat(),
                            "file_size": video_size,
                            "scene_name": result.get('scene_name', 'Unknown')
                        }, f, ensure_ascii=False, indent=2)

                    await safe_send(ws, {"status": "success", "url": f"/video/{video_id}"})
                    return
            except Exception as e:
                await safe_send(ws, {"status": f"retry-{attempt+1}"})
                await asyncio.sleep(1)

        await safe_send(ws, {"status": f"failed-5", "video_id": video_id})

    except Exception as e:
        await safe_send(ws, {"status": f"error: {str(e)}", "video_id": video_id})

async def safe_send(ws, message):
    try:
        await ws.send(json.dumps(message))
    except Exception:
        logger.warning("WebSocket disconnected during send. Saving fallback status.")
        if 'video_id' in message:
            fallback_file = Path(API_CONFIG["output_dir"]) / f"{message['video_id']}_task.json"
            with open(fallback_file, 'w', encoding='utf-8') as f:
                json.dump(message, f)

@app.get("/checkstatus/<video_id:str>")
async def check_status(request, video_id):
    try:
        task_file = Path(API_CONFIG["output_dir"]) / f"{video_id}_task.json"
        if not task_file.exists():
            return response.json({"status": "not_found"}, status=404)

        with open(task_file, 'r', encoding='utf-8') as f:
            task = json.load(f)
            return response.json({"status": task.get("status", "unknown"), "url": task.get("url", None)})

    except Exception as e:
        return response.json({"error": f"查询失败: {str(e)}"}, status=500)

@app.get("/video/<video_id:str>")
async def download_video(request, video_id):
    try:
        video_path = f"ai-principal-presentation.mp4"
        info_file = Path(API_CONFIG["output_dir"]) / f"{video_id}_info.json"
        video_name = f"ai_video_{video_id}.mp4"

        if info_file.exists():
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    title = info.get('title', 'AI生成视频')
                    clean_title = "".join(c for c in title if c.isalnum() or c in " _-")[:20]
                    video_name = f"{clean_title}_{video_id}.mp4"
            except:
                pass

        return await response.file(
            video_path,
            filename=video_name,
            mime_type="video/mp4"
        )

    except Exception as e:
        return response.json({"error": f"下载失败: {str(e)}"}, status=500)

@app.get("/models")
async def list_models(request):
    if ai_generator:
        models = ai_generator.list_available_models()
        return response.json({
            "available_models": models,
            "current_model": ai_generator.config.get("default_model", "unknown"),
            "total": len(models)
        })
    else:
        return response.json({
            "available_models": {},
            "current_model": None,
            "total": 0,
            "error": "AI生成器不可用"
        })

if __name__ == '__main__':
    logger.info("🎥 AI Manim 视频生成器 API 启动")
    logger.info(f"📡 WebSocket 地址: ws://localhost:{API_CONFIG['port']}/ws")
    app.run(host="0.0.0.0", port=API_CONFIG['port'], access_log=True)