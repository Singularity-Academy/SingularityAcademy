from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#001f3f"  # 深蓝色背景
        stars = VGroup(
            *[Dot(point=np.random.uniform(-7, 7, 3), color=WHITE, radius=0.03) for _ in range(100)]
        )
        for star in stars:
            star.set_opacity(np.random.uniform(0.5, 1))
        self.add(stars)

        # 场景标题
        title = Text("热力学第二定律", font_size=48, color=YELLOW)
        subtitle = Text("熵总是增加", font_size=32, color=WHITE)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # 两个球体设置
        hot_sphere = Circle(radius=1, color=RED, fill_opacity=0.6)
        cold_sphere = Circle(radius=1, color=BLUE, fill_opacity=0.6)
        hot_sphere.move_to(LEFT * 3)
        cold_sphere.move_to(RIGHT * 3)
        self.play(FadeIn(hot_sphere), FadeIn(cold_sphere))
        self.wait(1)

        # 分子运动展示
        hot_particles = VGroup(
            *[Dot(point=hot_sphere.get_center() + np.random.uniform(-1, 1, 2), color=ORANGE, radius=0.05) for _ in range(50)]
        )
        cold_particles = VGroup(
            *[Dot(point=cold_sphere.get_center() + np.random.uniform(-1, 1, 2), color=BLUE, radius=0.05) for _ in range(30)]
        )
        self.play(FadeIn(hot_particles), FadeIn(cold_particles))
        self.wait(1)

        # 热量传递箭头
        arrow = Arrow(start=hot_sphere.get_center(), end=cold_sphere.get_center(), color=YELLOW)
        self.play(Write(arrow))
        self.wait(1)

        # 熵公式展示
        entropy_formula = MathTex(r"\Delta S = \frac{Q}{T}", font_size=48, color=WHITE)
        entropy_formula.to_edge(UP)
        explanation = Text("熵是系统混乱程度的度量", font_size=32, color=YELLOW)
        explanation.next_to(entropy_formula, DOWN, buff=0.5)

        self.play(Write(entropy_formula))
        self.play(FadeIn(explanation))
        self.wait(2)
        self.play(FadeOut(entropy_formula), FadeOut(explanation))

        # 熵变化曲线
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            axis_config={"color": WHITE},
            x_length=7,
            y_length=4,
        )
        axes.move_to(DOWN * 2)

        labels = axes.get_axis_labels(x_label="时间", y_label="熵")
        curve = axes.plot(lambda x: x**0.5 + 2, x_range=[0, 9], color=RED, stroke_width=2)

        self.play(Create(axes), Create(labels))
        self.play(Create(curve))
        self.wait(2)

        # 热平衡展示
        self.play(FadeOut(arrow))
        self.play(
            hot_sphere.animate.set_color(PURPLE),
            cold_sphere.animate.set_color(PURPLE),
            run_time=2,
        )
        self.wait(1)

        # 结束场景
        end_text = Text("熵总是增加", font_size=48, color=YELLOW)
        end_text.to_edge(DOWN)
        self.play(Write(end_text))
        self.wait(2)

        # 淡出
        self.play(FadeOut(VGroup(*self.mobjects)))