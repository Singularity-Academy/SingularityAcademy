from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color="#001f4d", fill_opacity=1).set_z_index(-1)
        stars = VGroup(*[Dot(point=np.random.uniform(-6, 6, size=3), color=WHITE).scale(0.3) for _ in range(50)])
        light_glow = Circle(radius=1.5, color=YELLOW, fill_opacity=0.3).set_z_index(-1).move_to(ORIGIN)

        self.add(background, stars, light_glow)

        # 热库设置
        hot_reservoir = Rectangle(width=2, height=3, color=RED, fill_color=RED, fill_opacity=0.5).shift(LEFT*4)
        cold_reservoir = Rectangle(width=2, height=3, color=BLUE, fill_color=BLUE, fill_opacity=0.5).shift(RIGHT*4)

        self.play(FadeIn(hot_reservoir), FadeIn(cold_reservoir))

        # 粒子设置与动画
        hot_particles = VGroup(*[Dot(color=RED).move_to(hot_reservoir.get_center() + np.random.uniform(-1, 1, size=2)) for _ in range(20)])
        cold_particles = VGroup(*[Dot(color=BLUE).move_to(cold_reservoir.get_center() + np.random.uniform(-1, 1, size=2)) for _ in range(20)])

        self.play(FadeIn(hot_particles), FadeIn(cold_particles))
        self.wait(1)

        # 标题文字
        title = Text("热力学第二定律", font_size=48, color=WHITE).move_to(UP*3)
        self.play(Write(title))
        self.wait(1)

        # 能量流动动画
        energy_arrow = Arrow(start=hot_reservoir.get_right(), end=cold_reservoir.get_left(), color=YELLOW, stroke_width=4)
        self.play(Create(energy_arrow))
        self.wait(1)

        # 粒子扩散动画
        all_particles = VGroup(hot_particles, cold_particles)
        self.play(
            hot_particles.animate.arrange(RIGHT, buff=0.5).move_to(ORIGIN),
            cold_particles.animate.arrange(RIGHT, buff=0.5).move_to(ORIGIN),
            run_time=3
        )
        self.wait(1)

        # 公式展示
        entropy_formula = MathTex(r"\Delta S = S_{\text{final}} - S_{\text{initial}} \geq 0", font_size=36).move_to(DOWN*2)
        self.play(Write(entropy_formula))

        # 熵增条形图
        entropy_bar = Rectangle(width=0.5, height=2, color=GREEN, fill_color=GREEN, fill_opacity=0.8).move_to(DOWN*1)
        entropy_label = Text("熵增", font_size=24, color=WHITE).next_to(entropy_bar, UP)

        self.play(Write(entropy_label), Create(entropy_bar))
        self.wait(1)

        # 时间箭头
        time_arrow = Arrow(start=LEFT*6, end=RIGHT*6, color=ORANGE, stroke_width=4).move_to(DOWN*3)
        time_text = Text("时间的不可逆性", font_size=24, color=WHITE).next_to(time_arrow, UP)

        self.play(Create(time_arrow), Write(time_text))
        self.wait(1)

        # 混合展示
        self.play(FadeOut(energy_arrow), FadeOut(entropy_bar), FadeOut(entropy_label))
        mixed_particles = VGroup(*[Dot(color=np.random.choice([RED, BLUE])).move_to(np.random.uniform(-4, 4, size=2)) for _ in range(40)])
        self.play(Transform(all_particles, mixed_particles))
        self.wait(1)

        # 总结文字
        summary = VGroup(
            Text("热力学第二定律", font_size=36, color=WHITE),
            entropy_formula.copy(),
            Text("熵增：宇宙的自然法则", font_size=24, color=WHITE)
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN)

        self.play(Write(summary))
        self.wait(2)

        # 淡出场景
        self.play(FadeOut(VGroup(*self.mobjects)))