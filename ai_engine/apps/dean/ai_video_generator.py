#!/usr/bin/env python3
"""
AI驱动的Manim视频生成器
支持根据提示词自动生成数学动画视频
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import logging
import shutil

from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ai_engine.apps.ai.llm import LLM
from ai_engine.logging import logger, log_exception
from ai_engine.config import load_llm_config

# Hardcoded configuration matching config.json
CONFIG = {
    "default_model": "gpt-4",
    "models": {
        "gpt-4": {
            "name": "GPT-4",
            "model_id": "gpt-4",
            "api_key": "Link_T1ZLmLhcIhZvOX9bRYFM4agbjY0CNwIpCbScjEe0GG",
            "api_base": "https://api.link-ai.tech/v1",
            "temperature": 0.7,
            "max_tokens": 2000,
            "streaming": True,
            "timeout": 60,
            "retry_attempts": 3,
            "description": "OpenAI's most capable model, optimized for complex mathematical and educational content generation"
        },
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "model_id": "gpt-4-1106-preview",
            "api_key": "Link_T1ZLmLhcIhZvOX9bRYFM4agbjY0CNwIpCbScjEe0GG",
            "api_base": "https://api.link-ai.tech/v1",
            "temperature": 0.7,
            "max_tokens": 2000,
            "streaming": True,
            "timeout": 60,
            "retry_attempts": 3,
            "description": "Latest GPT-4 model with improved performance and lower cost, ideal for educational animations"
        },
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "model_id": "gpt-3.5-turbo",
            "api_key": "Link_T1ZLmLhcIhZvOX9bRYFM4agbjY0CNwIpCbScjEe0GG",
            "api_base": "https://api.link-ai.tech/v1",
            "temperature": 0.7,
            "max_tokens": 2000,
            "streaming": True,
            "timeout": 60,
            "retry_attempts": 3,
            "description": "Fast and cost-effective model, suitable for basic mathematical animations"
        },
        "deepseek-v3": {
            "name": "Deepseek Chat v3",
            "model_id": "deepseek-chat",
            "api_key": "sk-f4035b1b6ee54b58871ed85d2e53e21f",
            "api_base": "https://api.deepseek.com/v1",
            "temperature": 0.7,
            "max_tokens": 2000,
            "streaming": True,
            "timeout": 60,
            "retry_attempts": 3,
            "description": "Deepseek's latest model with strong performance on coding and mathematical reasoning tasks"
        }
    },
    "manim_settings": {
        "quality": "medium",
        "preview": True,
        "frame_rate": 30,
        "resolution": "1080p",
        "quality_options": {
            "low": {
                "flag": "-ql",
                "resolution": "480p",
                "frame_rate": 15,
                "description": "Fast rendering for quick previews"
            },
            "medium": {
                "flag": "-qm",
                "resolution": "720p",
                "frame_rate": 30,
                "description": "Balanced quality and rendering speed"
            },
            "high": {
                "flag": "-qh",
                "resolution": "1080p",
                "frame_rate": 60,
                "description": "High quality for final output"
            },
            "4k": {
                "flag": "-qk",
                "resolution": "2160p",
                "frame_rate": 60,
                "description": "Ultra high quality for professional use"
            }
        }
    },
    "output_settings": {
        "output_dir": "ai_generated_videos",
        "keep_intermediate_files": True,
        "auto_backup": True,
        "max_video_duration": 120,
        "video_format": "mp4",
        "audio_enabled": False
    },
    "generation_settings": {
        "scene_planning": {
            "include_formulas": True,
            "include_animations": True,
            "include_colors": True,
            "chinese_support": True,
            "max_scene_complexity": "medium"
        },
        "code_generation": {
            "add_comments": True,
            "use_meaningful_names": True,
            "include_error_handling": False,
            "optimize_for_readability": True
        },
        "fallback_enabled": True,
        "debug_mode": False
    },
    "ui_settings": {
        "language": "zh-CN",
        "show_progress": True,
        "verbose_logging": True,
        "color_output": True
    }
}

class AIVideoGenerator:
    def __init__(self, selected_model: str = None):
        """初始化AI视频生成器"""
        # 如果指定了模型，覆盖默认设置
        self.model_key = selected_model or CONFIG["default_model"]
        if self.model_key not in CONFIG["models"]:
            logger.warning(f"⚠️  指定的模型 '{self.model_key}' 不存在，使用默认模型 {CONFIG['default_model']}")
            self.model_key = CONFIG["default_model"]
        
        self.model_config = CONFIG["models"][self.model_key]
        self.manim_settings = CONFIG["manim_settings"]
        self.output_settings = CONFIG["output_settings"]
        self.generation_settings = CONFIG["generation_settings"]
        self.ui_settings = CONFIG["ui_settings"]
        
        # Initialize logger
        self.logger = logger
        # Set logging level through the root logger instead
        if self.ui_settings["verbose_logging"]:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Debug logging enabled")
        else:
            logging.getLogger().setLevel(logging.INFO)
            logger.info("Info logging enabled")
        
        # Find Python executable
        self.python_path = self._find_python_executable()
        if not self.python_path:
            raise RuntimeError("Could not find Python executable with Manim installed")
        
        self.llm = self._initialize_llm()
        
        # 设置输出目录
        self.output_dir = Path(self.output_settings["output_dir"])
        self.output_dir.mkdir(exist_ok=True)
        
        # Verify Manim installation
        if not self._verify_manim_installation():
            raise RuntimeError("Manim is not properly installed or not accessible")
        
        logger.info(f"✅ AI Video Generator initialized with Python: {self.python_path}")
    
    def _find_python_executable(self) -> Optional[str]:
        """Find a Python executable with Manim installed"""
        # Try common Python executable names
        python_names = ["python3", "python3.10", "python3.9", "python3.8", "python"]
        
        for name in python_names:
            try:
                # Try to find the executable in PATH
                python_path = shutil.which(name)
                if python_path:
                    # Verify it has Manim installed
                    result = subprocess.run(
                        [python_path, "-c", "import manim; print(manim.__file__)"],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        logger.info(f"✅ Found Python with Manim: {python_path}")
                        return python_path
            except Exception as e:
                logger.debug(f"Failed to check Python {name}: {e}")
                continue
        
        logger.error("❌ Could not find Python with Manim installed")
        return None

    def _verify_manim_installation(self) -> bool:
        """Verify that Manim is properly installed and accessible"""
        try:
            result = subprocess.run(
                [self.python_path, "-m", "manim", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logger.info(f"✅ Manim version: {result.stdout.strip()}")
                return True
            else:
                logger.error(f"❌ Manim check failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to verify Manim installation: {e}")
            return False
    
    def _initialize_llm(self) -> Optional[LLM]:
        """初始化LLM实例"""
        try:
            llm = LLM(model_key=self.model_key)
            logger.info(f"✅ LLM初始化成功: {llm}")
            return llm
        except Exception as e:
            log_exception(e, "LLM初始化失败")
            return None
    
    def _create_scene_prompt(self) -> List[BaseMessage]:
        """创建场景规划提示词"""
        system_prompt = """你是一个专业的数学和物理教育动画设计师。请根据用户的输入，设计一个生动的Manim动画场景。

