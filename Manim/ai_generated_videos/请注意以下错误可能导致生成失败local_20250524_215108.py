from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 标题
        title = Text("Second Law of Thermodynamics", font_size=36, color=WHITE)
        title.to_corner(UL)
        self.play(Write(title))
        
        # 背景渐变色
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color=BLUE, fill_opacity=1)
        background.set_gradient(start_color=BLUE, end_color=PURPLE)
        self.add(background)

        # 盒子
        box = Rectangle(width=6, height=3, color=WHITE)
        box.move_to(ORIGIN)
        self.play(Create(box))

        # 左侧粒子有序排列
        particles = VGroup(*[Dot(color=BLUE) for _ in range(30)])
        particles.arrange_in_grid(rows=5, cols=6, buff=0.3)
        particles.move_to(box.get_left() + RIGHT * 1.5)
        self.play(FadeIn(particles))

        # 初始状态标签
        initial_label = Text("Initial State: High Order, Low Entropy", font_size=24, color=WHITE)
        initial_label.next_to(box, DOWN)
        self.play(Write(initial_label))
        self.wait(2)

        # 时间轴
        time_axis = Line(start=LEFT * 3, end=RIGHT * 3, color=RED)
        time_axis.shift(DOWN * 2)
        time_arrow = Arrow(start=LEFT * 3, end=RIGHT * 3, color=RED, buff=0)
        time_label = Text("Time Progression", font_size=24, color=RED)
        time_label.next_to(time_arrow, UP)
        self.play(Create(time_arrow), Write(time_label))

        # 粒子扩散动画
        self.play(
            particles.animate.arrange_in_grid(rows=3, cols=10, buff=0.5).move_to(box.get_center()),
            run_time=10,
            rate_func=smooth
        )
        self.wait(2)

        # 公式展示
        entropy_formula = MathTex(r"S = k_B \ln \Omega", font_size=48)
        entropy_formula.move_to(UP * 2)
        second_law_formula = MathTex(r"\Delta S \geq 0", font_size=48)
        second_law_formula.next_to(entropy_formula, DOWN, buff=0.5)
        self.play(FadeIn(entropy_formula), FadeIn(second_law_formula))
        self.wait(3)

        # 最终状态标签
        final_label = Text("Entropy Increases: Irreversible Process", font_size=24, color=WHITE)
        final_label.next_to(box, DOWN)
        self.play(Transform(initial_label, final_label))
        self.wait(2)

        # 箭头连接初始状态和最终状态
        arrow = Arrow(start=particles.get_left() + LEFT * 0.5, end=particles.get_right() + RIGHT * 0.5, color=YELLOW)
        self.play(Create(arrow))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))