from manim import *

class NewtonFirstLaw(Scene):
    def construct(self):
        # 设置背景和地面
        self.camera.background_color = "#00008B"  # 深蓝色背景
        stars = VGroup(*[Dot(color=WHITE, radius=0.002) for _ in range(200)])
        for star in stars:
            star.move_to([self.random.uniform(-7, 7), self.random.uniform(-4, 4), 0])
            star.set_opacity(self.random.uniform(0.2, 0.8))
        self.add(stars)
        
        ground = Rectangle(width=14, height=2, color=GRAY, fill_opacity=0.3).shift(DOWN * 3)
        self.add(ground)

        # 第一阶段：静止状态
        ball = Circle(radius=0.5, color=WHITE, fill_opacity=1).shift(DOWN * 2)
        velocity_arrow = Arrow(start=ball.get_center(), end=ball.get_center(), color=GREEN)
        static_label = Text("静止状态（No Force）", font_size=24, color=YELLOW).next_to(ball, UP)

        formula_static = MathTex(r"F = 0 \rightarrow v = \text{constant}", color=WHITE).to_edge(UP)
        
        self.play(FadeIn(ball), FadeIn(static_label))
        self.play(Write(formula_static))
        self.wait(2)

        # 第二阶段：匀速运动状态
        self.play(FadeOut(static_label))
        moving_label = Text("匀速运动（No Force）", font_size=24, color=YELLOW).next_to(ball, UP)
        velocity_arrow = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT * 2, color=GREEN)
        self.play(Write(moving_label), GrowArrow(velocity_arrow))
        self.wait(1)

        self.play(ball.animate.shift(RIGHT * 4), stars.animate.shift(LEFT * 0.5), run_time=3)
        self.wait(2)

        # 第三阶段：外力作用
        self.play(FadeOut(moving_label))
        force_arrow = Arrow(start=ball.get_center() + LEFT * 0.5, end=ball.get_center(), color=RED)
        stop_label = Text("停止（Force Applied）", font_size=24, color=YELLOW).next_to(ball, UP)
        formula_force = MathTex(r"F \neq 0 \rightarrow v \, \text{changes}", color=WHITE).to_edge(UP)

        self.play(GrowArrow(force_arrow), Write(stop_label))
        self.play(ball.animate.shift(LEFT * 2), FadeOut(velocity_arrow), run_time=2)
        self.play(Transform(formula_static, formula_force))
        self.wait(2)

        # 总结阶段：惯性定律总结
        self.play(FadeOut(stop_label), FadeOut(force_arrow))
        summary_text = Text("牛顿第一定律：惯性定律", font_size=32, color=WHITE).to_edge(DOWN)

        self.play(FadeIn(summary_text))
        self.wait(1)
        self.play(summary_text.animate.scale(1.2).set_opacity(0.5).set_opacity(1), run_time=1.5)
        self.wait(2)

        # 整体淡出
        self.play(FadeOut(Group(*self.mobjects)))