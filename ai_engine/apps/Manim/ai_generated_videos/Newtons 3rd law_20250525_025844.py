from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background_grid = NumberPlane(
            x_range=(-8, 8, 1),
            y_range=(-4, 4, 1),
            background_line_style={"stroke_color": GREY, "stroke_opacity": 0.3}
        )
        self.add(background_grid)
        
        title = Text("Newton's Third Law", font_size=24, color=WHITE)
        title.to_corner(DR)
        self.add(title)

        # 创建球体和接触点
        ball_a = Circle(radius=0.6, color=BLUE, fill_opacity=1).shift(LEFT * 2)
        ball_b = Circle(radius=0.4, color=RED, fill_opacity=1).shift(RIGHT * 2)
        self.play(FadeIn(ball_a), FadeIn(ball_b))

        # 场景标题
        intro_text = Text("牛顿第三定律：作用力与反作用力", font_size=32, color=WHITE)
        intro_text.to_edge(UP)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))

        # 球体移动至接触点
        self.play(ball_a.animate.shift(RIGHT * 3), run_time=2)
        contact_point = Dot(point=RIGHT, color=YELLOW)
        glowing_effect = Circle(radius=0.2, color=YELLOW).move_to(contact_point)
        self.play(FadeIn(contact_point), Create(glowing_effect), run_time=0.5)

        # 作用力箭头
        force_ab = Arrow(start=ball_a.get_center(), end=ball_b.get_center(), color=GREEN, buff=0.5)
        self.play(Create(force_ab))
        self.wait(1)

        # 反作用力箭头
        force_ba = Arrow(start=ball_b.get_center(), end=ball_a.get_center(), color=ORANGE, buff=0.5)
        self.play(Create(force_ba))
        self.wait(1)

        # 动态公式显示
        formula = MathTex(r"F_{AB} = -F_{BA}", color=WHITE)
        formula.to_edge(DOWN)
        self.play(Write(formula), run_time=2)
        self.wait(2)

        # 球体因力移动
        self.play(
            ball_a.animate.shift(LEFT * 2),
            ball_b.animate.shift(RIGHT * 1.5),
            force_ab.animate.shift(LEFT * 2),
            force_ba.animate.shift(RIGHT * 1.5),
            run_time=2
        )
        self.wait(1)

        # 接触点光环消失
        self.play(FadeOut(contact_point), FadeOut(glowing_effect))
        self.wait(1)

        # 球体复位
        self.play(
            ball_a.animate.shift(RIGHT * 2),
            ball_b.animate.shift(LEFT * 1.5),
            force_ab.animate.shift(RIGHT * 2),
            force_ba.animate.shift(LEFT * 1.5),
            run_time=2
        )
        self.wait(1)

        # 力箭头消失
        self.play(FadeOut(force_ab), FadeOut(force_ba))
        self.wait(1)

        # 总结文字
        conclusion_text = Text(
            "作用力和反作用力总是同时存在，且大小相等、方向相反。",
            font_size=28, color=WHITE
        )
        self.play(Write(conclusion_text))
        self.wait(3)
        self.play(FadeOut(conclusion_text), FadeOut(ball_a), FadeOut(ball_b), FadeOut(formula), FadeOut(background_grid), FadeOut(title))