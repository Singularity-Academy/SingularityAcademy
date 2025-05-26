from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLUE, fill_opacity=1)
        background.set_fill("#87CEEB", opacity=1)  # 浅蓝渐变背景
        ground = Line(start=LEFT * FRAME_WIDTH, end=RIGHT * FRAME_WIDTH, color=GRAY)
        ground.to_edge(DOWN)
        stars = VGroup(*[Dot(point=np.random.random(3) * FRAME_WIDTH - FRAME_WIDTH / 2, color=WHITE, radius=0.01) for _ in range(50)])
        for star in stars:
            star.shift(UP * np.random.random() * FRAME_HEIGHT / 2)
        self.add(background, ground, stars)

        # 主要对象：球体 A 和 B
        ball_a = Circle(radius=0.5, color=RED, fill_opacity=1)
        ball_b = Circle(radius=0.5, color=BLUE, fill_opacity=1)
        ball_a.move_to(LEFT * 3 + DOWN * 1)
        ball_b.move_to(RIGHT * 3 + DOWN * 1)

        # 标签文本
        label_a = Text("A", font_size=36, color=WHITE).move_to(ball_a.get_center())
        label_b = Text("B", font_size=36, color=WHITE).move_to(ball_b.get_center())

        self.play(FadeIn(ball_a), FadeIn(ball_b), FadeIn(label_a), FadeIn(label_b))
        self.wait(1)

        # 作用力和反作用力箭头
        force_ab = Arrow(start=ball_a.get_center(), end=ball_b.get_center(), color=RED, buff=0.5)
        label_force_ab = Text("作用力 (Force A on B)", font_size=24, color=RED).next_to(force_ab, UP)

        force_ba = Arrow(start=ball_b.get_center(), end=ball_a.get_center(), color=BLUE, buff=0.5)
        label_force_ba = Text("反作用力 (Force B on A)", font_size=24, color=BLUE).next_to(force_ba, UP)

        self.play(Create(force_ab), Write(label_force_ab))
        self.wait(0.5)
        self.play(Create(force_ba), Write(label_force_ba))
        self.wait(1)

        # 牛顿第三定律公式
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=48, color=WHITE)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 动态模拟：球体的交互作用
        self.play(
            ball_a.animate.shift(RIGHT * 2),
            ball_b.animate.shift(LEFT * 2),
            force_ab.animate.shift(RIGHT * 2),
            force_ba.animate.shift(LEFT * 2),
            label_force_ab.animate.shift(RIGHT * 2),
            label_force_ba.animate.shift(LEFT * 2),
            run_time=3
        )
        self.wait(1)

        # 总结强调
        summary = Text("作用力与反作用力始终成对出现", font_size=32, color=WHITE)
        summary.to_edge(DOWN)
        self.play(FadeIn(summary))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))