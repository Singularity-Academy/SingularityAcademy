from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#001F3F"  # 深蓝色
        light_glow = Circle(radius=4, color=WHITE, fill_opacity=0.1)
        light_glow.set_stroke(width=0)
        self.add(light_glow)
        
        # 标题
        title = Text("牛顿第三定律", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 两个圆球
        ball_a = Circle(radius=0.5, color=RED, fill_opacity=1).move_to(LEFT * 2)
        ball_b = Circle(radius=0.5, color=BLUE, fill_opacity=1).move_to(RIGHT * 2)

        # 力箭头和标签
        force_a = Arrow(start=LEFT * 1.5, end=LEFT * 2.5, color=WHITE, buff=0)
        force_b = Arrow(start=RIGHT * 2.5, end=RIGHT * 1.5, color=WHITE, buff=0)
        label_a = Text("作用力", font_size=24, color=WHITE).next_to(force_a, UP)
        label_b = Text("反作用力", font_size=24, color=WHITE).next_to(force_b, UP)

        # 添加物体和力
        self.play(FadeIn(ball_a), FadeIn(ball_b))
        self.wait(0.5)
        self.play(Create(force_a), Create(force_b), Write(label_a), Write(label_b))
        self.wait(1)

        # 动画序列
        self.play(
            ball_a.animate.shift(RIGHT * 2),
            ball_b.animate.shift(LEFT * 2),
            force_a.animate.shift(RIGHT * 2),
            force_b.animate.shift(LEFT * 2),
            run_time=2
        )
        self.wait(1)

        # 牛顿第三定律公式
        formula = MathTex(r"F_A = -F_B", font_size=48, color=WHITE)
        formula.move_to(DOWN * 2)
        self.play(Write(formula))
        self.wait(1)

        # 强调箭头和标签
        self.play(
            force_a.animate.set_color(YELLOW),
            force_b.animate.set_color(YELLOW),
            label_a.animate.set_color(YELLOW).scale(1.2),
            label_b.animate.set_color(YELLOW).scale(1.2)
        )
        self.wait(1)

        # 总结文字
        summary = Text(
            "力总是成对出现，大小相等，方向相反",
            font_size=36, color=WHITE
        )
        summary.move_to(DOWN * 3)
        self.play(Write(summary))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))