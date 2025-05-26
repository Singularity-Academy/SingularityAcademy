from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#001f4d"  # 深蓝背景
        background_gradient = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color="#87CEEB", fill_opacity=1)
        background_gradient.set_fill("#001f4d", opacity=1)
        background_gradient.set_gradient(["#001f4d", "#87CEEB"], direction=UP)
        background_gradient.move_to(ORIGIN)
        self.add(background_gradient)

        # 标题
        title = Text("热力学第二定律", font_size=36, color=WHITE)
        subtitle = Text("孤立系统的熵总是增加或保持不变", font_size=24, color=WHITE)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(2)

        # 高温区和低温区矩形容器
        high_temp_rect = Rectangle(width=3, height=2, color=RED, fill_color=RED, fill_opacity=0.5)
        low_temp_rect = Rectangle(width=3, height=2, color=BLUE, fill_color=BLUE, fill_opacity=0.5)
        high_temp_rect.to_edge(LEFT)
        low_temp_rect.to_edge(RIGHT)

        self.play(FadeIn(high_temp_rect), FadeIn(low_temp_rect))
        self.wait(1)

        # 分子模拟
        num_molecules = 20
        high_temp_molecules = VGroup(*[Dot(color=RED).move_to(high_temp_rect.get_center() + np.random.random(2) * 2 - 1) for _ in range(num_molecules)])
        low_temp_molecules = VGroup(*[Dot(color=BLUE).move_to(low_temp_rect.get_center() + np.random.random(2) * 2 - 1) for _ in range(num_molecules)])

        self.play(FadeIn(high_temp_molecules), FadeIn(low_temp_molecules))
        self.wait(1)

        # 分子运动
        for _ in range(3):
            self.play(
                *[molecule.animate.move_to(high_temp_rect.get_center() + np.random.random(2) * 2 - 1) for molecule in high_temp_molecules],
                *[molecule.animate.move_to(low_temp_rect.get_center() + np.random.random(2) * 2 - 1) for molecule in low_temp_molecules],
                run_time=1
            )

        # 热量流动动画
        arrow = Arrow(start=high_temp_rect.get_center(), end=low_temp_rect.get_center(), color=YELLOW)
        self.play(GrowArrow(arrow))
        self.wait(1)

        # 分子混合动画
        mixed_molecules = VGroup(*[Dot(color=PURPLE).move_to(np.random.random(2) * FRAME_WIDTH - FRAME_WIDTH / 2) for _ in range(num_molecules * 2)])
        self.play(
            Transform(high_temp_molecules, mixed_molecules),
            Transform(low_temp_molecules, mixed_molecules),
            run_time=2
        )
        self.wait(1)

        # 矩形颜色渐变到紫色
        final_rect = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=PURPLE, fill_color=PURPLE, fill_opacity=0.5)
        self.play(FadeOut(high_temp_rect), FadeOut(low_temp_rect), FadeIn(final_rect))
        self.wait(1)

        # 熵公式和解释文字
        entropy_formula = MathTex(r"\Delta S = \frac{Q}{T}", font_size=36, color=WHITE)
        entropy_formula.to_edge(DOWN)
        entropy_text = Text("熵增加", font_size=32, color=WHITE)
        entropy_text.next_to(entropy_formula, UP)

        self.play(Write(entropy_formula), Write(entropy_text))
        self.wait(2)

        # 总结文字
        summary_text = Text("热力学第二定律：孤立系统的熵总是增加或保持不变，体现自然过程的不可逆性。", font_size=24, color=WHITE)
        summary_text.to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(3)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))