from manim import *

class IrreversibleEntropyScene(Scene):
    def construct(self):
        # 场景背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color="#001F54", fill_opacity=1)
        self.add(background)

        # 添加粒子效果
        particles = VGroup(*[
            Dot(radius=0.05, color=YELLOW).move_to(
                [np.random.uniform(-FRAME_WIDTH / 2, FRAME_WIDTH / 2),
                 np.random.uniform(-FRAME_HEIGHT / 2, FRAME_HEIGHT / 2),
                 0]
            ) for _ in range(50)
        ])
        self.add(particles)

        # 高温和低温热源矩形
        high_temp_source = Rectangle(width=2, height=3, color=RED, fill_color=RED, fill_opacity=0.8)
        low_temp_source = Rectangle(width=2, height=3, color=BLUE, fill_color=BLUE, fill_opacity=0.8)
        high_temp_source.to_edge(LEFT, buff=1)
        low_temp_source.to_edge(RIGHT, buff=1)

        # 热源滑入动画
        self.play(
            high_temp_source.animate.shift(RIGHT * 3),
            low_temp_source.animate.shift(LEFT * 3),
            run_time=2
        )
        self.wait(1)

        # 热量粒子从高温流向低温
        heat_particles = VGroup(*[
            Dot(radius=0.1, color=RED).move_to(high_temp_source.get_center())
            for _ in range(20)
        ])
        self.add(heat_particles)

        for dot in heat_particles:
            self.play(
                dot.animate.shift((low_temp_source.get_center() - high_temp_source.get_center()) * 0.5).set_color(BLUE),
                run_time=0.5
            )

        self.wait(1)

        # 动态熵柱状图
        entropy_bar = Rectangle(width=1, height=0.5, color=YELLOW, fill_color=YELLOW, fill_opacity=0.8)
        entropy_bar.next_to(high_temp_source, UP, buff=2)
        entropy_label = Text("熵", font_size=24, color=YELLOW)
        entropy_label.next_to(entropy_bar, UP, buff=0.3)

        self.play(FadeIn(entropy_bar), Write(entropy_label))

        for i in range(1, 6):  # 模拟熵柱状图增加
            new_bar = Rectangle(width=1, height=0.5 + i * 0.2, color=YELLOW, fill_color=YELLOW, fill_opacity=0.8)
            new_bar.next_to(high_temp_source, UP, buff=2)
            self.play(Transform(entropy_bar, new_bar), run_time=0.5)

        self.wait(1)

        # 公式显示
        entropy_formula = MathTex(r"\Delta S = \frac{Q}{T} > 0", font_size=36, color=WHITE)
        entropy_formula.next_to(entropy_bar, RIGHT, buff=2)
        self.play(Write(entropy_formula))
        self.wait(2)

        # 文字解释
        explanation = Text("热量从高温流向低温是不可逆的，因为熵总是增加。", font_size=28, color=WHITE)
        explanation.next_to(entropy_formula, DOWN, buff=1)
        self.play(FadeIn(explanation))
        self.wait(3)

        # 强调熵柱状图顶部和文字"不可逆"
        irreversible_text = Text("不可逆", font_size=36, color=YELLOW)
        irreversible_text.next_to(entropy_bar, UP, buff=0.5)
        self.play(FadeIn(irreversible_text), rate_func=rush_into)
        self.wait(2)

        # 热源变暗，粒子停止运动，熵柱状图静止
        self.play(
            high_temp_source.animate.set_fill(opacity=0.5).set_color(DARK_GRAY),
            low_temp_source.animate.set_fill(opacity=0.5).set_color(DARK_GRAY),
            FadeOut(heat_particles),
            run_time=2
        )

        conclusion = Text("这就是热力学第二定律的核心。", font_size=28, color=WHITE)
        conclusion.to_edge(DOWN, buff=1)
        self.play(Write(conclusion), run_time=2)

        self.wait(3)