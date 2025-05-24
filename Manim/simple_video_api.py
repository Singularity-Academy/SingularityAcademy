#!/usr/bin/env python3
"""
简化版 AI Manim 视频生成器 API
直接使用预设模板生成视频，避免AI依赖
"""

import os
import uuid
import subprocess
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 简化配置
CONFIG = {
    "output_dir": "api_videos",
    "max_content_length": 200,
    "python_path": "/usr/local/bin/python3.10"
}

# 创建输出目录
Path(CONFIG["output_dir"]).mkdir(exist_ok=True)

# 预设视频模板
VIDEO_TEMPLATES = {
    "牛顿第一定律": """from manim import *

class NewtonFirstLaw(Scene):
    def construct(self):
        # 设置背景
        self.camera.background_color = "#1e1e2e"
        
        # 标题
        title = Text("牛顿第一定律 - 惯性原理", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 公式
        formula = MathTex(r"F = 0 \\Rightarrow a = 0")
        formula.scale(1.2)
        formula.shift(UP*0.5)
        self.play(Write(formula))
        self.wait(1)
        
        # 地面
        ground = Line(LEFT*5, RIGHT*5, color=WHITE)
        ground.shift(DOWN*2)
        self.play(Create(ground))
        
        # 方块
        box = Square(side_length=0.8, color=RED, fill_opacity=0.7)
        box.shift(LEFT*2 + DOWN*1.6)
        self.play(Create(box))
        
        # 说明文字
        text1 = Text("物体保持静止状态", font_size=24, color=GREEN)
        text1.shift(DOWN*0.5)
        self.play(Write(text1))
        self.wait(2)
        
        # 施加力
        force_arrow = Arrow(
            start=box.get_right() + RIGHT*0.3,
            end=box.get_right() + RIGHT*1,
            color=YELLOW
        )
        self.play(Create(force_arrow))
        
        # 运动
        self.play(
            box.animate.shift(RIGHT*3),
            force_arrow.animate.shift(RIGHT*3),
            run_time=2
        )
        
        # 撤除力
        self.play(FadeOut(force_arrow))
        text2 = Text("撤除力后保持匀速运动", font_size=20, color=BLUE)
        text2.shift(DOWN*3)
        self.play(Write(text2))
        
        # 继续运动
        self.play(box.animate.shift(RIGHT*1.5), run_time=2, rate_func=linear)
        
        # 结论
        conclusion = Text("这就是惯性原理！", font_size=28, color=GOLD)
        conclusion.shift(UP*2)
        self.play(Write(conclusion))
        self.wait(2)
        
        # 淡出
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)""",
    
    "圆周运动": """from manim import *

class CircularMotion(Scene):
    def construct(self):
        self.camera.background_color = "#0f1419"
        
        # 标题
        title = Text("圆周运动", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 圆形轨道
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        
        # 运动的点
        dot = Dot(color=RED)
        dot.move_to(circle.point_at_angle(0))
        self.play(Create(dot))
        
        # 向心力箭头
        arrow = Arrow(start=ORIGIN, end=ORIGIN, color=YELLOW)
        
        # 标签
        label = Text("向心力指向圆心", font_size=24, color=GREEN)
        label.shift(DOWN*3)
        self.play(Write(label))
        
        # 圆周运动动画
        def update_arrow(mob):
            pos = dot.get_center()
            direction = -pos / np.linalg.norm(pos) * 1.5
            mob.put_start_and_end_on(pos, pos + direction)
        
        arrow.add_updater(update_arrow)
        self.add(arrow)
        
        # 让点沿圆运动
        self.play(
            MoveAlongPath(dot, circle),
            run_time=4,
            rate_func=linear
        )
        
        arrow.clear_updaters()
        
        # 结论
        conclusion = Text("向心力维持圆周运动", font_size=28, color=GOLD)
        conclusion.shift(UP*2.5)
        self.play(Write(conclusion))
        self.wait(2)
        
        self.play(FadeOut(Group(*self.mobjects)))""",
    
    "三角函数": """from manim import *

class TrigFunctions(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 标题
        title = Text("三角函数图像", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 坐标轴
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=4
        )
        self.play(Create(axes))
        
        # 正弦函数
        sin_graph = axes.plot(lambda x: np.sin(x), color=RED)
        sin_label = Text("sin(x)", font_size=20, color=RED)
        sin_label.next_to(sin_graph, UP)
        
        self.play(Create(sin_graph))
        self.play(Write(sin_label))
        self.wait(1)
        
        # 余弦函数
        cos_graph = axes.plot(lambda x: np.cos(x), color=BLUE)
        cos_label = Text("cos(x)", font_size=20, color=BLUE)
        cos_label.next_to(cos_graph, DOWN)
        
        self.play(Create(cos_graph))
        self.play(Write(cos_label))
        self.wait(2)
        
        # 动态点
        dot = Dot(color=YELLOW)
        t_tracker = ValueTracker(0)
        
        def update_dot(mob):
            t = t_tracker.get_value()
            x = t
            y = np.sin(t)
            mob.move_to(axes.coords_to_point(x, y))
        
        dot.add_updater(update_dot)
        self.add(dot)
        
        # 动画展示
        self.play(t_tracker.animate.set_value(2*PI), run_time=4)
        
        dot.clear_updaters()
        
        # 结论
        conclusion = Text("周期函数的美妙世界", font_size=24, color=GOLD)
        conclusion.shift(DOWN*3)
        self.play(Write(conclusion))
        self.wait(2)
        
        self.play(FadeOut(Group(*self.mobjects)))"""
}

