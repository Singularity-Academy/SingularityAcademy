from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=GRAY, fill_opacity=0.3)
        ground = Line(start=LEFT * 7, end=RIGHT * 7, color=WHITE, stroke_width=2)
        ground.shift(DOWN * 2.5)
        self.add(background, ground)

        # 初始标题
        title = Text("牛顿第三定律：作用力与反作用力", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建主要对象
        blue_square = Square(side_length=1, color=BLUE, fill_opacity=1)
        red_circle = Circle(radius=0.5, color=RED, fill_opacity=1)

        # 设置初始位置
        blue_square.move_to(LEFT * 3 + DOWN * 2)
        red_circle.move_to(RIGHT * 3 + DOWN * 2)

        self.play(FadeIn(blue_square), FadeIn(red_circle))
        self.wait(1)

        # 动画交互开始
        self.play(blue_square.animate.shift(RIGHT * 5), run_time=2)
        self.wait(0.5)

        # 碰撞瞬间箭头显示
        action_force = Arrow(start=blue_square.get_center(), end=blue_square.get_center() + RIGHT * 2, color=GREEN, buff=0.1, stroke_width=5)
        reaction_force = Arrow(start=red_circle.get_center(), end=red_circle.get_center() + LEFT * 2, color=ORANGE, buff=0.1, stroke_width=5)
        self.play(Create(action_force), Create(reaction_force))
        self.wait(1)

        # 显示公式
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=36, color=WHITE)
        formula.to_edge(UP).shift(DOWN * 0.5)
        self.play(Write(formula))
        self.wait(1)

        # 动态展示箭头变化
        self.play(
            action_force.animate.scale(1.5),
            reaction_force.animate.scale(1.5),
            blue_square.animate.shift(LEFT * 2),
            red_circle.animate.shift(RIGHT * 2),
            run_time=2
        )
        self.wait(1)

        self.play(
            action_force.animate.scale(0.5),
            reaction_force.animate.scale(0.5),
            run_time=1
        )
        self.wait(1)

        # 总结与强调
        self.play(FadeOut(action_force), FadeOut(reaction_force))
        summary_text = Text("作用力与反作用力永远成对出现，大小相等，方向相反", font_size=32, color=WHITE)
        summary_text.to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(2)

        # 清晰视觉总结
        self.play(FadeOut(summary_text), FadeOut(title))
        self.play(formula.animate.set_color(YELLOW).scale(1.5))
        self.wait(1)
        self.play(formula.animate.scale(2).set_opacity(0.8), run_time=2)
        self.wait(1)

        # 结束场景
        self.play(FadeOut(VGroup(*self.mobjects)))