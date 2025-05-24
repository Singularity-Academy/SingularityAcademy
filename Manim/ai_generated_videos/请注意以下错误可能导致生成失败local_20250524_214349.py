from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 标题
        title = Text("探索热力学第二定律：从混乱到秩序的限制", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景和孤立系统边框
        background = Rectangle(width=8, height=4.5, fill_color="#1E90FF", fill_opacity=0.6, color=WHITE)
        background.set_gradient("#1E90FF", "#FFA07A")
        self.play(Create(background))
        self.wait(1)

        isolated_system = Rectangle(width=7, height=4, color=WHITE)
        self.play(Create(isolated_system))
        self.wait(1)

        # 左侧高温热源容器和右侧低温容器
        high_temp_container = Rectangle(width=2, height=3, color=RED, fill_color=RED, fill_opacity=0.5)
        low_temp_container = Rectangle(width=2, height=3, color=BLUE, fill_color=BLUE, fill_opacity=0.5)
        high_temp_container.move_to(LEFT * 3)
        low_temp_container.move_to(RIGHT * 3)

        self.play(FadeIn(high_temp_container), FadeIn(low_temp_container))
        self.wait(1)

        # 箭头表示热量流动
        heat_flow_arrow = Arrow(start=LEFT * 1.5, end=RIGHT * 1.5, color=YELLOW, buff=0.5)
        heat_flow_label = Text("热量流动", font_size=24, color=YELLOW)
        heat_flow_label.next_to(heat_flow_arrow, UP)

        self.play(Create(heat_flow_arrow), Write(heat_flow_label))
        self.wait(1)

        # 热力学第二定律说明
        second_law_text = Text("孤立系统的熵不会减少", font_size=32, color=WHITE)
        second_law_text.move_to(DOWN * 2)

        self.play(Write(second_law_text))
        self.wait(1)

        # 动态展示热量粒子从高温容器到低温容器
        particles = VGroup(*[Dot(color=RED).move_to(high_temp_container.get_center() + np.random.uniform(-1, 1, 2)) for _ in range(10)])
        self.play(FadeIn(particles))
        self.wait(1)

        for particle in particles:
            self.play(particle.animate.move_to(low_temp_container.get_center() + np.random.uniform(-1, 1, 2)), run_time=0.5)
        self.wait(1)

        # 熵变化公式和文字解释
        entropy_formula = MathTex(r"\Delta S = \frac{Q}{T}", font_size=36)
        entropy_formula.move_to(DOWN * 2 + LEFT * 3)

        entropy_explanation = Text("熵是系统中混乱程度的度量", font_size=24, color=WHITE)
        entropy_explanation.next_to(entropy_formula, RIGHT)

        self.play(Write(entropy_formula), Write(entropy_explanation))
        self.wait(1)

        # 系统达到热平衡状态
        equilibrium_color = ORANGE
        high_temp_container.set_fill(color=equilibrium_color, opacity=0.8)
        low_temp_container.set_fill(color=equilibrium_color, opacity=0.8)

        self.play(
            high_temp_container.animate.set_fill(color=equilibrium_color),
            low_temp_container.animate.set_fill(color=equilibrium_color),
            run_time=2
        )
        self.wait(1)

        # 动态展示熵值增加
        entropy_increase_text = Text("熵值增加", font_size=32, color=WHITE)
        entropy_increase_text.move_to(UP * 2)

        self.play(Write(entropy_increase_text))
        self.wait(1)

        # 时间轴展示变化过程
        time_axis = Line(start=LEFT * 4, end=RIGHT * 4, color=WHITE)
        initial_state = Text("初始状态", font_size=24, color=BLUE).next_to(time_axis, UP).to_edge(LEFT)
        final_state = Text("最终状态", font_size=24, color=ORANGE).next_to(time_axis, UP).to_edge(RIGHT)

        self.play(Create(time_axis), Write(initial_state), Write(final_state))
        self.wait(1)

        # 强调自然界不可逆性
        conclusion_text = Text("热力学第二定律揭示了自然界的不可逆性", font_size=32, color=WHITE)
        conclusion_text.move_to(DOWN * 2)

        self.play(Write(conclusion_text))
        self.wait(2)

        # 结束
        self.play(FadeOut(VGroup(*self.mobjects)))