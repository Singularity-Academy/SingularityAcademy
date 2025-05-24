from manim import *

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 场景背景设置
        self.camera.background_color = DARK_BLUE
        # 星空粒子效果
        stars = VGroup(*[Dot(color=WHITE).shift(2 * UP).set_opacity(0.2).scale(0.5) for _ in range(50)])
        for star in stars:
            star.move_to(self.frame_center + np.random.uniform(-6, 6) * RIGHT + np.random.uniform(-3, 3) * UP)
        self.play(FadeIn(stars), run_time=2)

        # 中文标题
        title = Text("热力学第二定律", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建两个方块（红色高温物体，蓝色低温物体）
        red_square = Square(color=RED, fill_opacity=0.9).scale(1.5).shift(3 * LEFT)
        blue_square = Square(color=BLUE, fill_opacity=0.9).scale(1.5).shift(3 * RIGHT)
        self.play(FadeIn(red_square), FadeIn(blue_square), run_time=1.5)
        
        # 热量流动箭头
        heat_arrow = Arrow(start=red_square.get_right(), end=blue_square.get_left(), color=YELLOW, buff=0.2)
        self.play(GrowArrow(heat_arrow))
        self.wait(1)

        # 动态展示热量流动过程
        self.play(
            red_square.animate.set_fill(color=RED, opacity=0.5),
            blue_square.animate.set_fill(color=BLUE, opacity=1),
            run_time=3,
        )

        # 添加代表粒子的点
        red_particles = VGroup(*[Dot(color=RED).scale(0.5) for _ in range(10)])
        blue_particles = VGroup(*[Dot(color=BLUE).scale(0.5) for _ in range(10)])
        
        for particle in red_particles:
            particle.move_to(red_square.get_center() + np.random.uniform(-1, 1) * RIGHT + np.random.uniform(-1, 1) * UP)
        for particle in blue_particles:
            particle.move_to(blue_square.get_center() + np.random.uniform(-1, 1) * RIGHT + np.random.uniform(-1, 1) * UP)
        
        self.play(FadeIn(red_particles), FadeIn(blue_particles), run_time=1)
        
        # 粒子从红色方块流向蓝色方块
        self.play(
            red_particles.animate.arrange_in_grid(cols=1).shift(6 * RIGHT),
            blue_particles.animate.arrange_in_grid(cols=3).shift(LEFT * 0.5),
            run_time=3,
        )

        # 熵计量器
        entropy_meter = VGroup(
            Rectangle(height=4, width=1, color=WHITE, fill_opacity=0.5).shift(3 * DOWN + 5 * RIGHT),
            Rectangle(height=0.5, width=1, color=GREEN, fill_opacity=1).align_to(entropy_meter[0], DOWN)
        )
        entropy_label = Text("熵计量器", font_size=24).next_to(entropy_meter, DOWN)
        self.play(FadeIn(entropy_meter), Write(entropy_label))
        self.wait(1)

        # 动态更新熵计量器高度
        entropy_bar = entropy_meter[1]
        self.play(entropy_bar.animate.scale(2, about_edge=DOWN), run_time=3)

        # 熵公式展示
        entropy_formula = MathTex(r"\Delta S = \frac{Q}{T}").next_to(entropy_meter, UP)
        self.play(Write(entropy_formula))
        self.wait(2)

        # 不可逆性强调
        irreversible_text = Text("孤立系统：熵总是增加，过程不可逆", font_size=28, color=YELLOW)
        self.play(FadeIn(irreversible_text.to_edge(DOWN)))
        self.wait(2)

        # 结束场景
        summary_text = Text("热力学第二定律：自然的方向是从秩序到混乱", font_size=32, color=WHITE)
        self.play(FadeOut(Group(title, red_square, blue_square, heat_arrow, red_particles, blue_particles, entropy_meter, entropy_label, entropy_formula, irreversible_text)))
        self.play(FadeIn(summary_text))
        self.wait(3)

        # 淡出星空背景
        self.play(FadeOut(stars), run_time=2)