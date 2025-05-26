from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 标题
        title = Text("热力学第二定律：从混乱到秩序的故事", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景渐变
        gradient_rect = Rectangle(width=14, height=8)
        gradient_rect.set_fill(color=[BLUE, ORANGE], opacity=0.3)
        gradient_rect.set_stroke(width=0)
        self.add(gradient_rect)

        # 矩形容器
        container = Rectangle(width=8, height=4, color=WHITE)
        container.move_to(DOWN * 1.5)
        self.play(Create(container), run_time=2)

        # 初始分子（低熵状态）
        molecules = VGroup(*[Dot(color=BLUE).scale(0.5) for _ in range(20)])
        for i, dot in enumerate(molecules):
            dot.move_to(container.get_left() + RIGHT * 0.5 + RIGHT * (i % 5) * 0.5 + UP * (i // 5) * 0.5)
        self.play(FadeIn(molecules))
        self.wait(1)

        # 初始状态标签
        initial_label = Text("初始低熵状态", font_size=28, color=BLUE)
        initial_label.next_to(container, UP)
        self.play(Write(initial_label))
        self.wait(1)

        # 分子扩散动画
        def random_position_in_container():
            x = np.random.uniform(-4, 4)
            y = np.random.uniform(-2, 2)
            return container.get_center() + RIGHT * x + UP * y
        
        self.play(FadeOut(initial_label))
        for dot in molecules:
            self.play(dot.animate.move_to(random_position_in_container()).set_color(ORANGE), run_time=0.5)
        self.wait(1)

        # 最终状态标签
        final_label = Text("最终高熵状态", font_size=28, color=ORANGE)
        final_label.next_to(container, UP)
        self.play(Write(final_label))
        self.wait(1)

        # 熵公式展示
        entropy_formula = MathTex(r"S = k \ln \Omega", font_size=48, color=WHITE)
        entropy_formula.to_edge(UP)
        self.play(Write(entropy_formula))
        self.wait(1)

        # 熵公式解释
        explanation = Text("微观状态数量增加导致熵增加", font_size=28, color=WHITE)
        explanation.next_to(entropy_formula, DOWN)
        self.play(Write(explanation))
        self.wait(2)

        # 热力学第二定律文字浮现
        second_law_text = Text("孤立系统的熵总是趋于增加", font_size=32, color=WHITE)
        second_law_text.move_to(DOWN * 2)
        time_arrow = Arrow(start=LEFT * 4, end=RIGHT * 4, color=YELLOW, stroke_width=3)
        self.play(Write(second_law_text), Create(time_arrow))
        self.wait(2)

        # 总结文字
        summary = Text("熵是宇宙的方向", font_size=36, color=WHITE)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)

        # 结束
        self.play(FadeOut(VGroup(*self.mobjects)))