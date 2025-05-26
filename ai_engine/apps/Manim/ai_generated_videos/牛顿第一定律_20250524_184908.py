from manim import *

class NewtonFirstLawScene(Scene):
    def construct(self):
        # 中文标题
        title = Text("运动的秘密：牛顿第一定律的直观演示", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # 背景设置
        background = Rectangle(width=14, height=8, color=BLUE, fill_opacity=0.4)
        background.set_z_index(-1)
        self.add(background)

        # 地面绘制
        ground = Line(start=LEFT * 7, end=RIGHT * 7, color=WHITE)
        ground.shift(DOWN * 2.5)
        self.play(Create(ground), run_time=1)
        self.wait(0.5)

        # 静止小球
        ball = Circle(radius=0.3, color=BLACK, fill_color=WHITE, fill_opacity=1)
        ball.move_to(LEFT * 4 + DOWN * 2.2)
        self.play(FadeIn(ball), run_time=1)
        self.wait(0.5)

        # 牛顿第一定律文字展示
        text_law = Text("如果一个物体不受外力作用，它将保持静止或匀速直线运动状态。",
                        font_size=28, color=WHITE, background_stroke_color=BLUE, background_stroke_width=1)
        text_law.scale(0.8).next_to(ball, UP * 2)
        self.play(Write(text_law), run_time=2)
        self.wait(1)

        # 数学公式展示
        formula_static = MathTex(r"F_{\text{net}} = 0 \implies \text{运动状态不变}", color=YELLOW)
        formula_static.next_to(text_law, DOWN, buff=0.5)
        self.play(Write(formula_static), run_time=1)
        self.wait(1)

        # 匀速运动演示
        self.play(ball.animate.shift(RIGHT * 6), run_time=3, rate_func=linear)
        formula_motion = MathTex(r"F_{\text{net}} = 0 \implies v = \text{constant}", color=YELLOW)
        formula_motion.move_to(formula_static.get_center())
        self.play(Transform(formula_static, formula_motion), run_time=1)
        hint_constant = Text("没有外力，物体将继续保持匀速运动。",
                             font_size=24, color=WHITE)
        hint_constant.scale(0.8)
        hint_constant.next_to(formula_motion, DOWN, buff=0.5)
        self.play(FadeIn(hint_constant), run_time=2)
        self.wait(2)

        # 外力作用演示
        force_arrow = Arrow(start=RIGHT * 4 + UP * 1, end=RIGHT * 4 + DOWN * 0.5, color=RED, buff=0.2)
        force_text = Text("外力作用：改变运动状态", font_size=24, color=RED)
        force_text.next_to(force_arrow, UP, buff=0.3)
        self.play(Create(force_arrow), FadeIn(force_text), run_time=1)
        self.wait(1)
        self.play(ball.animate.shift(RIGHT * 4), run_time=2, rate_func=rush_into)
        formula_acceleration = MathTex(r"F_{\text{net}} \neq 0 \implies a \neq 0", color=YELLOW)
        formula_acceleration.move_to(formula_static.get_center())
        self.play(Transform(formula_static, formula_acceleration), run_time=1)
        self.wait(1)

        # 惯性概念总结
        summary_text = Text("惯性是物体保持其运动状态的能力，除非受到外力作用。",
                            font_size=28, color=WHITE)
        summary_text.scale(0.8)
        summary_text.next_to(ball, UP * 2)
        self.play(Transform(text_law, summary_text), run_time=2)
        inertia_label = Text("惯性", font_size=28, color=WHITE)
        inertia_label.next_to(ball, RIGHT, buff=0.5)
        self.play(FadeIn(inertia_label), run_time=1)
        self.play(inertia_label.animate.scale(1.2).set_color(YELLOW), run_time=1)
        self.wait(2)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)), run_time=2)