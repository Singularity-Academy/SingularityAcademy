from manim import *
import numpy as np

class FunnyPhysics(Scene):
    def construct(self):
        # 设置背景
        background = Rectangle(width=14, height=8, color=BLUE, fill_opacity=1)
        grass = Rectangle(width=14, height=3, color=GREEN, fill_opacity=1)
        grass.shift(DOWN * 2.5)
        sun = Circle(radius=0.7, color=YELLOW, fill_opacity=1)
        sun.shift(UP * 3 + LEFT * 5)
        cloud1 = Ellipse(width=2, height=1, color=WHITE, fill_opacity=1)
        cloud2 = Ellipse(width=1.5, height=0.8, color=WHITE, fill_opacity=1)
        cloud1.shift(UP * 2.5 + RIGHT * 3)
        cloud2.shift(UP * 2 + RIGHT * 4.5)
        self.add(background, grass, sun, cloud1, cloud2)

        # 斜面和主角💩
        incline = Polygon(
            ORIGIN, RIGHT * 5, RIGHT * 5 + UP * 3,
            color=ORANGE, fill_opacity=0.5
        )
        incline.shift(DOWN * 1.5)
        poop = SVGMobject("💩").scale(0.5)
        poop.move_to(RIGHT * 5 + UP * 1.5)

        # 添加斜面和💩
        self.play(Create(incline), FadeIn(poop))
        self.wait(1)

        # 💩眨眼动画
        poop.scale(1.2)
        self.play(poop.animate.scale(1/1.2), run_time=0.5)
        self.wait(1)

        # 力的分解
        gravity_arrow = Arrow(
            start=poop.get_center(), end=poop.get_center() + DOWN * 2, 
            color=BLUE
        )
        gravity_label = Text("g = 9.8 m/s²", font_size=24, color=BLUE)
        gravity_label.next_to(gravity_arrow, DOWN)

        self.play(Create(gravity_arrow), Write(gravity_label))
        self.wait(1)

        normal_force_arrow = Arrow(
            start=poop.get_center(), end=poop.get_center() + UP * 1 + LEFT * 1,
            color=GREEN
        )
        normal_label = Text("法向力", font_size=24, color=GREEN)
        normal_label.next_to(normal_force_arrow, UP)

        self.play(Create(normal_force_arrow), Write(normal_label))
        self.wait(1)

        parallel_force_arrow = Arrow(
            start=poop.get_center(), end=poop.get_center() + RIGHT * 2 + DOWN * 1,
            color=YELLOW
        )
        parallel_label = Text("分力", font_size=24, color=YELLOW)
        parallel_label.next_to(parallel_force_arrow, RIGHT)

        self.play(Create(parallel_force_arrow), Write(parallel_label))
        self.wait(1)

        # 展示公式
        formula1 = MathTex(r"F = m \cdot g \cdot \sin(\theta)", font_size=36)
        formula2 = MathTex(r"F_{\text{friction}} = \mu \cdot F_{\text{normal}}", font_size=36)
        formula1.to_edge(DOWN)
        formula2.next_to(formula1, DOWN)

        self.play(Write(formula1))
        self.wait(1)
        self.play(Write(formula2))
        self.wait(1)

        # 摩擦力展示
        friction_arrow = Arrow(
            start=poop.get_center(), end=poop.get_center() + LEFT * 2,
            color=RED
        )
        friction_label = Text("摩擦力", font_size=24, color=RED)
        friction_label.next_to(friction_arrow, LEFT)

        self.play(Create(friction_arrow), Write(friction_label))
        self.wait(1)

        # 摩擦力减小，💩滑下
        self.play(
            friction_arrow.animate.scale(0.5),
            poop.animate.shift(DOWN * 2 + RIGHT * 3),
            run_time=3
        )
        self.wait(1)

        # 💩跳入草地
        poop_target = poop.copy()
        poop_target.move_to(DOWN * 2.5 + RIGHT * 2)
        self.play(Transform(poop, poop_target), run_time=1)
        self.wait(1)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=1)