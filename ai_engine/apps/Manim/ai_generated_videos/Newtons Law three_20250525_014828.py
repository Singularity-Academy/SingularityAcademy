from manim import *
import numpy as np

class NewtonsLawScene(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = DARK_BLUE
        
        # 添加星星点缀
        stars = VGroup(*[
            Dot(point=np.random.uniform(-6, 6, size=3), color=WHITE, radius=0.03)
            for _ in range(50)
        ])
        self.add(stars)

        # 标题
        title = Text("揭示运动的秘密：牛顿三大定律", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 第一定律演示：惯性定律
        first_law_text = Text("牛顿第一定律：惯性定律", font_size=28, color=WHITE).to_edge(UP, buff=1)
        self.play(Write(first_law_text))
        self.wait(1)

        ball = Dot(color=YELLOW).move_to(LEFT * 4)
        self.play(Create(ball))
        self.wait(1)

        motion_text = Text("物体在没有外力作用下会保持静止或匀速直线运动", font_size=24, color=WHITE)
        motion_text.next_to(ball, DOWN * 2)
        self.play(Write(motion_text))
        self.wait(2)

        force_arrow = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT, color=RED)
        self.play(GrowArrow(force_arrow))
        self.play(ball.animate.shift(RIGHT * 3), run_time=2)
        self.wait(1)

        first_law_formula = MathTex(r"F = 0 \implies \text{保持运动状态}").next_to(ball, UP)
        self.play(Write(first_law_formula))
        self.wait(2)
        self.play(FadeOut(VGroup(ball, force_arrow, motion_text, first_law_formula)))
        self.wait(1)

        # 第二定律演示：加速度定律
        second_law_text = Text("牛顿第二定律：加速度定律", font_size=28, color=WHITE).to_edge(UP, buff=1)
        self.play(Transform(first_law_text, second_law_text))
        self.wait(1)

        ball = Dot(color=YELLOW).move_to(LEFT * 4)
        force_arrow = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT * 2, color=RED)
        second_law_formula = MathTex(r"F = ma").next_to(ball, UP)

        self.play(Create(ball), Create(force_arrow), Write(second_law_formula))
        self.wait(1)

        # 动态显示力和加速度关系
        force_value = MathTex(r"F = 10\,\text{N}", font_size=24).next_to(force_arrow, UP)
        mass_value = MathTex(r"m = 2\,\text{kg}", font_size=24).next_to(ball, DOWN)
        acceleration_value = MathTex(r"a = 5\,\text{m/s}^2", font_size=24).next_to(ball, RIGHT * 2)

        self.play(Write(force_value), Write(mass_value), Write(acceleration_value))
        self.play(ball.animate.shift(RIGHT * 4), run_time=2)
        self.wait(2)
        self.play(FadeOut(VGroup(ball, force_arrow, second_law_formula, force_value, mass_value, acceleration_value)))
        self.wait(1)

        # 第三定律演示：作用与反作用定律
        third_law_text = Text("牛顿第三定律：作用与反作用定律", font_size=28, color=WHITE).to_edge(UP, buff=1)
        self.play(Transform(second_law_text, third_law_text))
        self.wait(1)

        ball = Dot(color=YELLOW).move_to(LEFT * 2)
        wall = Line(start=RIGHT * 4 + DOWN, end=RIGHT * 4 + UP, color=WHITE)
        self.play(Create(ball), Create(wall))
        self.wait(1)

        impact_arrow = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT, color=RED)
        reaction_arrow = Arrow(start=wall.get_center(), end=wall.get_center() + LEFT, color=BLUE)

        self.play(GrowArrow(impact_arrow))
        self.play(ball.animate.shift(RIGHT * 2), Create(reaction_arrow))
        self.wait(1)

        third_law_formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}").next_to(wall, UP)
        self.play(Write(third_law_formula))
        self.wait(2)

        # 结束
        self.play(FadeOut(VGroup(ball, wall, impact_arrow, reaction_arrow, third_law_formula, second_law_text)))
        self.play(FadeOut(title))
        self.wait(1)