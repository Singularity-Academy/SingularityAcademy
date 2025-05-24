from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#1E1E99"  # 深蓝色背景
        stars = VGroup(*[Dot(point=np.random.random(3) * 7 - 3.5, color=WHITE, radius=0.02) for _ in range(100)])
        self.add(stars)

        # 热力学第二定律标签
        label = Text("热力学第二定律", font_size=24, color=WHITE)
        label.to_corner(DR)
        self.add(label)

        # 介绍性文字
        intro_text = Text("热力学第二定律指出，系统的熵总是增加。", font_size=32, color=WHITE)
        self.play(FadeIn(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))

        # 容器和分隔板
        container = Rectangle(width=6, height=3, color=WHITE)
        separator = Line(start=UP * 1.5, end=DOWN * 1.5, color=GRAY)
        self.play(Create(container), Create(separator))
        self.wait(1)

        # 初始气体分子
        particles_left = VGroup(*[Dot(point=LEFT * np.random.random() * 2.5 + np.random.random(3) * 0.5, color=BLUE, radius=0.1) for _ in range(30)])
        self.play(FadeIn(particles_left))
        self.wait(1)

        # 淡出分隔板
        self.play(FadeOut(separator))
        self.wait(1)

        # 熵值文字
        s_left_text = Text("S_left", font_size=24, color=GREEN).move_to(LEFT * 3.5 + UP * 2)
        s_right_text = Text("S_right", font_size=24, color=GREEN).move_to(RIGHT * 3.5 + UP * 2)
        s_total_text = Text("S_total", font_size=24, color=GREEN).move_to(UP * 3)

        self.play(FadeIn(s_left_text), FadeIn(s_right_text), FadeIn(s_total_text))

        # 粒子扩散动画
        particles_right = VGroup(*[Dot(point=RIGHT * np.random.random() * 2.5 + np.random.random(3) * 0.5, color=BLUE, radius=0.1) for _ in range(30)])
        for i, particle in enumerate(particles_left):
            self.play(particle.animate.move_to(particles_right[i].get_center()), run_time=0.1)

        self.wait(1)

        # 更新熵值
        s_left_update = Text("S_left ↓", font_size=24, color=GREEN).move_to(s_left_text.get_center())
        s_right_update = Text("S_right ↑", font_size=24, color=GREEN).move_to(s_right_text.get_center())
        s_total_update = Text("S_total ↑", font_size=24, color=GREEN).move_to(s_total_text.get_center())

        self.play(Transform(s_left_text, s_left_update), Transform(s_right_text, s_right_update), Transform(s_total_text, s_total_update))
        self.wait(1)

        # 公式展示
        formula = MathTex(r"\Delta S \geq 0", font_size=48, color=WHITE)
        formula.scale(1.5)
        self.play(Write(formula))
        self.wait(2)

        # 总结性文字
        summary_text = Text("熵的增加意味着自然过程的不可逆性。热力学第二定律塑造了我们的宇宙。", font_size=32, color=WHITE)
        summary_text.move_to(DOWN * 2)
        self.play(FadeIn(summary_text))
        self.wait(3)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))