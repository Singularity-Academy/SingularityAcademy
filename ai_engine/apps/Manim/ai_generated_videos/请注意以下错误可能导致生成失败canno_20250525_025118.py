from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 定义颜色和背景
        BACKGROUND_COLOR = "#0E1A40"  # 深蓝色背景
        GROUND_COLOR = "#C0C0C0"  # 浅灰色地面
        GRID_COLOR = "#A0A0A0"  # 网格颜色
        FORCE_COLOR = RED  # 作用力箭头颜色
        REACTION_COLOR = GREEN  # 反作用力箭头颜色
        TEXT_COLOR = WHITE  # 文字颜色

        # 设置背景
        self.camera.background_color = BACKGROUND_COLOR

        # 创建地面
        ground = Rectangle(width=FRAME_WIDTH, height=0.3, color=GROUND_COLOR, fill_opacity=1)
        ground.to_edge(DOWN)
        grid = NumberPlane(
            x_range=[-FRAME_WIDTH / 2, FRAME_WIDTH / 2, 1],
            y_range=[-FRAME_HEIGHT / 2, FRAME_HEIGHT / 2, 1],
            background_line_style={"stroke_color": GRID_COLOR, "stroke_width": 1},
        )
        self.add(grid, ground)

        # 第一阶段：标题和静止物体
        title = Text("力的对话：揭示牛顿第三定律的奥秘", font_size=36, color=TEXT_COLOR)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建方块和球
        block = Square(side_length=1, color=YELLOW, fill_opacity=0.7).move_to(LEFT * 2)
        ball = Circle(radius=0.5, color=BLUE, fill_opacity=0.7).move_to(RIGHT * 2)
        label_a = Text("A", font_size=24, color=BLACK).move_to(block.get_center())
        label_b = Text("B", font_size=24, color=WHITE).move_to(ball.get_center())
        self.play(FadeIn(block), FadeIn(ball), Write(label_a), Write(label_b))
        self.wait(1)

        intro_text = Text("牛顿第三定律：作用力与反作用力总是大小相等、方向相反", font_size=24, color=TEXT_COLOR)
        intro_text.to_edge(DOWN)
        self.play(Write(intro_text))
        self.wait(2)

        # 第二阶段：球向方块移动并碰撞
        self.play(ball.animate.shift(LEFT * 3), run_time=2)
        self.wait(0.5)

        # 碰撞瞬间：展示作用力和反作用力
        force_arrow = Arrow(ball.get_center(), block.get_center(), color=FORCE_COLOR, buff=0.1, stroke_width=4)
        reaction_arrow = Arrow(block.get_center(), ball.get_center(), color=REACTION_COLOR, buff=0.1, stroke_width=4)
        force_text = Text("作用力", font_size=24, color=FORCE_COLOR).next_to(force_arrow, UP)
        reaction_text = Text("反作用力", font_size=24, color=REACTION_COLOR).next_to(reaction_arrow, UP)
        self.play(Create(force_arrow), Write(force_text))
        self.play(Create(reaction_arrow), Write(reaction_text))
        self.wait(1)

        # 第三阶段：动态公式框和关键词强调
        formula = MathTex(r"F_{\text{AB}} = -F_{\text{BA}}", font_size=36)
        formula.move_to(UP * 2)
        self.play(Write(formula))
        highlight_text = Text("大小相等，方向相反", font_size=30, color=YELLOW)
        highlight_text.next_to(formula, DOWN)
        self.play(Write(highlight_text))
        self.wait(2)

        # 第四阶段：物体分离并运动
        self.play(
            ball.animate.shift(RIGHT * 2),
            block.animate.shift(LEFT * 1),
            run_time=2
        )
        self.wait(1)

        # 第五阶段：总结文字
        summary_text = Text("牛顿第三定律告诉我们，力总是成对出现，交互中的每一方同时施加力并受到力。", font_size=24, color=TEXT_COLOR)
        summary_text.to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(3)

        # 场景渐暗
        self.play(FadeOut(VGroup(*self.mobjects)))