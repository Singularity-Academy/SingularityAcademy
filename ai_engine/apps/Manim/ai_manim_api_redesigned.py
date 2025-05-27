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
        "description": "输入文字需求，AI自动生成教育动画视频",
        "status": "online",
        "ai_status": "available" if ai_available else "offline",
        "endpoints": {
            "POST /generate": "提交生成请求",
            "GET /checkstatus/<video_id>": "查询状态",
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

@app.post("/generate")
async def generate_video(request):
    try:
        data = request.json
        if not data:
            return response.json({"error": "请提供JSON数据"}, status=400)

        text = data.get("text", "").strip()
        title = data.get("title", "").strip()
        model = data.get("model", "").strip()

        if not text:
            return response.json({"error": "文字内容不能为空"}, status=400)
        if len(text) > API_CONFIG["max_content_length"]:
            return response.json({"error": f"内容过长，最大支持{API_CONFIG['max_content_length']}字符"}, status=400)

        video_id = str(uuid.uuid4())[:8]
        task_file = Path(API_CONFIG["output_dir"]) / f"{video_id}_task.json"

        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump({
                "video_id": video_id,
                "text": text,
                "title": title,
                "model": model,
                "status": "pending",
                "attempts": 0
            }, f)

        asyncio.create_task(process_video_task(video_id))

        return response.json({
            "success": True,
            "video_id": video_id,
            "check_url": f"/checkstatus/{video_id}"
        }, status=200)

    except Exception as e:
        return response.json({"success": False, "error": f"服务器错误: {str(e)}"}, status=500)

@app.get("/checkstatus/<video_id:str>")
async def check_status(request, video_id):
    try:
        task_file = Path(API_CONFIG["output_dir"]) / f"{video_id}_task.json"
        if not task_file.exists():
            return response.json({"status": "not_found"}, status=404)

        with open(task_file, 'r', encoding='utf-8') as f:
            task = json.load(f)
            if task["status"] == "success":
                return response.json({"status": f"success-/video/{video_id}"})
            elif task["status"] == "failed":
                return response.json({"status": f"failed-{task.get('attempts', 0)}"})
            else:
                return response.json({"status": "pending"})

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

async def process_video_task(video_id):
    task_file = Path(API_CONFIG["output_dir"]) / f"{video_id}_task.json"
    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            task = json.load(f)

        text = task['text']
        title = task['title']
        model = task['model']

        if model and ai_generator:
            ai_generator.switch_model(model)

        for attempt in range(5):
            try:
                result = await ai_generator.generate_video(text)
                if result.get("video_path") and os.path.exists(result['video_path']):
                    api_video_path = "ai-principal-presentation.mp4"
                    import shutil
                    shutil.copy2(result['video_path'], api_video_path)
                    video_size = os.path.getsize(api_video_path)

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

                    task["status"] = "success"
                    with open(task_file, 'w', encoding='utf-8') as f:
                        json.dump(task, f)
                    return
            except Exception as e:
                logger.warning(f"尝试 {attempt+1} 失败: {e}")
                task["attempts"] = attempt + 1
                await asyncio.sleep(1)

        task["status"] = "failed"
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task, f)

    except Exception as e:
        logger.error(f"任务处理异常: {e}")

if __name__ == '__main__':
    logger.info("🎥 AI Manim 视频生成器 API 启动")
    logger.info(f"📡 API地址: http://localhost:{API_CONFIG['port']}")
    app.run(host="0.0.0.0", port=API_CONFIG['port'], access_log=True)
