from manim import *

class NewtonFirstLaw(Scene):
    def construct(self):
        # 中文标题
        title = Text("牛顿第一定律", font_size=48, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景网格线
        grid = NumberPlane(
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 2
            }
        )
        self.add(grid)

        # 地面线
        ground = Line(start=LEFT * 7, end=RIGHT * 7, color=GREY).shift(DOWN * 2.5)
        self.play(Create(ground))
        self.wait(1)

        # 静止的木箱
        box = Rectangle(width=1.2, height=1, color=BROWN, fill_opacity=1).shift(LEFT * 3 + DOWN * 2)
        box_label = Text("静止", font_size=24, color=WHITE).next_to(box, DOWN)
        self.play(FadeIn(box), Write(box_label))
        self.wait(1)

        # 匀速运动的红球
        ball = Circle(radius=0.5, color=RED, fill_opacity=1).shift(RIGHT * 3 + DOWN * 2)
        ball_label = Text("匀速运动", font_size=24, color=WHITE).next_to(ball, DOWN)
        self.play(FadeIn(ball), Write(ball_label))
        self.wait(1)

        # 静止公式
        static_formula = MathTex(r"F = 0 \Rightarrow v = 0", font_size=36).next_to(box, UP)
        self.play(Write(static_formula))
        self.wait(1)

        # 匀速运动公式
        motion_formula = MathTex(r"F = 0 \Rightarrow v = \text{constant}", font_size=36).next_to(ball, UP)
        self.play(Write(motion_formula))
        self.wait(1)

        # 箭头试图接近木箱但未施加外力
        no_force_arrow = Arrow(
            start=LEFT * 4 + DOWN * 2, end=box.get_center(),
            color=GREEN, buff=0.2
        )
        self.play(GrowArrow(no_force_arrow))
        self.wait(1)
        self.play(FadeOut(no_force_arrow))
        self.wait(1)

        # 球匀速运动
        self.play(ball.animate.shift(RIGHT * 3), run_time=3, rate_func=linear)
        self.wait(1)

        # 对木箱施加外力
        force_arrow_box = Arrow(
            start=box.get_center(), end=box.get_center() + RIGHT,
            color=GREEN, buff=0.2
        )
        self.play(GrowArrow(force_arrow_box))
        self.play(box.animate.shift(RIGHT * 2), run_time=2)
        self.wait(1)

        # 对红球施加外力
        force_arrow_ball = Arrow(
            start=ball.get_center(), end=ball.get_center() + UP + LEFT,
            color=GREEN, buff=0.2
        )
        self.play(GrowArrow(force_arrow_ball))
        self.play(ball.animate.shift(UP + LEFT * 2), run_time=2)
        self.wait(1)

        # 总结公式
        summary_formula = MathTex(r"F = 0 \Rightarrow \text{静止或匀速直线运动}", font_size=36).to_edge(DOWN)
        self.play(Write(summary_formula))
        summary_text = Text(
            "没有外力时，物体保持原状态；受力时，状态改变。",
            font_size=24, color=WHITE
        ).next_to(summary_formula, UP)
        self.play(Write(summary_text))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)