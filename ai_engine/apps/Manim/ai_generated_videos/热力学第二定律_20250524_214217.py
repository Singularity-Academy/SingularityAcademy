from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLUE, fill_opacity=1)
        background.set_color_by_gradient(DARK_BLUE, BLUE)
        self.add(background)

        # 星点背景
        stars = VGroup(*[Dot(point=np.array([np.random.uniform(-7, 7), np.random.uniform(-4, 4), 0]),
                             color=WHITE, radius=0.03) for _ in range(100)])
        for star in stars:
            star.set_opacity(np.random.uniform(0.3, 0.7))
        self.add(stars)

        # 标题
        subtitle = Text("热力学第二定律", font_size=28, color=WHITE)
        subtitle.to_corner(DR)
        self.add(subtitle)

        # 初始化盒状系统
        box = Rectangle(width=6, height=3, color=WHITE)
        box.move_to(ORIGIN)

        # 左侧高温区域
        left_box = Rectangle(width=3, height=3, color=RED, fill_opacity=0.8).move_to(LEFT * 1.5)
        left_particles = VGroup(*[Dot(color=RED).move_to(left_box.get_center() + np.random.uniform(-1, 1, 2) * LEFT * 0.3]
---