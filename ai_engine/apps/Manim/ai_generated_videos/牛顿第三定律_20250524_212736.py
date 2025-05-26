from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#87CEEB"  # 浅蓝色背景
        grid = NumberPlane(background_line_style={
            "stroke_color": GRAY,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        })
        self.add(grid)

        # 地板
        ground = Rectangle(width=10, height=0.2, color=GRAY, fill_opacity=1)
        ground.to_edge(DOWN)
        self.add(ground)

        # 标题公式
        formula = MathTex(r"F_{A} = -F_{B}", font_size=48, color=WHITE)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 创建球体和推手
        red_ball = Circle(radius=0.5, color=RED, fill_opacity=0.8)
        blue_ball = Circle(radius=0.5, color=BLUE, fill_opacity=0.8)
        red_ball.move_to(LEFT * 2 + DOWN * 0.6)
        blue_ball.move_to(RIGHT * 2 + DOWN * 0.6)

        push_hand = Rectangle(width=0.5, height=0.3, color=WHITE, fill_opacity=0.8)
        push_hand.move_to(LEFT * 3 + DOWN * 0.6)

        # 添加球体和推手
        self.play(FadeIn(red_ball), FadeIn(blue_ball), FadeIn(push_hand))
        self.wait(1)

        # 力箭头和标签
        action_arrow = Arrow(
            start=red_ball.get_center(),
            end=red_ball.get_center() + RIGHT * 2,
            color=RED,
            stroke_width=8,
        )
        reaction_arrow = Arrow(
            start=blue_ball.get_center(),
            end=blue_ball.get_center() + LEFT * 2,
            color=BLUE,
            stroke_width=8,
        )

        action_label = Text("作用力", font_size=24, color=RED)
        action_label.next_to(action_arrow, UP)
        reaction_label = Text("反作用力", font_size=24, color=BLUE)
        reaction_label.next_to(reaction_arrow, UP)

        # 动画序列
        # 推手推动红球
        self.play(
            push_hand.animate.shift(RIGHT * 1),
            red_ball.animate.shift(RIGHT * 2),
            GrowArrow(action_arrow),
            run_time=2,
        )
        self.wait(1)

        # 蓝球受力
        self.play(
            blue_ball.animate.shift(LEFT * 2),
            GrowArrow(reaction_arrow),
            run_time=2,
        )
        self.wait(1)

        # 加入力箭头的标签
        self.play(Write(action_label), Write(reaction_label))
        self.wait(1)

        # 动态公式演绎
        self.play(
            formula.animate.set_color_by_tex("F_{A}", RED),
            formula.animate.set_color_by_tex("F_{B}", BLUE),
            run_time=2,
        )
        self.wait(1)

        # 循环演示
        for _ in range(2):
            self.play(
                red_ball.animate.shift(LEFT * 2),
                blue_ball.animate.shift(RIGHT * 2),
                action_arrow.animate.shift(LEFT * 2),
                reaction_arrow.animate.shift(RIGHT * 2),
                run_time=1,
            )
            self.wait(0.5)
            self.play(
                red_ball.animate.shift(RIGHT * 2),
                blue_ball.animate.shift(LEFT * 2),
                action_arrow.animate.shift(RIGHT * 2),
                reaction_arrow.animate.shift(LEFT * 2),
                run_time=1,
            )
            self.wait(0.5)

        # 总结文本
        summary = Text(
            "牛顿第三定律：作用力与反作用力总是大小相等，方向相反",
            font_size=32,
            color=WHITE,
        )
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))