请按照以下格式输出详细的场景规划：

## 场景标题
[为这个动画起一个吸引人的标题]

## 场景描述
[描述整个动画的主要内容和教育目标]

## 具体元素
1. **背景设置**: [描述背景、颜色主题等]
2. **主要对象**: [列出需要展示的几何图形、文字、公式等]
3. **动画序列**: [描述动画的步骤顺序]
4. **重点强调**: [指出需要特别强调的概念或元素]

## 技术要求
- 使用Manim社区版语法
- 动画时长建议: 15-30秒
- 包含适当的数学公式
- 颜色搭配要和谐
- 动画节奏要适中

请确保场景设计既有教育价值又具有视觉吸引力。"""
        
        return [
            SystemMessage(content=system_prompt),
            HumanMessage(content="{user_input}")
        ]
    
    def _create_code_prompt(self) -> List[BaseMessage]:
        """创建代码生成提示词"""
        system_prompt = """根据以下场景规划，生成完整的Manim代码。

请生成一个完整的Manim Scene类，严格遵循以下要求：

## 1. 基本结构
```python
from manim import *
import numpy as np

class YourSceneName(Scene):
    def construct(self):
        # 你的代码
```

## 2. 重要语法规则 (必须遵守)

### 导入和基础
- 必须导入: `from manim import *`
- 如果使用随机数: `import numpy as np` 然后用 `np.random.random()`
- 不要使用 `import random`，应该使用numpy

