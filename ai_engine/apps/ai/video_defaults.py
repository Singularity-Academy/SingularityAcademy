"""
Default values and templates for video generation.

This module contains default values, templates, and fallback content
used by the video generation system.
"""

from typing import Dict

# Default scene plans for common topics
DEFAULT_SCENE_PLANS: Dict[str, str] = {
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

# Default scene plan template for unknown topics
DEFAULT_SCENE_PLAN_TEMPLATE = """
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

# Default Manim code template for fallback
DEFAULT_MANIM_CODE = '''from manim import *
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

# Prompt templates for LLM interactions
SCENE_PLAN_PROMPT = """
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

CODE_GENERATION_PROMPT = """
根据以下场景规划，生成完整的Manim代码。

场景规划:
{scene_plan}

请生成一个完整的Manim Scene类，严格遵循以下要求：
请为每个环境变量赋值
⚠️你生成的Python代码将直接被封装执行，无任何已知变量。请务必在调用变量前为其赋值，例如WIDTH, HEIGHT, LIGHT_BLUE, YELLOW等，都会触发NOT DEFINED错误。
提示：当该页面满了后你可以擦除内容并新起一页。请注意背景和文字颜色的对比和重叠。 设备暂时无联网权限，且本地无图像和 svg 文件。请勿尝试加载网络资源或本地文件。
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
- 必须导入: `from manim import *`
- 如果使用随机数: `import numpy as np` 然后用 `np.random.random()`
- 不要使用 `import random`，应该使用numpy
- 中文文字：`Text("中文内容", font_size=32, color=WHITE)`
- 数学公式：`MathTex(r"E = mc^2")`
- 绝对不要用Tex()处理中文

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

请直接输出Python代码，不要包含其他说明。
""" 