@app.route('/', methods=['GET'])
def home():
    """API首页"""
    return jsonify({
        "message": "🎥 简化版 AI Manim 视频生成器 API",
        "version": "1.0.0",
        "description": "使用预设模板快速生成教育动画视频",
        "available_templates": list(VIDEO_TEMPLATES.keys()),
        "endpoints": {
            "POST /generate": "生成视频",
            "GET /video/{video_id}": "获取视频文件",
            "GET /templates": "查看可用模板"
        }
    })

@app.route('/templates', methods=['GET'])
def get_templates():
    """获取可用模板"""
    return jsonify({
        "templates": list(VIDEO_TEMPLATES.keys()),
        "total": len(VIDEO_TEMPLATES),
        "usage": "在content字段中使用模板名称或相关关键词"
    })

@app.route('/generate', methods=['POST'])
def generate_video():
    """生成视频"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "请提供JSON数据"}), 400
        
        content = data.get('content', '').strip()
        title = data.get('title', '').strip()
        
        if not content:
            return jsonify({"error": "内容不能为空"}), 400
        
        if len(content) > CONFIG["max_content_length"]:
            return jsonify({"error": f"内容过长，最大{CONFIG['max_content_length']}字符"}), 400
        
        # 生成ID和名称
        video_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if title:
            video_name = f"{title}_{timestamp}"
        else:
            clean_content = "".join(c for c in content if c.isalnum() or c in " _")[:15]
            video_name = f"{clean_content}_{timestamp}"
        
        print(f"🚀 开始生成视频: {content}")
        print(f"📋 视频ID: {video_id}")
        
        # 选择模板
        template_code = select_template(content)
        if not template_code:
            return jsonify({"error": "未找到匹配的模板"}), 400
        
        # 保存代码文件
        code_filename = f"{video_id}.py"
        code_path = Path(CONFIG["output_dir"]) / code_filename
        
        with open(code_path, 'w', encoding='utf-8') as f:
            f.write(template_code)
        
        print(f"💾 代码已保存: {code_path}")
        
        # 渲染视频
        success, video_path, error_msg = render_video(code_path, video_id)
        
        if success and video_path:
            video_size = os.path.getsize(video_path)
            print(f"✅ 视频生成成功: {video_path}")
            
            return jsonify({
                "success": True,
                "video_name": video_name,
                "video_id": video_id,
                "video_url": f"/video/{video_id}",
                "video_size": f"{video_size/1024:.1f} KB",
                "generated_at": datetime.now().isoformat(),
                "content": content,
                "template_used": get_template_name(content)
            })
        else:
            return jsonify({
                "success": False,
                "error": f"渲染失败: {error_msg}",
                "video_id": video_id,
                "video_name": video_name
            }), 500
            
    except Exception as e:
        print(f"❌ API错误: {e}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

def select_template(content):
    """根据内容选择模板"""
    content_lower = content.lower()
    
    # 关键词匹配
    keywords_map = {
        "牛顿": "牛顿第一定律",
        "惯性": "牛顿第一定律", 
        "第一定律": "牛顿第一定律",
        "圆周": "圆周运动",
        "向心力": "圆周运动",
        "圆形": "圆周运动",
        "三角": "三角函数",
        "正弦": "三角函数",
        "余弦": "三角函数",
        "sin": "三角函数",
        "cos": "三角函数"
    }
    
    for keyword, template in keywords_map.items():
        if keyword in content_lower:
            return VIDEO_TEMPLATES[template]
    
    # 直接匹配模板名
    for template_name in VIDEO_TEMPLATES:
        if template_name in content:
            return VIDEO_TEMPLATES[template_name]
    
    # 默认返回牛顿第一定律
    return VIDEO_TEMPLATES["牛顿第一定律"]

def get_template_name(content):
    """获取使用的模板名称"""
    content_lower = content.lower()
    
    keywords_map = {
        "牛顿": "牛顿第一定律",
        "惯性": "牛顿第一定律",
        "圆周": "圆周运动", 
        "三角": "三角函数"
    }
    
    for keyword, template in keywords_map.items():
        if keyword in content_lower:
            return template
    
    for template_name in VIDEO_TEMPLATES:
        if template_name in content:
            return template_name
    
    return "牛顿第一定律"

def render_video(code_path, video_id):
    """渲染视频"""
    try:
        # 提取类名
        with open(code_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # 简单的类名提取
        class_name = "Scene"
        for line in code_content.split('\n'):
            if 'class ' in line and '(Scene):' in line:
                class_name = line.split('class ')[1].split('(')[0].strip()
                break
        
        # 构建渲染命令
        cmd = [
            CONFIG["python_path"], "-m", "manim",
            "-qm",  # 中等质量
            "--disable_caching",
            str(code_path),
            class_name
        ]
        
        print(f"🎬 执行渲染命令: {' '.join(cmd)}")
        
        # 执行渲染
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=CONFIG["output_dir"],
            timeout=120  # 2分钟超时
        )
        
        if result.returncode == 0:
            # 查找生成的视频文件
            video_path = find_video_file(code_path.stem, class_name)
            if video_path:
                # 复制到API目录
                final_path = Path(CONFIG["output_dir"]) / f"{video_id}.mp4"
                import shutil
                shutil.copy2(video_path, final_path)
                return True, str(final_path), None
            else:
                return False, None, "视频文件未找到"
        else:
            return False, None, result.stderr
            
    except subprocess.TimeoutExpired:
        return False, None, "渲染超时"
    except Exception as e:
        return False, None, str(e)

def find_video_file(script_name, class_name):
    """查找生成的视频文件"""
    possible_paths = [
        Path(CONFIG["output_dir"]) / "media" / "videos" / script_name / "720p30" / f"{class_name}.mp4",
        Path("media") / "videos" / script_name / "720p30" / f"{class_name}.mp4",
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None

@app.route('/video/<video_id>', methods=['GET'])
def get_video(video_id):
    """获取视频文件"""
    try:
        video_path = Path(CONFIG["output_dir"]) / f"{video_id}.mp4"
        
        if not video_path.exists():
            return jsonify({"error": "视频不存在"}), 404
        
        return send_file(
            str(video_path),
            as_attachment=True,
            download_name=f"manim_video_{video_id}.mp4",
            mimetype='video/mp4'
        )
    except Exception as e:
        return jsonify({"error": f"获取视频失败: {str(e)}"}), 500

@app.route('/videos', methods=['GET'])
def list_videos():
    """列出所有视频"""
    try:
        video_dir = Path(CONFIG["output_dir"])
        videos = []
        
        for video_file in video_dir.glob("*.mp4"):
            if len(video_file.stem) == 8:  # 只显示API生成的视频
                video_id = video_file.stem
                file_size = video_file.stat().st_size
                created_time = datetime.fromtimestamp(video_file.stat().st_ctime)
                
                videos.append({
                    "video_id": video_id,
                    "size": f"{file_size/1024:.1f} KB",
                    "created_at": created_time.isoformat(),
                    "download_url": f"/video/{video_id}"
                })
        
        return jsonify({
            "total": len(videos),
            "videos": sorted(videos, key=lambda x: x['created_at'], reverse=True)
        })
    except Exception as e:
        return jsonify({"error": f"获取列表失败: {str(e)}"}), 500

if __name__ == '__main__':
    print("🎥 启动简化版 Manim 视频生成器 API")
    print("=" * 50)
    print("📡 API地址: http://localhost:6666")
    print("📚 可用模板:", list(VIDEO_TEMPLATES.keys()))
    print("🎬 生成视频: POST http://localhost:6666/generate")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=6666,  # 使用6666端口
        debug=True,
        threaded=True
    ) 