### 中文文本处理 (关键)
- 中文文字：`Text("中文内容", font_size=32, color=WHITE)`
- 数学公式：`MathTex(r"E = mc^2")`
- 绝对不要用Tex()处理中文

### 几何对象
- 圆形：`Circle(radius=1, color=BLUE)`
- 方形：`Square(side_length=1, color=RED)`
- 矩形：`Rectangle(width=2, height=1, color=GREEN)`
- 直线：`Line(start=LEFT, end=RIGHT, color=WHITE)`
- 箭头：`Arrow(start=ORIGIN, end=UP, color=YELLOW)`
- 点：`Dot(point=ORIGIN, color=RED)`

### 动画方法 (正确的API)
- 创建：`Create(object)`
- 写入：`Write(text_object)`
- 淡入：`FadeIn(object)`
- 淡出：`FadeOut(object)`
- 变换：`Transform(obj1, obj2)`
- 移动：`object.animate.shift(direction)`
- 旋转：`object.animate.rotate(angle)`
- 缩放：`object.animate.scale(factor)`

### 方向和位置
- UP, DOWN, LEFT, RIGHT, ORIGIN
- 移动：`object.shift(UP*2)` 或 `object.animate.shift(RIGHT*3)`
- 定位：`object.move_to(UP*2 + RIGHT*1)`
- 边缘：`object.to_edge(UP)`, `object.to_corner(UL)`

### 颜色
- 基础颜色：RED, BLUE, GREEN, YELLOW, WHITE, BLACK, PURPLE, ORANGE
- 自定义：`"#FF5733"`

### 动画执行
- 播放动画：`self.play(Create(circle), run_time=2)`
- 等待：`self.wait(1)`
- 多个动画：`self.play(Write(text), Create(circle))`

### 组合对象
- 分组：`group = VGroup(obj1, obj2, obj3)`
- 排列：`group.arrange(RIGHT, buff=0.5)`

## 3. 常见错误避免

❌ 错误的写法：
- `self.camera.frame.animate` (Camera没有frame属性)
- `import random; random.random()` (应该用numpy)
- `Tex("中文")` (中文用Text)
- `rate_func='accelerate'` (应该是rate_func=rush_into)

✅ 正确的写法：
- 直接移动对象：`object.animate.shift(UP)`
- `import numpy as np; np.random.random()`
- `Text("中文", font_size=24)`
- `rate_func=rush_into` 或 `rate_func=smooth`

请直接输出Python代码，不要包含其他说明。"""
        
        return [
            SystemMessage(content=system_prompt),
            HumanMessage(content="场景规划:\n{scene_plan}")
        ]
    
    def generate_scene_plan(self, user_input: str) -> str:
        """生成场景规划"""
        if self.llm is None:
            return self._get_fallback_scene_plan(user_input)
        
        try:
            messages = self._create_scene_prompt()
            messages[1].content = messages[1].content.format(user_input=user_input)
            
            logger.info("🎯 正在规划场景...")
            scene_plan = self.llm.generate_response(messages)
            return scene_plan
        except Exception as e:
            log_exception(e, "场景规划失败")
            return self._get_fallback_scene_plan(user_input)
    
    def generate_manim_code(self, scene_plan: str) -> str:
        """根据场景规划生成Manim代码"""
        if self.llm is None:
            return self._get_fallback_code()
        
        try:
            messages = self._create_code_prompt()
            messages[1].content = messages[1].content.format(scene_plan=scene_plan)
            
            logger.info("💻 正在生成Manim代码...")
            code = self.llm.generate_response(messages)
            
            # 清理代码 (移除可能的markdown标记)
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0]
            elif "```" in code:
                code = code.split("```")[1].split("```")[0]
            
            return code.strip()
        except Exception as e:
            log_exception(e, "代码生成失败")
            return self._get_fallback_code()
    
    def _get_fallback_scene_plan(self, user_input: str) -> str:
        """获取备用场景规划"""
        plans = {
            "牛顿第一定律": """
