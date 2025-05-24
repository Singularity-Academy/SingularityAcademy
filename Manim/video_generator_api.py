#!/usr/bin/env python3
"""
超简单视频生成API
输入：课程内容文字
输出：1.视频名字 2.视频ID 3.视频文件
端口：9999
"""

from flask import Flask, request, jsonify, send_file
import os
import uuid
import subprocess
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# 配置
OUTPUT_DIR = "simple_videos"
PYTHON_PATH = "/usr/local/bin/python3.10"

# 创建输出目录
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# 简单的视频模板 - 牛顿第一定律
NEWTON_TEMPLATE = '''from manim import *

class SimpleNewton(Scene):
    def construct(self):
        # 标题
        title = Text("牛顿第一定律", font_size=48, color=WHITE)
        self.play(Write(title))
        self.wait(1)
        
        # 公式
        formula = MathTex(r"F = 0", font_size=36)
        formula.shift(DOWN)
        self.play(Write(formula))
        self.wait(1)
        
        # 方块演示
        box = Square(color=RED, fill_opacity=0.5)
        box.shift(LEFT*2)
        self.play(Create(box))
        
        # 说明
        text = Text("物体保持静止", font_size=24, color=GREEN)
        text.shift(DOWN*2)
        self.play(Write(text))
        self.wait(2)
        
        # 淡出
        self.play(FadeOut(Group(*self.mobjects)))
'''

@app.route('/')
def home():
    return jsonify({
        "message": "🎥 超简单视频生成API",
        "endpoints": [
            "POST /generate - 生成视频",
            "GET /video/<id> - 下载视频"
        ],
        "example": {
            "url": "/generate",
            "method": "POST",
            "body": {"content": "牛顿第一定律"}
        }
    })

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # 获取输入
        data = request.get_json() or {}
        content = data.get('content', '牛顿第一定律')
        
        # 生成唯一ID
        video_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%H%M%S")
        video_name = f"physics_{timestamp}"
        
        print(f"🚀 生成视频: {content} (ID: {video_id})")
        
        # 保存代码
        code_file = Path(OUTPUT_DIR) / f"{video_id}.py"
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(NEWTON_TEMPLATE)
        
        # 执行渲染
        cmd = [
            PYTHON_PATH, "-m", "manim",
            "-qm", "--disable_caching",
            str(code_file), "SimpleNewton"
        ]
        
        print(f"🎬 渲染命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=OUTPUT_DIR)
        
        if result.returncode == 0:
            # 查找生成的视频
            media_dir = Path(OUTPUT_DIR) / "media" / "videos" / video_id / "720p30"
            video_file = media_dir / "SimpleNewton.mp4"
            
            if video_file.exists():
                # 复制到简单路径
                final_video = Path(OUTPUT_DIR) / f"{video_id}.mp4"
                import shutil
                shutil.copy2(video_file, final_video)
                
                file_size = final_video.stat().st_size
                
                return jsonify({
                    "success": True,
                    "video_name": video_name,
                    "video_id": video_id,
                    "video_url": f"/video/{video_id}",
                    "video_size": f"{file_size/1024:.1f} KB",
                    "content": content,
                    "generated_at": datetime.now().isoformat()
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "视频文件未找到",
                    "video_id": video_id
                }), 500
        else:
            return jsonify({
                "success": False,
                "error": f"渲染失败: {result.stderr}",
                "video_id": video_id
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"生成失败: {str(e)}"
        }), 500

@app.route('/video/<video_id>')
def download(video_id):
    try:
        video_path = Path(OUTPUT_DIR) / f"{video_id}.mp4"
        
        if not video_path.exists():
            return jsonify({"error": "视频不存在"}), 404
        
        return send_file(
            str(video_path),
            as_attachment=True,
            download_name=f"video_{video_id}.mp4"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🎥 启动超简单视频生成API")
    print("📡 地址: http://localhost:9999")
    print("🎬 生成: POST http://localhost:9999/generate")
    print("📥 下载: GET http://localhost:9999/video/{id}")
    
    app.run(host='0.0.0.0', port=9999, debug=False) 