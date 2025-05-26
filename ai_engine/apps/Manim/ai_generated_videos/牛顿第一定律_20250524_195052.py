from manim import *

class NewtonFirstLawScene(Scene):
    def construct(self):
        # 场景标题
        title = Text("牛顿第一定律", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 引入牛顿第一定律描述
        description = Text("物体保持静止或以匀速直线运动，除非受到外力作用。", font_size=28, color=WHITE)
        description.next_to(title, DOWN, buff=0.5)
        self.play(Write(description))
        self.wait(2)
        self.play(FadeOut(description))

        # 背景平面
        plane = NumberPlane(x_range=(-7, 7), y_range=(-4, 4), background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.3})
        self.play(Create(plane))
        self.wait(1)

        # 静止的绿色球
        ball = Dot(color=GREEN).shift(LEFT * 3)
        inertia_label = Text("惯性", font_size=24, color=WHITE).next_to(ball, UP, buff=0.5)
        self.play(FadeIn(ball), Write(inertia_label))
        self.wait(1)

        # 镜头缓慢放大，强调球的静止状态
        self.play(self.camera.frame.animate.scale(0.8).move_to(ball), run_time=2)
        self.wait(1)
        self.play(self.camera.frame.animate.scale(1).move_to(ORIGIN), run_time=2)

        # 匀速运动的蓝色箱子
        box = Rectangle(width=1.5, height=1, color=BLUE, fill_color=BLUE, fill_opacity=1).shift(LEFT * 7)
        motion_label = Text("匀速直线运动", font_size=24, color=WHITE).next_to(box, UP, buff=0.5)
        self.play(FadeIn(box), Write(motion_label))
        self.wait(1)

        # 蓝色箱子匀速运动
        self.play(box.animate.shift(RIGHT * 10), motion_label.animate.shift(RIGHT * 10), run_time=4, rate_func=linear)
        self.wait(1)

        # 显示公式 F = 0 ⇒ v = constant
        formula_constant = MathTex(r"F = 0 \Rightarrow v = \text{constant}", color=WHITE).to_edge(DOWN)
        self.play(Write(formula_constant))
        self.wait(2)

        # 施加外力改变运动状态
        force_arrow = Arrow(start=RIGHT * 4, end=RIGHT * 6, color=RED, stroke_width=6)
        self.play(GrowArrow(force_arrow))
        self.wait(1)

        # 箱子加速运动
        self.play(box.animate.shift(RIGHT * 5).scale(1.1), motion_label.animate.shift(RIGHT * 5).scale(1.1), run_time=2, rate_func=rush_into)
        self.wait(1)

        # 更新公式 F ≠ 0 ⇒ v changes
        formula_change = MathTex(r"F \neq 0 \Rightarrow v \text{ changes}", color=WHITE).next_to(formula_constant, UP, buff=0.5)
        self.play(Transform(formula_constant, formula_change))
        self.wait(2)

        # 加速后文字标签“外力影响”
        force_label = Text("外力影响", font_size=24, color=WHITE).next_to(force_arrow, UP, buff=0.5)
        self.play(Write(force_label))
        self.wait(1)

        # 总结与回顾
        summary_label = Text("牛顿第一定律", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Transform(title, summary_label))
        self.wait(1)

        # 将静止的球和运动的箱子并列展示
        self.play(ball.animate.shift(LEFT * 2), box.animate.shift(LEFT * 4), run_time=2)
        self.play(FadeOut(force_arrow), FadeOut(force_label), FadeOut(formula_constant), FadeOut(motion_label), FadeOut(inertia_label))
        self.wait(1)

        # 最后闪烁标题
        self.play(title.animate.set_opacity(0.2).set_opacity(1).set_opacity(0.2).set_opacity(1), run_time=2)
        self.wait(2)