from manim import *

class NewtonFirstLawScene(Scene):
    def construct(self):
        # 设置场景背景颜色为深蓝色
        self.camera.background_color = DARK_BLUE

        # 添加标题
        title = Text("牛顿第一定律：静止与运动的奥秘", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 添加静止的球和地面
        ball = Dot(color=WHITE, radius=0.2).shift(LEFT * 4)
        ground = Line(start=LEFT * 6, end=RIGHT * 6, color=GRAY).shift(DOWN * 2)
        grid = VGroup(
            *[Line(start=LEFT * 6, end=RIGHT * 6, color=GRAY, stroke_opacity=0.3).shift(DOWN * (2 + i * 0.2)) for i in range(10)]
        )
        self.play(Create(ground), Create(grid), FadeIn(ball))
        self.wait(1)

        # 添加文字说明：静止中的物体
        static_text = Text("静止中的物体", font_size=24, color=WHITE)
        static_text.next_to(ball, UP)
        self.play(FadeIn(static_text))
        self.wait(1)

        # 球开始匀速滚动
        self.play(FadeOut(static_text))
        motion_text = Text("匀速直线运动", font_size=24, color=WHITE)
        motion_text.next_to(ball, UP)
        self.play(Write(motion_text))
        self.play(ball.animate.shift(RIGHT * 6), run_time=4, rate_func=linear)
        self.wait(1)

        # 外力加入场景
        self.play(FadeOut(motion_text))
        force_arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1, max_stroke_width_to_length_ratio=2,
        ).next_to(ball, LEFT)
        force_text = Text("外力导致加速运动", font_size=24, color=WHITE)
        force_text.next_to(ball, UP)
        formula = MathTex(r"F_{\text{net}} = ma", font_size=36, color=YELLOW)
        formula.to_corner(UR)
        self.play(Create(force_arrow), FadeIn(force_text), Write(formula))
        self.play(ball.animate.shift(RIGHT * 4), run_time=2, rate_func=rush_into)
        self.wait(1)

        # 外力移除，球恢复匀速运动
        self.play(FadeOut(force_arrow), FadeOut(force_text))
        inertial_text = Text("牛顿第一定律：物体保持静止或匀速运动", font_size=24, color=WHITE)
        inertial_text.to_edge(DOWN)
        self.play(Write(inertial_text))
        self.play(ball.animate.shift(RIGHT * 4), run_time=4, rate_func=linear)
        self.wait(1)

        # 总结画面
        self.play(FadeOut(ball), FadeOut(inertial_text), FadeOut(formula), FadeOut(grid))
        summary_text = Text("牛顿第一定律：物体的惯性", font_size=36, color=YELLOW)
        self.play(Write(summary_text))
        self.wait(2)

        # 结束场景
        self.play(FadeOut(summary_text), FadeOut(ground), FadeOut(title))
        self.wait(1)