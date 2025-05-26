from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#87CEEB"  # 浅蓝渐变背景
        ground = Line(start=LEFT*6, end=RIGHT*6, color=GRAY).shift(DOWN*2.5)  # 地面
        self.play(Create(ground), run_time=1)
        
        # 标题
        title = Text("力的对话：牛顿第三定律的生动演绎", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 主要对象
        block_a = Square(side_length=1, color=RED, fill_opacity=0.8).shift(LEFT*2 + DOWN*2)
        ball_b = Circle(radius=0.5, color=BLUE, fill_opacity=0.8).shift(RIGHT*2 + DOWN*2)
        self.play(FadeIn(block_a), FadeIn(ball_b), run_time=1)

        # 初始状态：作用力与反作用力
        force_ab = Arrow(start=block_a.get_center(), end=ball_b.get_center(), color=RED, buff=0.1, stroke_width=6)
        force_ba = Arrow(start=ball_b.get_center(), end=block_a.get_center(), color=BLUE, buff=0.1, stroke_width=6)
        self.play(Create(force_ab), Create(force_ba), run_time=1)
        self.wait(0.5)

        # 动态展示公式
        formula = MathTex(r"F_{A \to B} = -F_{B \to A}", color=WHITE, font_size=48).to_edge(DOWN)
        self.play(Write(formula), run_time=1)
        self.wait(1)

        # 旁白文字
        text = Text("作用力与反作用力大小相等，方向相反。", font_size=28, color=YELLOW)
        text.next_to(formula, UP, buff=0.5)
        self.play(FadeIn(text), run_time=1)
        self.wait(1)

        # 对比演示：力的变化
        stronger_force_ab = Arrow(start=block_a.get_center(), end=ball_b.get_center(), color=RED, buff=0.1, stroke_width=8)
        stronger_force_ba = Arrow(start=ball_b.get_center(), end=block_a.get_center(), color=BLUE, buff=0.1, stroke_width=8)
        self.play(Transform(force_ab, stronger_force_ab), Transform(force_ba, stronger_force_ba), run_time=1.5)
        self.wait(1)

        # 结尾文字与公式放大
        conclusion_text = Text("你推动的每个物体，也在推动你。", font_size=32, color=YELLOW)
        conclusion_text.to_edge(UP, buff=1)
        self.play(FadeOut(force_ab), FadeOut(force_ba))
        self.play(Write(conclusion_text), formula.animate.scale(1.5), run_time=1.5)
        self.wait(2)

        # 结束场景
        self.play(FadeOut(VGroup(block_a, ball_b, formula, text, ground, conclusion_text, title)), run_time=2)
        self.wait(1)