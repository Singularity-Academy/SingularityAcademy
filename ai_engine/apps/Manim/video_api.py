#!/usr/bin/env python3
"""
AI Manim 视频生成器 - 简单API接口
输入：课程内容文字
输出：视频名字、ID、视频文件
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ai_video_generator import AIVideoGenerator

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 简化配置 - 使用基本设置
SIMPLE_CONFIG = {
    "output_dir": "api_videos",
    "max_content_length": 500,  # 最大输入字符数
    "supported_formats": ["mp4"],
    "default_quality": "medium"
}

# 创建输出目录
Path(SIMPLE_CONFIG["output_dir"]).mkdir(exist_ok=True)

# 初始化AI生成器（使用默认配置）
try:
    generator = AIVideoGenerator()
    print("✅ AI视频生成器初始化成功")
except Exception as e:
    print(f"⚠️ AI生成器初始化失败，使用基础模式: {e}")
    generator = None

@app.route('/', methods=['GET'])
def home():
    """API首页 - 显示使用说明"""
    return jsonify({
        "message": "🎥 AI Manim 视频生成器 API",
        "version": "1.0.0",
        "description": "输入课程内容，自动生成教育动画视频",
        "endpoints": {
            "POST /generate": "生成视频",
            "GET /video/{video_id}": "获取视频文件",
            "GET /status": "查看API状态"
        },
        "usage": {
            "url": "POST /generate",
            "body": {
                "content": "牛顿第一定律",
                "title": "物理课程（可选）"
            }
        }
    })

@app.route('/status', methods=['GET'])
def status():
    """API状态检查"""
    return jsonify({
        "status": "online",
        "ai_generator": "available" if generator else "offline",
        "timestamp": datetime.now().isoformat(),
        "config": {
            "output_dir": SIMPLE_CONFIG["output_dir"],
            "max_content_length": SIMPLE_CONFIG["max_content_length"],
            "default_quality": SIMPLE_CONFIG["default_quality"]
        }
    })

@app.route('/generate', methods=['POST'])
def generate_video():
    """
    生成视频API
    输入：{"content": "课程内容", "title": "标题（可选）"}
    输出：{"video_name": "名字", "video_id": "ID", "video_url": "下载链接"}
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({"error": "请提供JSON数据"}), 400
        
        content = data.get('content', '').strip()
        title = data.get('title', '').strip()
        
        # 验证输入
        if not content:
            return jsonify({"error": "课程内容不能为空"}), 400
        
        if len(content) > SIMPLE_CONFIG["max_content_length"]:
            return jsonify({
                "error": f"内容过长，最大支持{SIMPLE_CONFIG['max_content_length']}字符"
            }), 400
        
        # 生成唯一ID
        video_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 生成视频名称
        if title:
            video_name = f"{title}_{timestamp}"
        else:
            # 从内容中提取关键词作为名称
            clean_content = "".join(c for c in content if c.isalnum() or c in " _")[:20]
            video_name = f"{clean_content}_{timestamp}"
        
        print(f"🚀 开始生成视频: {content}")
        print(f"📋 视频ID: {video_id}")
        print(f"🎬 视频名称: {video_name}")
        
        # 使用AI生成器生成视频
        if generator:
            try:
                result = generator.generate_video(content)
                video_path = result.get('video_path', '')
                code_path = result.get('code_path', '')
                
                if video_path and os.path.exists(video_path):
                    # 复制视频到API输出目录
                    api_video_path = Path(SIMPLE_CONFIG["output_dir"]) / f"{video_id}.mp4"
                    import shutil
                    shutil.copy2(video_path, api_video_path)
                    
                    # 获取视频文件大小
                    video_size = os.path.getsize(api_video_path)
                    
                    print(f"✅ 视频生成成功: {api_video_path}")
                    
                    return jsonify({
                        "success": True,
                        "video_name": video_name,
                        "video_id": video_id,
                        "video_url": f"/video/{video_id}",
                        "video_size": f"{video_size/1024:.1f} KB",
                        "generated_at": datetime.now().isoformat(),
                        "content": content,
                        "scene_name": result.get('scene_name', 'Unknown')
                    })
                else:
                    # AI生成失败，使用备用方案
                    return generate_fallback_response(content, video_id, video_name)
                    
            except Exception as e:
                print(f"❌ AI生成失败: {e}")
                return generate_fallback_response(content, video_id, video_name)
        else:
            # 没有AI生成器，使用备用方案
            return generate_fallback_response(content, video_id, video_name)
            
    except Exception as e:
        print(f"❌ API错误: {e}")
        return jsonify({
            "error": "服务器内部错误",
            "message": str(e)
        }), 500

def generate_fallback_response(content, video_id, video_name):
    """备用响应 - 当AI生成失败时"""
    return jsonify({
        "success": False,
        "video_name": video_name,
        "video_id": video_id,
        "video_url": None,
        "message": "AI生成暂时不可用，已记录您的请求",
        "content": content,
        "fallback": True,
        "generated_at": datetime.now().isoformat()
    }), 202  # 202 Accepted

@app.route('/video/<video_id>', methods=['GET'])
def get_video(video_id):
    """
    获取视频文件
    """
    try:
        video_path = Path(SIMPLE_CONFIG["output_dir"]) / f"{video_id}.mp4"
        
        if not video_path.exists():
            return jsonify({"error": "视频不存在"}), 404
        
        return send_file(
            str(video_path),
            as_attachment=True,
            download_name=f"ai_video_{video_id}.mp4",
            mimetype='video/mp4'
        )
        
    except Exception as e:
        return jsonify({"error": f"获取视频失败: {str(e)}"}), 500

@app.route('/videos', methods=['GET'])
def list_videos():
    """列出所有生成的视频"""
    try:
        video_dir = Path(SIMPLE_CONFIG["output_dir"])
        videos = []
        
        for video_file in video_dir.glob("*.mp4"):
            video_id = video_file.stem
            file_size = video_file.stat().st_size
            created_time = datetime.fromtimestamp(video_file.stat().st_ctime)
            
            videos.append({
                "video_id": video_id,
                "filename": video_file.name,
                "size": f"{file_size/1024:.1f} KB",
                "created_at": created_time.isoformat(),
                "download_url": f"/video/{video_id}"
            })
        
        return jsonify({
            "total": len(videos),
            "videos": sorted(videos, key=lambda x: x['created_at'], reverse=True)
        })
        
    except Exception as e:
        return jsonify({"error": f"获取视频列表失败: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "API端点不存在"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "服务器内部错误"}), 500

if __name__ == '__main__':
    print("🎥 启动AI Manim视频生成器API")
    print("=" * 50)
    print("📡 API地址: http://localhost:7777")
    print("📚 使用说明: http://localhost:7777")
    print("🎬 生成视频: POST http://localhost:7777/generate")
    print("📁 查看视频: GET http://localhost:7777/videos")
    print("=" * 50)
    
    # 启动Flask服务器
    app.run(
        host='0.0.0.0',  # 允许外部访问
        port=7777,       # 使用7777端口
        debug=True,      # 开发模式
        threaded=True    # 支持并发请求
    ) 