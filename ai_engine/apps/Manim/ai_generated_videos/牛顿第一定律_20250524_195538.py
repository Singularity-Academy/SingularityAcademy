from manim import *

class NewtonFirstLawScene(Scene):
    def construct(self):
        # 设置背景颜色和地平线
        self.camera.background_color = "#87CEEB"  # 浅蓝色背景
        ground_line = Line(start=LEFT * 6, end=RIGHT * 6, color=WHITE)
        ground_line.shift(DOWN * 2)
        self.add(ground_line)

        # 场景1：静止的球
        ball = Circle(radius=0.5, color=WHITE, fill_opacity=1).shift(DOWN * 1.5)
        ball_text = Text("静止的物体保持静止", font_size=24, color=WHITE).to_edge(DOWN)
        self.play(FadeIn(ball), Write(ball_text))
        self.wait(5)

        # 场景2：匀速运动的小车
        self.play(FadeOut(ball), FadeOut(ball_text))
        car = Rectangle(width=2, height=1, color=RED, fill_opacity=1).shift(LEFT * 5 + DOWN * 1.5)
        wheels = VGroup(
            Circle(radius=0.2, color=BLACK, fill_opacity=1).next_to(car, DOWN, buff=0.1).shift(LEFT * 0.6),
            Circle(radius=0.2, color=BLACK, fill_opacity=1).next_to(car, DOWN, buff=0.1).shift(RIGHT * 0.6),
        )
        car_group = VGroup(car, wheels)
        car_text = Text("匀速运动的物体保持匀速运动", font_size=24, color=WHITE).to_edge(DOWN)
        self.play(FadeIn(car_group), Write(car_text))
        self.play(car_group.animate.shift(RIGHT * 10), run_time=5, rate_func=linear)
        self.wait(2)
        self.play(FadeOut(car_group), FadeOut(car_text))

        # 场景3：外力作用改变球的状态
        ball = Circle(radius=0.5, color=WHITE, fill_opacity=1).shift(DOWN * 1.5)
        self.play(FadeIn(ball))
        force_arrow = Arrow(start=ball.get_center() + LEFT * 1, end=ball.get_center(), color=YELLOW, buff=0.1)
        force_text = Text("外力作用改变物体的速度", font_size=24, color=WHITE).to_edge(DOWN)
        self.play(GrowArrow(force_arrow), Write(force_text))
        self.play(ball.animate.shift(RIGHT * 5), run_time=3, rate_func=rush_into)
        self.wait(2)
        self.play(FadeOut(force_arrow), FadeOut(force_text))

        # 场景4：公式展示
        formula = MathTex(r"F = 0 \Rightarrow v = \text{constant}", font_size=48, color=WHITE)
        self.play(Write(formula))
        self.wait(2)

        # 场景5：总结
        self.play(FadeOut(formula))
        ball = Circle(radius=0.5, color=WHITE, fill_opacity=1).shift(LEFT * 3 + DOWN * 1.5)
        car = Rectangle(width=2, height=1, color=RED, fill_opacity=1).shift(RIGHT * 3 + DOWN * 1.5)
        wheels = VGroup(
            Circle(radius=0.2, color=BLACK, fill_opacity=1).next_to(car, DOWN, buff=0.1).shift(LEFT * 0.6),
            Circle(radius=0.2, color=BLACK, fill_opacity=1).next_to(car, DOWN, buff=0.1).shift(RIGHT * 0.6),
        )
        car_group = VGroup(car, wheels)
        summary_text = Text("牛顿第一定律：惯性的力量", font_size=36, color=WHITE)
        self.play(FadeIn(ball), FadeIn(car_group), Write(summary_text))
        self.wait(3)
        self.play(FadeOut(Group(ball, car_group, summary_text)))

        self.wait(1)