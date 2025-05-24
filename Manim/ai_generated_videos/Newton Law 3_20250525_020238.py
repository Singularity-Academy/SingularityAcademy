from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH * 2, height=FRAME_HEIGHT * 2, color=BLUE, fill_opacity=1)
        background.set_style(fill_color="#001F3F", stroke_width=0)
        self.add(background)

        ground = Line(start=LEFT * FRAME_WIDTH, end=RIGHT * FRAME_WIDTH, color=WHITE, stroke_width=2)
        ground.shift(DOWN * 3)
        self.add(ground)

        # 标题
        title = Text("牛顿第三定律：作用力与反作用力", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 主要对象
        ball = Circle(radius=0.5, color=RED, fill_opacity=1).shift(LEFT * 3 + DOWN * 2)
        box = Square(side_length=1, color=BLUE, fill_opacity=1).shift(RIGHT * 3 + DOWN * 2)
        self.play(FadeIn(ball), FadeIn(box))
        self.wait(1)

        # 物体A移动至物体B
        self.play(ball.animate.shift(RIGHT * 5), run_time=2)
        self.wait(0.5)

        # 作用力箭头
        action_arrow = Arrow(start=ball.get_center(), end=box.get_center(), color=RED, buff=0.1, stroke_width=3)
        action_text = Text("作用力", font_size=24, color=RED).next_to(action_arrow, UP)
        self.play(Create(action_arrow), Write(action_text))
        self.wait(0.5)

        # 反作用力箭头
        reaction_arrow = Arrow(start=box.get_center(), end=ball.get_center(), color=BLUE, buff=0.1, stroke_width=3)
        reaction_text = Text("反作用力", font_size=24, color=BLUE).next_to(reaction_arrow, DOWN)
        self.play(Create(reaction_arrow), Write(reaction_text))
        self.wait(1)

        # 箭头闪烁效果
        for _ in range(2):
            self.play(action_arrow.animate.set_opacity(0.5), reaction_arrow.animate.set_opacity(0.5), run_time=0.5)
            self.play(action_arrow.animate.set_opacity(1), reaction_arrow.animate.set_opacity(1), run_time=0.5)

        # 公式展示
        formula = MathTex(r"F_{AB} = -F_{BA}", font_size=48, color=YELLOW)
        formula.move_to(UP * 2)
        self.play(Write(formula))
        self.wait(1)

        # 力平衡效果
        self.play(ball.animate.shift(LEFT * 0.1).shift(RIGHT * 0.1), box.animate.shift(RIGHT * 0.1).shift(LEFT * 0.1), run_time=0.5)
        self.wait(0.5)

        # 总结与结尾
        summary = Text("每个力都有大小相等、方向相反的反作用力。", font_size=28, color=WHITE)
        summary.move_to(DOWN * 1.5)
        self.play(Write(summary), run_time=2)
        self.wait(2)

        # 缩放展示整个场景
        self.play(self.camera.frame.animate.scale(1.2).move_to(ORIGIN), run_time=2)
        self.wait(1)

        # 结束
        self.play(FadeOut(VGroup(*self.mobjects)))