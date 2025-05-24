from manim import *
import numpy as np

class NewtonSecondLawScene(Scene):
    def construct(self):
        # 场景标题
        title = Text("牛顿第二定律", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=LIGHT_GREY, fill_opacity=1)
        ground_line = Line(start=LEFT * FRAME_WIDTH / 2, end=RIGHT * FRAME_WIDTH / 2, color=DARK_GREY).shift(DOWN * 2)
        self.add(background, ground_line)

        # 主要对象：立方体
        cube = Square(side_length=1, color=ORANGE, fill_opacity=0.8).move_to(LEFT * 3 + DOWN * 1.5)
        force_arrow = Arrow(start=cube.get_left(), end=cube.get_left() + RIGHT * 1, color=RED, stroke_width=6)
        self.add(cube)

        # 公式标签
        formula = MathTex(r"a = \frac{F}{m}", font_size=48, color=GREEN).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1)

        # 动态调整力和质量滑块
        force_label = Text("力 F", font_size=24, color=RED).move_to(UP * 3 + LEFT * 3.5)
        mass_label = Text("质量 m", font_size=24, color=BLUE).move_to(UP * 3 + RIGHT * 3.5)
        force_slider = Line(start=LEFT, end=RIGHT, color=RED).scale(2).next_to(force_label, DOWN, buff=0.5)
        mass_slider = Line(start=LEFT, end=RIGHT, color=BLUE).scale(2).next_to(mass_label, DOWN, buff=0.5)
        self.add(force_label, mass_label, force_slider, mass_slider)

        # 力与质量动态演示
        for f, m in [(1, 1), (2, 1), (2, 2), (3, 2)]:
            # 更新箭头长度
            new_arrow = Arrow(start=cube.get_left(), end=cube.get_left() + RIGHT * f, color=RED, stroke_width=6)
            self.play(Transform(force_arrow, new_arrow))

            # 更新立方体加速度
            acceleration_text = Text(f"a = {f/m:.2f}", font_size=24, color=GREEN).next_to(formula, UP)
            self.play(Write(acceleration_text))

            # 立方体运动
            self.play(cube.animate.shift(RIGHT * (f/m)), run_time=2)
            self.wait(1)

            # 更新滑块显示
            self.play(FadeOut(acceleration_text))

        # 轨迹变化
        trajectory = Line(start=LEFT * 3 + DOWN * 1.5, end=cube.get_center(), color=BLUE, stroke_width=2, dash_length=0.2)
        self.play(Create(trajectory))
        self.wait(1)

        # 结尾
        conclusion = Text("牛顿第二定律解释了力与运动的关系", font_size=32, color=WHITE).to_edge(DOWN)
        self.play(FadeIn(conclusion))
        self.wait(2)

        # 清除场景
        self.play(FadeOut(VGroup(*self.mobjects)))