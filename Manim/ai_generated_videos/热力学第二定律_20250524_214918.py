from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#001f3f"  # 深蓝色背景
        stars = VGroup(*[
            Dot(point=np.array([
                np.random.uniform(-7, 7),
                np.random.uniform(-4, 4),
                0
            ]), radius=0.02, color=WHITE).set_opacity(0.5)
            for _ in range(100)
        ])
        self.add(stars)
        
        # 标题
        title = Text("热力学第二定律：从混乱到秩序的故事", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 玻璃盒子
        box = Rectangle(width=6, height=4, color=WHITE, fill_opacity=0.1)
        self.play(Create(box))
        self.wait(1)

        # 分子粒子
        num_particles = 50
        particles = VGroup(*[
            Dot(point=np.array([
                np.random.uniform(-2.5, -1),  # 初始红色粒子在左侧
                np.random.uniform(-1.8, 1.8),
                0
            ]), radius=0.1, color=RED) for _ in range(num_particles // 2)
        ] + [
            Dot(point=np.array([
                np.random.uniform(1, 2.5),  # 初始蓝色粒子在右侧
                np.random.uniform(-1.8, 1.8),
                0
            ]), radius=0.1, color=BLUE) for _ in range(num_particles // 2)
        ])
        self.play(FadeIn(particles))
        self.wait(1)

        # 粒子运动和扩散
        def update_particles(mobject, dt):
            for dot in mobject:
                dot.shift(np.array([
                    np.random.uniform(-0.1, 0.1),
                    np.random.uniform(-0.1, 0.1),
                    0
                ]))
        particles.add_updater(update_particles)
        self.wait(5)
        particles.remove_updater(update_particles)

        # 熵条形图
        entropy_chart = BarChart(
            values=[1, 2, 3, 4, 5],  # 模拟熵增加
            max_value=5,
            bar_colors=[YELLOW],
            width=4, height=2
        )
        entropy_chart.move_to(box.get_bottom() + DOWN * 1.5)
        self.play(FadeIn(entropy_chart))
        self.wait(1)

        # 模拟熵增长
        for i in range(1, 6):
            self.play(entropy_chart.animate.set_values([i]), run_time=1)

        # 热量流动箭头
        arrow = Arrow(start=box.get_left() + LEFT * 0.5, end=box.get_right() + RIGHT * 0.5, color=ORANGE, stroke_width=4)
        self.play(Create(arrow))
        self.wait(1)

        # 温度计
        thermometer = Rectangle(width=0.5, height=3, color=WHITE, fill_opacity=0.2)
        thermometer.move_to(box.get_right() + RIGHT * 1.5)
        self.play(FadeIn(thermometer))
        red_bar = Rectangle(width=0.5, height=0.5, color=RED, fill_opacity=1)
        red_bar.move_to(thermometer.get_bottom() + UP * 0.25)
        self.add(red_bar)
        for i in range(1, 6):
            red_bar.scale(1 + i * 0.1, about_edge=DOWN)
            self.wait(0.5)

        # 公式展示
        formula = MathTex(r"\Delta S \geq 0", font_size=48, color=WHITE)
        formula.move_to(UP * 2)
        self.play(Write(formula))
        self.wait(1)

        # 定格展示
        final_text = Text("熵是时间之箭", font_size=36, color=WHITE)
        final_text.move_to(DOWN * 2)
        self.play(Write(final_text))
        self.wait(2)

        # 结束
        self.play(FadeOut(VGroup(*self.mobjects)))