from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景和地面
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color=BLUE, fill_opacity=0.5)
        background.set_stroke(width=0)
        ground = Line(start=LEFT * FRAME_WIDTH / 2, end=RIGHT * FRAME_WIDTH / 2, color=GRAY)
        ground.shift(DOWN * 2.5)

        self.play(FadeIn(background), Create(ground))
        self.wait(1)

        # 墙壁和球
        wall = Rectangle(width=0.5, height=3, color=GRAY, fill_color=GRAY, fill_opacity=1)
        wall.move_to(RIGHT * 4 + DOWN * 1.5)
        ball = Circle(radius=0.3, color=RED, fill_color=RED, fill_opacity=1)
        ball.move_to(LEFT * 4 + DOWN * 2.2)

        self.play(FadeIn(wall), FadeIn(ball))
        self.wait(1)

        # 球滚动到墙壁
        self.play(ball.animate.shift(RIGHT * 7.5), run_time=2)
        self.wait(0.5)

        # 撞击时的作用力箭头
        action_arrow = Arrow(start=ball.get_center(), end=wall.get_center(), color=RED, buff=0.2, stroke_width=4)
        self.play(Create(action_arrow), run_time=1)
        self.wait(0.5)

        # 墙壁的反作用力箭头
        reaction_arrow = Arrow(start=wall.get_center(), end=ball.get_center(), color=BLUE, buff=0.2, stroke_width=4)
        self.play(Create(reaction_arrow), run_time=1)
        self.wait(0.5)

        # 牛顿第三定律公式
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=48)
        formula.to_edge(UP)
        self.play(Write(formula), run_time=1.5)
        self.wait(0.5)

        # 添加文字解释
        explanation = Text("作用力与反作用力总是大小相等、方向相反", font_size=32, color=WHITE)
        explanation.next_to(formula, DOWN, buff=0.5)
        self.play(Write(explanation), run_time=1.5)
        self.wait(1)

        # 球被反作用力推动离开墙壁
        self.play(ball.animate.shift(LEFT * 2), FadeOut(action_arrow), FadeOut(reaction_arrow), run_time=2)
        self.wait(1)

        # 结束动画
        title = Text("牛顿第三定律", font_size=36, color=WHITE)
        title.to_edge(DOWN)
        self.play(FadeOut(VGroup(*self.mobjects)), FadeIn(title))
        self.wait(2)