## 场景标题
牛顿第一定律 - 惯性原理演示

## 场景描述
通过动画展示牛顿第一定律：物体在不受外力或受到平衡力时保持静止或匀速直线运动状态。

## 具体元素
1. **背景设置**: 深蓝色背景，营造科学实验氛围
2. **主要对象**: 一个红色方块、地面、力的箭头、公式F=ma
3. **动画序列**: 
   - 显示标题和公式
   - 方块静止状态
   - 施加力后方块运动
   - 撤除力后方块继续运动
4. **重点强调**: 惯性概念和力与运动的关系

## 技术要求
- 使用箭头表示力的方向和大小
- 方块的运动要平滑自然
- 公式要清晰可见
- 动画节奏适中
            """,
            "圆周运动": """
## 场景标题
圆周运动与向心力

## 场景描述
展示物体做圆周运动时向心力的作用和运动轨迹。

## 具体元素
1. **背景设置**: 黑色背景配金色元素
2. **主要对象**: 圆形轨道、运动小球、向心力箭头、速度矢量
3. **动画序列**: 小球沿圆轨道运动，显示向心力和速度方向
4. **重点强调**: 向心力始终指向圆心，速度方向始终切线方向
            """
        }
        
        # 检查是否有匹配的预设方案
        for key in plans:
            if key in user_input:
                return plans[key]
        
        # 默认方案
        return f"""
## 场景标题
{user_input} - 数学物理动画

## 场景描述
基于 "{user_input}" 主题的教育动画，展示相关的数学或物理概念。

## 具体元素
1. **背景设置**: 简洁的深色背景
2. **主要对象**: 相关公式、几何图形、动画元素
3. **动画序列**: 循序渐进地展示概念
4. **重点强调**: 核心概念的可视化

