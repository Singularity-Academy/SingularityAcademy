from manim import *

class NewtonFirstLaw(Scene):
    def construct(self):
        # 场景背景设置
        self.camera.background_color = "#1E1E2E"  # 深蓝色背景
        stars = VGroup(*[Dot(color=WHITE, radius=0.01) for _ in range(100)])
        stars.arrange_in_grid(10, 10).scale(0.5).shift(UP * 0.5)
        self.add(stars)

        # 标题文字
        title = Text("牛顿第一定律", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 静止球体和地面
        ground = Line(LEFT * 5, RIGHT * 5, color=GREY, stroke_width=2).shift(DOWN * 2)
        ball = Circle(radius=0.5, color=WHITE, fill_opacity=1).set_fill(color="#C0C0C0")  # 银白色球体
        ball.next_to(ground, UP, buff=0.5)

        self.play(Create(ground), FadeIn(ball))
        self.wait(1)

        # 静止状态文字和箭头
        static_label = Text("静止", font_size=24, color=WHITE).next_to(ball, UP, buff=0.8)
        static_arrow = Arrow(start=ball.get_center(), end=ball.get_center(), color=WHITE, stroke_width=2)

        self.play(Write(static_label), Create(static_arrow))
        self.wait(1)

        # 静止状态说明
        static_explanation = Text("物体在没有外力作用时保持静止状态", font_size=24, color=WHITE).to_edge(DOWN)
        self.play(Write(static_explanation))
        self.wait(2)

        # 匀速运动状态
        self.play(FadeOut(static_label), FadeOut(static_arrow), FadeOut(static_explanation))
        moving_label = Text("匀速运动", font_size=24, color=WHITE).next_to(ball, UP, buff=0.8)
        velocity_arrow = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT * 1.5, color=WHITE, stroke_width=2)

        self.play(Write(moving_label), Create(velocity_arrow))
        self.play(ball.animate.shift(RIGHT * 4), velocity_arrow.animate.shift(RIGHT * 4), run_time=3, rate_func=linear)
        self.wait(1)

        # 匀速运动状态说明
        moving_explanation = Text("物体在没有外力作用时，保持匀速直线运动", font_size=24, color=WHITE).to_edge(DOWN)
        self.play(Write(moving_explanation))
        self.wait(2)

        # 外力作用
        self.play(FadeOut(moving_label), FadeOut(moving_explanation))
        force_arrow = Arrow(start=ball.get_center() + LEFT * 1.5, end=ball.get_center(), color=RED, stroke_width=3)
        force_label = Text("外力", font_size=24, color=RED).next_to(force_arrow, LEFT, buff=0.3)

        self.play(Create(force_arrow), Write(force_label))
        self.play(ball.animate.shift(UP * 2 + RIGHT * 2), velocity_arrow.animate.shift(UP * 2 + RIGHT * 2), run_time=2, rate_func=rush_into)
        self.wait(1)

        # 外力后运动变化说明
        force_explanation = Text("有外力，运动状态改变", font_size=24, color=RED).to_edge(DOWN)
        self.play(Write(force_explanation))
        self.wait(2)

        # 回归惯性状态
        self.play(FadeOut(force_arrow), FadeOut(force_label), FadeOut(force_explanation))
        inertia_label = Text("匀速运动", font_size=24, color=WHITE).next_to(ball, UP, buff=0.8)

        self.play(Write(inertia_label))
        self.play(ball.animate.shift(RIGHT * 3), velocity_arrow.animate.shift(RIGHT * 3), run_time=3, rate_func=linear)
        self.wait(1)

        # 结尾
        self.play(FadeOut(inertia_label), FadeOut(velocity_arrow), FadeOut(ball), FadeOut(ground))
        ending_formula = Text("牛顿第一定律", font_size=36, color=WHITE)
        ending_subtitle = Text("惯性是物体的基本属性", font_size=24, color=WHITE).next_to(ending_formula, DOWN, buff=0.5)

        self.play(Write(ending_formula), FadeIn(ending_subtitle))
        self.wait(2)
        self.play(FadeOut(Group(ending_formula, ending_subtitle)))