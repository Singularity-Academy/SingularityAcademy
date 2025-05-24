from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 场景设置
        self.camera.background_color = "#0D1B2A"  # 深蓝背景
        ground = Rectangle(width=14, height=0.5, color=LIGHT_GRAY, fill_opacity=1)
        ground.to_edge(DOWN)
        self.add(ground)

        # 星星背景效果
        stars = VGroup(*[
            Dot(point=np.random.uniform([-7, -2, 0], [7, 4, 0]), radius=0.03, color=WHITE)
            for _ in range(100)
        ])
        self.add(stars)

        # 标题
        title = Text("牛顿第三定律", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 球体设置
        ball_a = Circle(radius=0.5, color=RED, fill_opacity=1).shift(LEFT*3 + DOWN*0.5)
        ball_b = Circle(radius=0.5, color=BLUE, fill_opacity=1).shift(RIGHT*3 + DOWN*0.5)
        self.play(FadeIn(ball_a), FadeIn(ball_b))
        self.wait(1)

        # 作用力箭头
        force_a = Arrow(start=ball_a.get_center(), end=ball_b.get_center(), color=RED, buff=0.2, stroke_width=6)
        force_b = Arrow(start=ball_b.get_center(), end=ball_a.get_center(), color=BLUE, buff=0.2, stroke_width=6)
        force_label_a = MathTex(r"F_{\text{A→B}}", color=RED).next_to(force_a, UP, buff=0.2)
        force_label_b = MathTex(r"F_{\text{B→A}}", color=BLUE).next_to(force_b, DOWN, buff=0.2)

        # 动画展示作用力和反作用力
        self.play(GrowArrow(force_a), Write(force_label_a))
        self.wait(0.5)
        self.play(GrowArrow(force_b), Write(force_label_b))
        self.wait(1)

        # 牛顿第三定律公式
        formula = MathTex(r"F_{\text{A→B}} = -F_{\text{B→A}}", font_size=48, color=WHITE)
        formula.to_edge(UP, buff=1)
        self.play(Write(formula))
        self.wait(1)

        # 动画展示球体移动
        self.play(
            ball_a.animate.shift(LEFT*1),
            ball_b.animate.shift(RIGHT*1),
            force_a.animate.shift(LEFT*1),
            force_b.animate.shift(RIGHT*1),
            force_label_a.animate.shift(LEFT*1),
            force_label_b.animate.shift(RIGHT*1),
            run_time=2
        )
        self.wait(1)

        # 力箭头逐渐缩回
        self.play(FadeOut(VGroup(force_a, force_b, force_label_a, force_label_b)))
        self.wait(0.5)

        # 总结文字
        summary = Text("作用力与反作用力：力总是成双成对出现！", font_size=36, color=WHITE)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)

        # 场景结束
        self.play(FadeOut(VGroup(*self.mobjects)))