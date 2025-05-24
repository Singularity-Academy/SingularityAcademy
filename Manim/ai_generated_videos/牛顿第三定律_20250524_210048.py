from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#1E1E90"  # 深蓝色背景
        ground = Line(start=LEFT*6, end=RIGHT*6, color=WHITE)
        ground.shift(DOWN*2)
        self.play(Create(ground))

        # 标题和公式
        title = Text("牛顿第三定律：作用与反作用的完美平衡", font_size=36, color=WHITE)
        title.to_edge(UP)
        formula = MathTex(r"\vec{F}_{A \to B} = -\vec{F}_{B \to A}", font_size=36)
        formula.next_to(title, DOWN)
        self.play(Write(title), FadeIn(formula, run_time=2))
        self.wait(1)

        # 创建物体A（蓝色方块）和物体B（红色球）
        block = Square(side_length=1, color=BLUE, fill_opacity=0.6)
        block.shift(LEFT*3 + DOWN*1.5)
        ball = Circle(radius=0.5, color=RED, fill_opacity=0.6)
        ball.shift(RIGHT*3 + DOWN*1.5)
        self.play(FadeIn(block), FadeIn(ball))
        self.wait(1)

        # 动画：方块向右移动，碰撞到球
        self.play(block.animate.shift(RIGHT*3), run_time=2)
        self.wait(0.5)

        # 显示作用力和反作用力
        action_arrow = Arrow(start=block.get_center(), end=ball.get_center(), color=GREEN, buff=0.1)
        reaction_arrow = Arrow(start=ball.get_center(), end=block.get_center(), color=YELLOW, buff=0.1)
        action_label = Text("作用力", font_size=24, color=GREEN)
        reaction_label = Text("反作用力", font_size=24, color=YELLOW)
        action_label.next_to(action_arrow, UP)
        reaction_label.next_to(reaction_arrow, UP)

        self.play(Create(action_arrow), Write(action_label), run_time=1)
        self.play(Create(reaction_arrow), Write(reaction_label), run_time=1)
        self.wait(1)

        # 箭头动态伸展，显示两力大小相等
        self.play(
            action_arrow.animate.scale(1.5, about_point=block.get_center()),
            reaction_arrow.animate.scale(1.5, about_point=ball.get_center()),
            run_time=1.5
        )
        self.wait(1)

        # 强调公式和闪烁效果
        self.play(Indicate(formula, color=YELLOW, scale_factor=1.2), run_time=1.5)
        explanation = Text("作用力和反作用力大小相等，方向相反", font_size=28, color=WHITE)
        explanation.next_to(formula, DOWN)
        self.play(Write(explanation), run_time=2)
        self.wait(1.5)

        # 动画：物体分别向不同方向运动
        self.play(
            block.animate.shift(LEFT*2),
            ball.animate.shift(RIGHT*2),
            run_time=2
        )
        self.wait(1)

        # 结束场景：公式保持高亮，逐渐淡出
        self.play(FadeOut(VGroup(block, ball, action_arrow, reaction_arrow, action_label, reaction_label, explanation)))
        self.play(FadeOut(formula), FadeOut(title), FadeOut(ground))
        self.wait(1)