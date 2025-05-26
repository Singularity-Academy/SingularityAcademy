from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#0D1B2A"  # 深蓝色背景
        stars = VGroup(*[Dot(point=np.random.random(3) * 7 - 3.5, color=WHITE, radius=0.02) for _ in range(50)])
        self.add(stars)

        # 标题
        title = Text("热力学第二定律", font_size=48, color=WHITE)
        subtitle = Text("从混乱到秩序的不可逆性", font_size=32, color=WHITE)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(title), Write(subtitle))
        self.wait(2)

        # 容器
        left_container = Rectangle(width=3, height=3, color=RED)
        right_container = Rectangle(width=3, height=3, color=BLUE)
        left_container.move_to(LEFT * 2)
        right_container.move_to(RIGHT * 2)
        divider = Line(start=UP * 1.5 + LEFT, end=DOWN * 1.5 + LEFT, color=WHITE)

        # 初始粒子分布
        red_particles = VGroup(*[Dot(radius=0.1, color=RED).move_to(
            LEFT * 2 + np.random.random(2) * 1.5 - 0.75) for _ in range(15)])
        blue_particles = VGroup(*[Dot(radius=0.1, color=BLUE).move_to(
            RIGHT * 2 + np.random.random(2) * 1.5 - 0.75) for _ in range(15)])

        # 添加初始状态
        self.play(Create(left_container), Create(right_container), Create(divider))
        self.play(FadeIn(red_particles), FadeIn(blue_particles))
        self.wait(2)

        # 熵增加：分隔壁消失，粒子开始扩散
        self.play(FadeOut(divider))
        self.wait(1)
        for particle in red_particles:
            self.play(particle.animate.move_to(
                np.random.random(2) * 4 - 2), run_time=0.5)
        for particle in blue_particles:
            self.play(particle.animate.move_to(
                np.random.random(2) * 4 - 2), run_time=0.5)
        self.wait(2)

        # 展示公式
        formula = MathTex(r"dS \geq 0", font_size=48, color=WHITE)
        formula.to_edge(DOWN)
        arrow = Arrow(start=LEFT, end=RIGHT, color=YELLOW)
        arrow.next_to(formula, UP, buff=0.3)
        self.play(Write(formula), Create(arrow))
        self.wait(2)

        # 熵曲线展示
        entropy_curve = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 5, 1],
            axis_config={"color": WHITE}
        ).move_to(DOWN * 2 + RIGHT * 2)
        entropy_label = entropy_curve.get_y_axis_label("熵 (S)", direction=LEFT, buff=0.4)
        time_label = entropy_curve.get_x_axis_label("时间 (t)", direction=DOWN, buff=0.4)

        # 曲线
        curve = entropy_curve.plot(lambda x: 0.5 * x + 1, x_range=[0, 9], color=ORANGE)
        self.play(Create(entropy_curve), Write(entropy_label), Write(time_label))
        self.play(Create(curve))
        self.wait(2)

        # 结束总结
        summary = Text("熵增加是一种不可逆的自然现象，是热力学第二定律的核心", font_size=32, color=WHITE)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(3)

        # 清除场景
        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(1)