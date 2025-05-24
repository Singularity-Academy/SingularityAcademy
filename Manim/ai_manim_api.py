#!/usr/bin/env python3
"""
AI Manim 视频生成器 API
输入：文字需求
输出：视频文件
"""

import os
import uuid
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ai_video_generator import AIVideoGenerator

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# API配置
API_CONFIG = {
    "output_dir": "api_output",
    "max_content_length": 300,
    "port": 8888
}

# 创建输出目录
Path(API_CONFIG["output_dir"]).mkdir(exist_ok=True)

# 初始化AI视频生成器
try:
    ai_generator = AIVideoGenerator()
    print("✅ AI视频生成器初始化成功")
    ai_available = True
except Exception as e:
    print(f"⚠️ AI生成器初始化失败: {e}")
    ai_generator = None
    ai_available = False

@app.route('/', methods=['GET'])
def home():
    """API首页"""
    return jsonify({
        "service": "🎥 AI Manim 视频生成器 API",
        "version": "2.0.0",
        "description": "输入文字需求，AI自动生成教育动画视频",
        "status": "online",
        "ai_status": "available" if ai_available else "offline",
        "endpoints": {
            "POST /generate": "生成视频 - 输入: {\"text\": \"您的需求\"}",
            "GET /video/{video_id}": "下载视频文件",
            "GET /status": "查看API状态"
        },
        "example": {
            "request": {
                "method": "POST",
                "url": "/generate",
                "body": {
                    "text": "牛顿第一定律",
                    "title": "物理课程（可选）"
                }
            },
            "response": {
                "success": True,
                "video_id": "abc12345",
                "download_url": "/video/abc12345"
            }
        }
    })

@app.route('/status', methods=['GET'])
def status():
    """API状态检查"""
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "ai_generator": "available" if ai_available else "offline",
        "config": {
            "output_dir": API_CONFIG["output_dir"],
            "max_content_length": API_CONFIG["max_content_length"],
            "port": API_CONFIG["port"]
        },
        "models": list(ai_generator.list_available_models().keys()) if ai_generator else []
    })

