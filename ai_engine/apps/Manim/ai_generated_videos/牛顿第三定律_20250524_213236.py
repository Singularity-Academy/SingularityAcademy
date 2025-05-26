from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#ADD8E6"  # 浅蓝色背景
        ground = Line(start=LEFT * 6, end=RIGHT * 6, color=WHITE).to_edge(DOWN)
        self.play(Create(ground))
        self.wait(1)

        # 创建主要对象
        ball_a = Circle(radius=0.6, color=RED, fill_opacity=1).shift(LEFT * 3 + DOWN * 0.5)
        ball_b = Circle(radius=0.4, color=BLUE, fill_opacity=1).shift(RIGHT * 3 + DOWN * 0.5)
        self.play(FadeIn(ball_a), FadeIn(ball_b))
        self.wait(1)

        # 动画：红色大球移动并撞向蓝色小球
        self.play(ball_a.animate.shift(RIGHT * 3), run_time=2)
        self.wait(0.5)

        # 显示作用力和反作用力箭头
        force_arrow_a = Arrow(start=ball_a.get_center(), end=ball_b.get_center(), color=GREEN)
        force_arrow_b = Arrow(start=ball_b.get_center(), end=ball_a.get_center(), color=ORANGE)
        self.play(Create(force_arrow_a), Create(force_arrow_b))
        self.wait(1)

        # 显示公式
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=48, color=WHITE).to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 动画：蓝色小球向右滑动
        self.play(
            ball_b.animate.shift(RIGHT * 2),
            force_arrow_a.animate.scale(0.8),
            force_arrow_b.animate.scale(0.8),
            run_time=2
        )
        self.wait(1)

        # 总结与强调
        summary_text = Text("作用力与反作用力永远成对出现", font_size=36, color=WHITE)
        summary_text.add_background_rectangle(color=BLACK, opacity=0.6, buff=0.5)
        self.play(Write(summary_text))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(ball_a, ball_b, force_arrow_a, force_arrow_b, formula, summary_text, ground)))
        self.wait(1)