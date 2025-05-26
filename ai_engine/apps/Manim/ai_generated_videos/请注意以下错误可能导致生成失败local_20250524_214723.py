from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 标题
        title = Text("热力学第二定律的视觉解读", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景颜色渐变
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT)
        background.set_fill(
            color=["#00008B", "#FF4500"],  # 深蓝到橙红渐变
            opacity=1
        )
        background.set_stroke(opacity=0)
        self.add(background)

        # 冷区和热区
        cold_zone = Text("冷区", font_size=24, color=BLUE)
        hot_zone = Text("热区", font_size=24, color=RED)
        cold_zone.to_edge(LEFT)
        hot_zone.to_edge(RIGHT)
        self.play(Write(cold_zone), Write(hot_zone))
        self.wait(1)

        # 初始分子分布
        molecules_cold = VGroup(*[Dot(color=BLUE) for _ in range(10)])
        molecules_hot = VGroup(*[Dot(color=RED) for _ in range(10)])
        molecules_cold.arrange_in_grid(rows=2, cols=5, buff=0.5).move_to(LEFT*3)
        molecules_hot.arrange_in_grid(rows=2, cols=5, buff=0.5).move_to(RIGHT*3)
        self.play(FadeIn(molecules_cold), FadeIn(molecules_hot))
        self.wait(1)

        # 孤立系统边框
        system_border = Rectangle(width=12, height=6, color=WHITE, stroke_width=2)
        self.play(Create(system_border))
        self.wait(1)

        # 分子混合动画
        molecules = molecules_cold.copy()
        molecules.add(*molecules_hot.copy())
        for molecule in molecules:
            new_position = np.random.random(3) * 6 - 3  # 随机移动
            self.play(molecule.animate.move_to(new_position), run_time=0.5)

        self.wait(1)

        # 显示熵公式
        entropy_formula = MathTex(r"S = k_B \ln \Omega", font_size=48)
        entropy_formula.to_edge(DOWN)
        self.play(Write(entropy_formula))
        self.wait(1)

        # 动态增加微观态数量
        omega_values = [10, 100, 1000, 10000]
        omega_texts = [
            Text(f"Ω = {value}", font_size=24, color=YELLOW)
            for value in omega_values
        ]
        for omega_text in omega_texts:
            omega_text.next_to(entropy_formula, UP, buff=0.5)
            self.play(Write(omega_text))
            self.wait(0.5)
            self.play(FadeOut(omega_text))

        # 熵增加不可逆性
        arrow = Arrow(start=LEFT, end=RIGHT, color=WHITE)
        arrow.next_to(entropy_formula, UP, buff=1)
        increase_text = Text("熵增加", font_size=32, color=ORANGE)
        increase_text.next_to(arrow, UP)
        self.play(Create(arrow), Write(increase_text))
        self.wait(1)

        # 背景颜色变化
        self.play(
            background.animate.set_fill(
                color=["#FF4500", "#FF6347"],  # 混合橙色
                opacity=1
            ),
            run_time=2
        )
        self.wait(1)

        # 总结文字
        summary = Text("孤立系统的熵总是增加或保持不变", font_size=28, color=WHITE)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))