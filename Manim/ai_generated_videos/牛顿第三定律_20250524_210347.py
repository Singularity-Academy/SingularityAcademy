from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 场景标题
        title = Text("力的对话：牛顿第三定律的动态演绎", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLUE, fill_color=BLUE, fill_opacity=0.3)
        background_grid = NumberPlane(x_range=(-8, 8), y_range=(-4, 4), color=WHITE, opacity=0.1)
        self.add(background, background_grid)

        # 墙壁和地面
        wall = Rectangle(width=0.3, height=4, color=GRAY, fill_color=GRAY, fill_opacity=1)
        wall.to_edge(RIGHT)

        ground = Rectangle(width=FRAME_WIDTH, height=0.3, color=LIGHT_GRAY, fill_color=LIGHT_GRAY, fill_opacity=1)
        ground.to_edge(DOWN)

        self.play(FadeIn(wall), FadeIn(ground))
        self.wait(1)

        # 球体
        ball = Circle(radius=0.5, color=RED, fill_color=RED, fill_opacity=1)
        ball.move_to(LEFT * 4 + DOWN * 1.5)
        self.play(FadeIn(ball))
        self.wait(1)

        # 球体移动接近墙壁
        self.play(ball.animate.shift(RIGHT * 6), run_time=3)
        self.wait(1)

        # 显示作用力
        action_arrow = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT * 2, color=GREEN, buff=0)
        action_label = Text("作用力", font_size=32, color=GREEN)
        action_label.next_to(action_arrow, UP)

        formula = MathTex(r"F_{action} = -F_{reaction}", font_size=36, color=WHITE)
        formula.to_edge(UP, buff=1)

        self.play(Create(action_arrow), Write(action_label), Write(formula))
        self.wait(1)

        # 墙壁反作用力
        reaction_arrow = Arrow(start=wall.get_center(), end=wall.get_center() + LEFT * 2, color=ORANGE, buff=0)
        reaction_label = Text("反作用力", font_size=32, color=ORANGE)
        reaction_label.next_to(reaction_arrow, UP)

        self.play(Create(reaction_arrow), Write(reaction_label))
        self.wait(1)

        # 力的平衡展示
        balance_text = Text("作用力与反作用力总是大小相等、方向相反。", font_size=28, color=WHITE)
        balance_text.move_to(DOWN * 2)

        self.play(Write(balance_text))
        self.wait(2)

        # 箭头闪烁强调
        self.play(
            action_arrow.animate.set_opacity(0.5),
            reaction_arrow.animate.set_opacity(0.5),
            run_time=0.5
        )
        self.play(
            action_arrow.animate.set_opacity(1),
            reaction_arrow.animate.set_opacity(1),
            run_time=0.5
        )
        self.wait(1)

        # 球体弹离墙壁
        self.play(ball.animate.shift(LEFT * 4), run_time=2)
        self.play(FadeOut(action_arrow), FadeOut(reaction_arrow), FadeOut(action_label), FadeOut(reaction_label))
        self.wait(1)

        # 公式居中并结束
        self.play(formula.animate.move_to(ORIGIN), FadeOut(balance_text), FadeOut(background_grid))
        self.wait(2)

        # 场景淡出
        self.play(FadeOut(VGroup(*self.mobjects)))