@app.route('/generate', methods=['POST'])
def generate_video():
    """
    核心API：生成视频
    输入：{"text": "课程内容文字", "title": "标题（可选）", "model": "模型（可选）"}
    输出：{"success": true, "video_id": "ID", "download_url": "/video/ID"}
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({"error": "请提供JSON数据"}), 400
        
        text = data.get('text', '').strip()
        title = data.get('title', '').strip()
        model = data.get('model', '').strip()
        
        # 验证输入
        if not text:
            return jsonify({"error": "文字内容不能为空"}), 400
        
        if len(text) > API_CONFIG["max_content_length"]:
            return jsonify({
                "error": f"内容过长，最大支持{API_CONFIG['max_content_length']}字符"
            }), 400
        
        # 生成唯一视频ID
        video_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"🚀 开始处理请求")
        print(f"📝 输入文字: {text}")
        print(f"🆔 视频ID: {video_id}")
        print(f"⏰ 时间戳: {timestamp}")
        
        # 如果指定了模型，尝试切换
        if model and ai_generator:
            ai_generator.switch_model(model)
        
        # 使用AI生成器生成视频
        if ai_available and ai_generator:
            prevErr = ""
            for i in range(5):
                try:
                    print("🤖 使用AI生成器处理...")
                    result = ai_generator.generate_video(prevErr+text)
                    try:
                        a = result.get("ERR","")
                        if a != "":
                            print("即将重试")
                            prevErr = "请注意以下错误可能导致生成失败："+str(e) + "\n"
                            continue
                    except Exception as e:
                        None
                            
                    
                    if result.get('video_path') and os.path.exists(result['video_path']):
                        # 复制视频到API输出目录
                        api_video_path = f"ai-principal-presentation.mp4"
                        import shutil
                        shutil.copy2(result['video_path'], api_video_path)
                        
                        # 获取视频信息
                        video_size = os.path.getsize(api_video_path)
                        
                        print(f"✅ 视频生成成功: {api_video_path}")
                        print(f"📊 文件大小: {video_size/1024:.1f} KB")
                        
                        # 保存生成信息
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
                        
                        return jsonify({
                            "success": True,
                            "video_id": video_id,
                            "download_url": f"/video/{video_id}",
                            "video_size": f"{video_size/1024:.1f} KB",
                            "generated_at": datetime.now().isoformat(),
                            "input_text": text,
                            "title": title or "AI生成视频",
                            "model_used": ai_generator.config.get("default_model", "unknown"),
                            "scene_name": result.get('scene_name', 'Unknown')
                        })
                    else:
                        print("即将重试")
                        prevErr = "请注意以下错误可能导致生成失败："+str(e) + "\n"
                        continue
                        return jsonify({
                            "success": False,
                            "error": "视频生成失败，请检查输入内容",
                            "video_id": video_id,
                            "fallback": True
                        }), 500
                        
                except Exception as e:
                    print(f"❌ AI生成失败: {e}")
                    prevErr = "请注意以下错误可能导致生成失败："+str(e) + "\n"
            return jsonify({
                        "success": False,
                        "error": f"AI生成失败: {str(e)}",
                        "video_id": video_id
                    }), 500
        else:
            return jsonify({
                "success": False,
                "error": "AI生成器不可用",
                "video_id": video_id,
                "suggestion": "请检查config.json中的API密钥配置"
            }), 503
            
    except Exception as e:
        print(f"❌ API错误: {e}")
        return jsonify({
            "success": False,
            "error": f"服务器错误: {str(e)}"
        }), 500

@app.route('/ai-principal-presentation.mp4', methods=['GET'])
def download_video(video_id="1"):
    """下载生成的视频"""
    try:
        video_path = f"ai-principal-presentation.mp4"
        
        #if not video_path.exists():
         #   return jsonify({"error": "视频不存在或已过期"}), 404
        
        # 读取视频信息
        info_file = Path(API_CONFIG["output_dir"]) / f"{video_id}_info.json"
        video_name = f"ai_video_{video_id}.mp4"
        
        if True:
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    title = info.get('title', 'AI生成视频')
                    clean_title = "".join(c for c in title if c.isalnum() or c in " _-")[:20]
                    video_name = f"{clean_title}_{video_id}.mp4"
            except:
                pass
        
        return send_file(
            str(video_path),
            as_attachment=False,
            download_name=video_name,
            mimetype='video/mp4'
        )
        
    except Exception as e:
        print(f"❌ 下载视频失败: {e}")
        return jsonify({"error": f"下载失败: {str(e)}"}), 500

@app.route('/videos', methods=['GET'])
def list_videos():
    """列出所有生成的视频"""
    try:
        output_dir = Path(API_CONFIG["output_dir"])
        videos = []
        
        for video_file in output_dir.glob("*.mp4"):
            video_id = video_file.stem
            file_size = video_file.stat().st_size
            created_time = datetime.fromtimestamp(video_file.stat().st_ctime)
            
            # 尝试读取视频信息
            info_file = output_dir / f"{video_id}_info.json"
            input_text = "未知内容"
            title = "AI生成视频"
            
            if info_file.exists():
                try:
                    with open(info_file, 'r', encoding='utf-8') as f:
                        info = json.load(f)
                        input_text = info.get('input_text', '未知内容')
                        title = info.get('title', 'AI生成视频')
                except:
                    pass
            
            videos.append({
                "video_id": video_id,
                "title": title,
                "input_text": input_text,
                "file_size": f"{file_size/1024:.1f} KB",
                "created_at": created_time.isoformat(),
                "download_url": f"/video/{video_id}"
            })
        
        return jsonify({
            "total": len(videos),
            "videos": sorted(videos, key=lambda x: x['created_at'], reverse=True)
        })
        
    except Exception as e:
        return jsonify({"error": f"获取视频列表失败: {str(e)}"}), 500

@app.route('/models', methods=['GET'])
def list_models():
    """列出可用的AI模型"""
    if ai_generator:
        models = ai_generator.list_available_models()
        return jsonify({
            "available_models": models,
            "current_model": ai_generator.config.get("default_model", "unknown"),
            "total": len(models)
        })
    else:
        return jsonify({
            "available_models": {},
            "current_model": None,
            "total": 0,
            "error": "AI生成器不可用"
        })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "API端点不存在"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "服务器内部错误"}), 500

if __name__ == '__main__':
    print("🎥 AI Manim 视频生成器 API 启动")
    print("=" * 50)
    print(f"📡 API地址: http://localhost:{API_CONFIG['port']}")
    print("📚 使用说明: http://localhost:8888/")
    print("🎬 生成视频: POST http://localhost:8888/generate")
    print("📥 下载视频: GET http://localhost:8888/video/{id}")
    print("🔍 查看状态: GET http://localhost:8888/status")
    print("=" * 50)
    
    # 启动Flask服务器
    app.run(
        host='0.0.0.0',      # 允许外部访问
        port=API_CONFIG['port'],  # 使用8888端口
        debug=False,         # 生产模式
        threaded=True        # 支持并发请求
    ) 