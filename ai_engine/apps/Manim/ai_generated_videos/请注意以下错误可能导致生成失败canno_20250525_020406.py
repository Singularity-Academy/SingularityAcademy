from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color="#87CEFA", fill_opacity=1).move_to(ORIGIN)
        self.add(background)

        # 定律公式
        formula = MathTex(r"F_1 = -F_2", font_size=48, color=WHITE)
        formula.to_corner(UR)
        self.play(FadeIn(formula), run_time=2)

        # 地面
        ground = Line(start=LEFT*6, end=RIGHT*6, color=GRAY, stroke_width=4).shift(DOWN*2)
        self.play(Create(ground))

        # 方块 A 和 B
        block_a = Square(side_length=1, color=RED, fill_color=RED, fill_opacity=0.8).shift(LEFT*3 + DOWN*1.5)
        block_b = Square(side_length=1, color=BLUE, fill_color=BLUE, fill_opacity=0.8).shift(RIGHT*3 + DOWN*1.5)
        self.play(FadeIn(block_a), FadeIn(block_b))

        # 第一阶段：静止展示
        self.wait(2)

        # 第二阶段：作用力与反作用力可视化
        arrow_a_to_b = Arrow(start=block_a.get_center(), end=block_b.get_center(), color=RED, buff=0.5, stroke_width=5)
        label_a = Text("作用力 F₁", font_size=24, color=RED).next_to(arrow_a_to_b, UP)
        self.play(Create(arrow_a_to_b), Write(label_a))

        arrow_b_to_a = Arrow(start=block_b.get_center(), end=block_a.get_center(), color=BLUE, buff=0.5, stroke_width=5)
        label_b = Text("反作用力 F₂", font_size=24, color=BLUE).next_to(arrow_b_to_a, DOWN)
        self.play(Create(arrow_b_to_a), Write(label_b))

        # 第三阶段：力的平衡与方向关系
        dynamic_text = Text("作用力与反作用力大小相等，方向相反", font_size=28, color=YELLOW).to_edge(UP)
        self.play(Write(dynamic_text))
        self.wait(1)

        # 动态箭头变化
        self.play(
            arrow_a_to_b.animate.scale(1.5),
            arrow_b_to_a.animate.scale(1.5),
            run_time=2
        )

        # 方块运动
        self.play(
            block_b.animate.shift(RIGHT*2),
            block_a.animate.shift(LEFT*1),
            run_time=2
        )
        self.wait(1)

        # 第四阶段：总结与回顾
        self.play(FadeOut(dynamic_text), FadeOut(arrow_a_to_b), FadeOut(arrow_b_to_a), FadeOut(label_a), FadeOut(label_b))
        summary_formula = MathTex(r"F_1 = -F_2", font_size=72, color=WHITE).move_to(ORIGIN)
        summary_text = Text("牛顿第三定律：作用力与反作用力大小相等，方向相反", font_size=28, color=WHITE).next_to(summary_formula, DOWN)
        self.play(Transform(formula, summary_formula), Write(summary_text))
        self.wait(2)

        # 淡出所有元素
        self.play(FadeOut(VGroup(*self.mobjects)))