## 技术要求
- 清晰的视觉表达
- 适当的动画节奏
- 教育性与趣味性并重
        """
    
    def _get_fallback_code(self) -> str:
        """获取备用Manim代码"""
        return '''from manim import *
import numpy as np

class NewtonFirstLaw(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1e1e2e"  # 深色背景
        
        # 标题 - 使用Text处理中文
        title = Text("牛顿第一定律 - 惯性原理", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 公式 - 使用MathTex处理数学公式
        formula = MathTex(r"F = ma")
        formula.scale(1.2)
        formula.to_edge(UP).shift(DOWN*0.8)
        self.play(Write(formula))
        self.wait(1)
        
        # 中文描述 - 使用Text
        description = Text(
            "物体在不受外力或受平衡力时\\n保持静止或匀速直线运动状态",
            font_size=24,
            color=BLUE
        )
        description.next_to(formula, DOWN)
        self.play(FadeIn(description))
        self.wait(2)
        self.play(FadeOut(description))
        
        # 地面
        ground = Line(LEFT * 6, RIGHT * 6, color=WHITE)
        ground.shift(DOWN * 2)
        self.play(Create(ground))
        
        # 方块
        box = Square(side_length=0.8, color=RED, fill_opacity=0.7)
        box.shift(LEFT * 3 + DOWN * 1.6)
        self.play(Create(box))
        self.wait(1)
        
        # 静止状态说明 - 使用Text
        rest_text = Text("物体处于静止状态", font_size=24, color=GREEN)
        rest_text.shift(UP * 0.5)
        self.play(Write(rest_text))
        self.wait(2)
        
        # 施加力
        force_arrow = Arrow(
            start=box.get_right() + RIGHT * 0.5, 
            end=box.get_right() + RIGHT * 1.5, 
            color=YELLOW,
            buff=0
        )
        force_label = Text("施加力 F", font_size=20, color=YELLOW)
        force_label.next_to(force_arrow, UP)
        
        self.play(
            FadeOut(rest_text),
            Create(force_arrow),
            Write(force_label)
        )
        
        # 方块运动
        self.play(
            box.animate.shift(RIGHT * 4),
            force_arrow.animate.shift(RIGHT * 4),
            force_label.animate.shift(RIGHT * 4),
            run_time=2
        )
        
        # 撤除力后继续运动 - 使用Text
        motion_text = Text("撤除力后，物体保持匀速运动", font_size=24, color=PURPLE)
        motion_text.shift(UP * 0.5)
        
        self.play(
            FadeOut(force_arrow),
            FadeOut(force_label),
            Write(motion_text)
        )
        
        self.play(
            box.animate.shift(RIGHT * 2),
            run_time=2,
            rate_func=linear
        )
        
        # 结论 - 使用Text
        conclusion = Text("这就是牛顿第一定律 - 惯性原理", font_size=28, color=GREEN)
        conclusion.shift(DOWN * 3)
        self.play(Write(conclusion))
        self.wait(3)
        
        # 最终公式
        final_formula = MathTex(r"\\sum F = 0 \\Rightarrow \\Delta v = 0")
        final_formula.shift(DOWN * 1)
        self.play(Write(final_formula))
        self.wait(2)
        
        # 淡出所有元素
        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(1)'''
    
    def save_and_render(self, code: str, scene_name: str, user_input: str) -> tuple[str, str]:
        """保存代码并渲染视频"""
        try:
            # 创建唯一的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_input = "".join(c for c in user_input if c.isalnum() or c in "_ ")[:20]
            
            code_filename = f"{safe_input}_{timestamp}.py"
            code_path = self.output_dir / code_filename
            
            # 保存代码文件
            logger.info(f"💾 Saving code to: {code_path}")
            with open(code_path, 'w', encoding='utf-8') as f:
                f.write(code)
            logger.debug(f"📝 Code saved successfully ({len(code)} bytes)")
            
            # 渲染视频
            logger.info("🎥 Starting video rendering...")
            
            # 构建渲染命令
            quality = self.manim_settings["quality"]
            
            if "quality_options" in self.manim_settings:
                quality_config = self.manim_settings["quality_options"].get(quality, {})
                quality_flag = quality_config.get("flag", "-qm")
                logger.info(f"⚙️ Using quality settings: {quality}")
                logger.debug(f"📊 Quality config: {quality_config}")
            else:
                quality_flag = {
                    "low": "-ql",
                    "medium": "-qm", 
                    "high": "-qh"
                }.get(quality, "-qm")
                logger.info(f"⚙️ Using quality settings: {quality} (legacy mode)")
            
            preview_flag = "-p" if self.manim_settings["preview"] else ""
            
            # 使用绝对路径
            cmd = [
                self.python_path, "-m", "manim",
                quality_flag,
                preview_flag,
                str(code_path.absolute()),
                scene_name
            ]
            
            # 过滤空字符串
            cmd = [arg for arg in cmd if arg]
            logger.debug(f"🔧 Rendering command: {' '.join(cmd)}")
            
            # 执行渲染
            logger.info("⚙️ Executing Manim render...")
            start_time = datetime.now()
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.output_dir.absolute())
            )
            
            render_time = (datetime.now() - start_time).total_seconds()
            
            if result.returncode == 0:
                logger.info(f"✅ Video rendered successfully in {render_time:.1f} seconds")
                logger.debug(f"📝 Render output:\n{result.stdout}")
                
                # 查找生成的视频文件
                video_path = self._find_video_file(code_path.stem, scene_name)
                if video_path:
                    logger.info(f"📁 Found video file: {video_path}")
                    return str(code_path), video_path
                else:
                    logger.error("❌ Could not find generated video file")
                    return str(code_path), ""
            else:
                logger.error(f"❌ Render failed with code {result.returncode}")
                logger.error(f"❌ Error output:\n{result.stderr}")
                return str(code_path), ""
                
        except Exception as e:
            logger.error(f"❌ Render error: {str(e)}")
            log_exception(e, "Video render error")
            return str(code_path), ""
    
    def _find_video_file(self, script_name: str, scene_name: str) -> str:
        """查找生成的视频文件"""
        logger.debug(f"🔍 Searching for video file: {script_name}/{scene_name}")
        
        # Manim默认输出路径模式
        possible_paths = [
            self.output_dir / "media" / "videos" / script_name / "1080p60" / f"{scene_name}.mp4",
            self.output_dir / "media" / "videos" / script_name / "720p30" / f"{scene_name}.mp4",
            self.output_dir / "media" / "videos" / script_name / "480p15" / f"{scene_name}.mp4",
        ]
        
        for path in possible_paths:
            if path.exists():
                logger.info(f"✅ Found video at: {path}")
                return str(path)
        
        logger.error("❌ Video file not found in any expected location")
        return "视频文件未找到"
    
    def generate_video(self, user_input: str) -> Dict[str, str]:
        """主函数：根据用户输入生成视频"""
        logger.info(f"🎬 Starting video generation for input: '{user_input[:50]}...'")
        logger.debug(f"📝 Full input text: {user_input}")
        
        try:
            # 1. 生成场景规划
            logger.info("📋 Generating scene plan...")
            scene_plan = self.generate_scene_plan(user_input)
            logger.debug(f"📋 Scene plan generated:\n{scene_plan}")
            logger.info("✅ Scene planning completed")
            
            # 2. 生成Manim代码
            logger.info("💻 Generating Manim code...")
            code = self.generate_manim_code(scene_plan)
            logger.debug(f"💻 Generated code:\n{code}")
            logger.info("✅ Code generation completed")
            
            # 3. 提取类名
            scene_name = self._extract_class_name(code)
            logger.info(f"🔍 Extracted scene name: {scene_name}")
            
            # 4. 保存并渲染
            logger.info("🎥 Starting video rendering...")
            code_path, video_path = self.save_and_render(code, scene_name, user_input)
            
            if video_path and Path(video_path).exists():
                video_size = Path(video_path).stat().st_size
                logger.info(f"✅ Video rendered successfully (size: {video_size:,} bytes)")
                logger.debug(f"📁 Video saved at: {video_path}")
            else:
                logger.error("❌ Video rendering failed - no output file")
            
            return {
                "user_input": user_input,
                "scene_plan": scene_plan,
                "code": code,
                "code_path": code_path,
                "video_path": video_path,
                "scene_name": scene_name
            }
            
        except Exception as e:
            logger.error(f"❌ Video generation failed: {str(e)}")
            log_exception(e, "Video generation error")
            raise
    
    def _extract_class_name(self, code: str) -> str:
        """从代码中提取类名"""
        lines = code.split('\n')
        for line in lines:
            if 'class ' in line and '(Scene)' in line:
                # 提取类名
                class_line = line.strip()
                class_name = class_line.split('class ')[1].split('(')[0]
                return class_name
        
        return "GeneratedScene"
    
    def list_available_models(self) -> Dict[str, Dict]:
        """列出所有可用的模型"""
        return CONFIG["models"]
    
    def switch_model(self, model_name: str) -> bool:
        """切换到指定的模型"""
        if model_name not in CONFIG["models"]:
            print(f"❌ 模型 '{model_name}' 不存在")
            print("可用模型:", list(CONFIG["models"].keys()))
            print("可用模型:", list(MODEL_CONFIGS.keys()))
            return False
        
        self.model_key = model_name
        print(f"🔄 正在切换到模型: {model_name}")
        
        # 重新初始化LLM
        self.llm = self._initialize_llm()
        return True


def main():
    """主函数"""
    print("🎥 AI Manim视频生成器")
    print("=" * 30)
    
    # 初始化生成器
    generator = AIVideoGenerator()
    
    # 获取用户输入
    print("\n💡 请输入您想要生成的动画主题:")
    print("例如: '牛顿第一定律', '圆周运动', '三角函数', '导数的几何意义' 等")
    user_input = input("\n📝 输入主题: ").strip()
    
    if not user_input:
        print("❌ 输入不能为空")
        return
    
    # 生成视频
    try:
        result = generator.generate_video(user_input)
        
        print("\n" + "=" * 50)
        print("🎉 生成完成！")
        print(f"📁 代码文件: {result['code_path']}")
        print(f"🎬 视频文件: {result['video_path']}")
        print(f"🎭 场景类名: {result['scene_name']}")
        
        # 保存结果报告
        report_path = Path(generator.output_dir) / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"AI Manim 视频生成报告\n")
            f.write(f"生成时间: {datetime.now()}\n")
            f.write(f"用户输入: {result['user_input']}\n\n")
            f.write(f"场景规划:\n{result['scene_plan']}\n\n")
            f.write(f"生成代码:\n{result['code']}\n")
        
        print(f"📊 详细报告: {report_path}")
        
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    main() 