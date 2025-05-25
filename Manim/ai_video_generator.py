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
from typing import Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class AIVideoGenerator:
    def __init__(self, config_path: str = "config.json", selected_model: str = None):
        """初始化AI视频生成器"""
        self.config = self._load_config(config_path)
        
        # 如果指定了模型，覆盖默认设置
        if selected_model and "models" in self.config:
            if selected_model in self.config["models"]:
                self.config["default_model"] = selected_model
                print(f"🔄 切换到指定模型: {selected_model}")
            else:
                print(f"⚠️  指定的模型 '{selected_model}' 不存在，使用默认模型")
        
        self.llm = self._initialize_llm()
        self.output_dir = Path(self.config["output_settings"]["output_dir"])
        self.output_dir.mkdir(exist_ok=True)
        
        # Python路径 (从之前的安装中获得)
        self.python_path = "python3"
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查新格式的配置结构
            if "models" in config:
                default_model = config.get("default_model", "gpt-4")
                if default_model in config["models"]:
                    model_config = config["models"][default_model]
                    api_key = model_config.get("api_key", "")
                    
                    if not api_key or api_key == "YOUR_API_KEY_HERE":
                        print("⚠️  请在config.json中设置您的API密钥")
                        print("如果您没有API密钥，程序将使用预设的示例场景")
                    else:
                        print(f"✅ 已加载模型配置: {model_config['name']}")
                        print(f"   📋 描述: {model_config['description']}")
                else:
                    print(f"❌ 默认模型 '{default_model}' 在配置中未找到")
            else:
                # 兼容旧格式
                print("⚠️  检测到旧版配置格式，建议更新到新格式")
            
            return config
        except FileNotFoundError:
            print(f"❌ 配置文件 {config_path} 未找到")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ 配置文件 {config_path} 格式错误")
            sys.exit(1)
    
    def _initialize_llm(self) -> Optional[ChatOpenAI]:
        """初始化语言模型"""
        # 支持新的配置格式
        if "models" in self.config:
            default_model = self.config.get("default_model", "gpt-o4-mini")
            if default_model not in self.config["models"]:
                print(f"❌ 默认模型 '{default_model}' 配置未找到，切换到离线模式")
                return None
            
            model_config = self.config["models"][default_model]
            api_key = model_config.get("api_key", "")
            
            if not api_key or api_key in ["YOUR_API_KEY_HERE", "YOUR_OPENAI_API_KEY_HERE"]:
                print("🤖 使用离线模式 - 将使用预设的物理定律演示")
                return None
            
            try:
                # 设置环境变量
                os.environ["OPENAI_API_KEY"] = api_key
                
                # 创建LLM实例，支持自定义base_url
                llm_kwargs = {
                    "model": model_config["model_id"],
                    "temperature": model_config.get("temperature", 0.7),
                    "max_tokens": model_config.get("max_tokens", 2000)
                }
                
                # 如果有自定义的API base URL
                if "api_base" in model_config and model_config["api_base"]:
                    llm_kwargs["base_url"] = model_config["api_base"]
                
                llm = ChatOpenAI(**llm_kwargs)
                
                print(f"✅ {model_config['name']} 初始化成功")
                print(f"   🔗 API Base: {model_config.get('api_base', 'default')}")
                print(f"   🌡️  Temperature: {model_config.get('temperature', 0.7)}")
                print(f"   📊 Max Tokens: {model_config.get('max_tokens', 2000)}")
                return llm
            except Exception as e:
                print(f"❌ LLM初始化失败: {e}")
                print("🤖 切换到离线模式")
                return None
        else:
            # 兼容旧格式
            api_key = self.config.get("api_keys", {}).get("openai_api_key", "")
            
            if api_key == "YOUR_OPENAI_API_KEY_HERE":
                print("🤖 使用离线模式 - 将使用预设的物理定律演示")
                return None
            
            try:
                os.environ["OPENAI_API_KEY"] = api_key
                
                llm_settings = self.config.get("llm_settings", {})
                llm = ChatOpenAI(
                    model=llm_settings.get("model", "gpt-3.5-turbo"),
                    temperature=llm_settings.get("temperature", 0.7),
                    max_tokens=llm_settings.get("max_tokens", 2000)
                )
                
                print("✅ OpenAI LLM 初始化成功 (兼容模式)")
                return llm
            except Exception as e:
                print(f"❌ LLM初始化失败: {e}")
                print("🤖 切换到离线模式")
                return None
    
    def _create_scene_prompt(self) -> ChatPromptTemplate:
        """创建场景规划提示词模板"""
        template = """
请直接输出完整的 Python 代码。 你输出的 Python 代码将直接被执行。若需用户决定的变量，例如FRAME_WIDTH等，直接帮用户决策，使用默认值即可。当前目录下无图标文件。无法获取 URL 资源。
你是一个专业的数学和物理教育动画设计师。请根据用户的输入，设计一个生动的Manim动画场景。

用户输入: {user_input}

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

请确保场景设计既有教育价值又具有视觉吸引力。
"""
        return ChatPromptTemplate.from_template(template)
    
    def _create_code_prompt(self) -> ChatPromptTemplate:
        """创建代码生成提示词模板 - 包含完整的Manim语法参考"""
        template = """
根据以下场景规划，生成完整的Manim代码。

场景规划:
{scene_plan}

请生成一个完整的Manim Scene类，严格遵循以下要求：
请为每个环境变量赋值
⚠️你生成的Python代码将直接被封装执行，无任何已知变量。请务必在调用变量前为其赋值，例如WIDTH, HEIGHT, LIGHT_BLUE, YELLOW等，都会触发NOT DEFINED错误。
对于颜色，永远使用#xxxxxx 格式，不得使用 RED YELLOW 等格式。
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
- 圆形：`Circle(radius=1, color=#00FF00, fill_opacity=0.5)`
- 方形：`Square(side_length=1, color=#FF0000)`
- 矩形：`Rectangle(width=2, height=1, color=#00FF00)`
- 直线：`Line(start=LEFT, end=RIGHT, color=#FFFFFF)`
- 箭头：`Arrow(start=ORIGIN, end=UP, color=#FFFF00)`
- 点：`Dot(point=ORIGIN, color=#FF0000)`

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

## 4. 完整示例模板
```python
from manim import *
import numpy as np

class ExampleScene(Scene):
    def construct(self):
        # 标题
        title = Text("示例动画", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 几何对象
        circle = Circle(radius=1, color=BLUE, fill_opacity=0.3)
        square = Square(side_length=1.5, color=RED)
        
        # 位置
        circle.shift(LEFT*2)
        square.shift(RIGHT*2)
        
        # 动画
        self.play(Create(circle), Create(square))
        self.wait(1)
        
        # 公式
        formula = MathTex(r"x^2 + y^2 = r^2")
        formula.shift(DOWN*2)
        self.play(Write(formula))
        self.wait(1)
        
        # 移动动画
        self.play(
            circle.animate.shift(RIGHT*1),
            square.animate.shift(LEFT*1),
            run_time=2
        )
        self.wait(1)
        
        # 结束
        self.play(FadeOut(VGroup(*self.mobjects)))
```

## 5. 你的任务
根据场景规划生成完整可运行的代码，确保：
- 导入正确的模块
- 中文用Text()，公式用MathTex()
- 使用正确的API调用
- 不使用不存在的方法
- 代码语法完全正确

请直接输出Python代码，不要包含其他说明。
"""
        return ChatPromptTemplate.from_template(template)
    
    def generate_scene_plan(self, user_input: str) -> str:
        """生成场景规划"""
        if self.llm is None:
            return self._get_fallback_scene_plan(user_input)
        
        try:
            prompt = self._create_scene_prompt()
            chain = prompt | self.llm | StrOutputParser()
            
            print("🎯 正在规划场景...")
            scene_plan = chain.invoke({"user_input": user_input})
            return scene_plan
        except Exception as e:
            print(f"❌ 场景规划失败: {e}")
            return self._get_fallback_scene_plan(user_input)
    
    def generate_manim_code(self, scene_plan: str) -> str:
        """根据场景规划生成Manim代码"""
        if self.llm is None:
            return self._get_fallback_code()
        
        try:
            prompt = self._create_code_prompt()
            chain = prompt | self.llm | StrOutputParser()
            
            print("💻 正在生成Manim代码...")
            code = chain.invoke({"scene_plan": scene_plan})
            
            # 清理代码 (移除可能的markdown标记)
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0]
            elif "```" in code:
                code = code.split("```")[1].split("```")[0]
            
            return code.strip()
        except Exception as e:
            print(f"❌ 代码生成失败: {e}")
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
        # 创建唯一的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_input = "".join(c for c in user_input if c.isalnum() or c in "_ ")[:20]
        
        code_filename = f"{safe_input}_{timestamp}.py"
        code_path = self.output_dir / code_filename
        
        # 保存代码文件
        with open(code_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"💾 代码已保存到: {code_path}")
        
        # 渲染视频
        try:
            print("🎬 开始渲染视频...")
            
            # 构建渲染命令 - 支持新的质量配置格式
            quality = self.config["manim_settings"]["quality"]
            
            if "quality_options" in self.config["manim_settings"]:
                # 使用新的质量配置格式
                quality_config = self.config["manim_settings"]["quality_options"].get(quality, {})
                quality_flag = quality_config.get("flag", "-qm")
                print(f"📊 使用质量设置: {quality} ({quality_config.get('description', 'No description')})")
                print(f"   🎥 分辨率: {quality_config.get('resolution', 'Unknown')}")
                print(f"   ⏱️  帧率: {quality_config.get('frame_rate', 'Unknown')} FPS")
            else:
                # 兼容旧格式
                quality_flag = {
                    "low": "-ql",
                    "medium": "-qm", 
                    "high": "-qh"
                }.get(quality, "-qm")
                print(f"📊 使用质量设置: {quality} (兼容模式)")
            
            preview_flag = "-p" if self.config["manim_settings"]["preview"] else ""
            
            # 使用绝对路径
            cmd = [
                self.python_path, "-m", "manim",
                quality_flag,
                preview_flag,
                str(code_path.absolute()),  # 使用绝对路径
                scene_name
            ]
            
            # 过滤空字符串
            cmd = [arg for arg in cmd if arg]
            
            # 执行渲染，设置正确的工作目录
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.output_dir.absolute())  # 使用绝对路径
            )
            
            if result.returncode == 0:
                print("✅ 视频渲染成功！")
                
                # 查找生成的视频文件
                video_path = self._find_video_file(code_path.stem, scene_name)
                return str(code_path), video_path
            else:
                print(f"❌ 渲染失败: {result.stderr}")
                return str(code_path), result.stderr.strip()
                
        except Exception as e:
            print(f"❌ 渲染异常: {e}")
            return str(code_path), e
    
    def _find_video_file(self, script_name: str, scene_name: str) -> str:
        """查找生成的视频文件"""
        # Manim默认输出路径模式
        possible_paths = [
            self.output_dir / "media" / "videos" / script_name / "1080p60" / f"{scene_name}.mp4",
            self.output_dir / "media" / "videos" / script_name / "720p30" / f"{scene_name}.mp4",
            self.output_dir / "media" / "videos" / script_name / "480p15" / f"{scene_name}.mp4",
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        return "视频文件未找到"
    
    def generate_video(self, user_input: str) -> Dict[str, str]:
        """主函数：根据用户输入生成视频"""
        try:
            print(f"\n🚀 开始处理输入: '{user_input}'")
            print("=" * 50)
            
            # 1. 生成场景规划
            scene_plan = self.generate_scene_plan(user_input)
            print("📋 场景规划完成")
            
            # 2. 生成Manim代码
            code = self.generate_manim_code(scene_plan)
            print("💻 代码生成完成")
            
            # 3. 提取类名
            scene_name = self._extract_class_name(code)
            
            # 4. 保存并渲染
            code_path, video_path = self.save_and_render(code, scene_name, user_input)
            
            return {
                "user_input": user_input,
                "scene_plan": scene_plan,
                "code": code,
                "code_path": code_path,
                "video_path": video_path,
                "scene_name": scene_name
            }
        except:
            return {
                "ERR":str(video_path),
            }
    
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
        if "models" in self.config:
            return self.config["models"]
        return {}
    
    def switch_model(self, model_name: str) -> bool:
        """切换到指定的模型"""
        if "models" not in self.config:
            print("❌ 配置中没有模型定义")
            return False
        
        if model_name not in self.config["models"]:
            print(f"❌ 模型 '{model_name}' 不存在")
            print("可用模型:", list(self.config["models"].keys()))
            return False
        
        self.config["default_model"] = model_name
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