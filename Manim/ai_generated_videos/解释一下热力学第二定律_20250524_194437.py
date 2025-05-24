from manim import *

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 场景背景设置
        self.camera.background_color = "#001F4D"  # 深蓝色背景

        # 场景标题
        title = Text("从混乱到秩序：热力学第二定律的秘密", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # 显示熵公式
        entropy_formula = MathTex(r"S = k \ln \Omega", font_size=48, color=WHITE)
        entropy_formula.next_to(title, DOWN, buff=1)
        self.play(Write(entropy_formula), run_time=2)
        self.wait(1)

        # 粒子容器设置
        container = Square(color=WHITE, fill_opacity=0, stroke_width=2)
        container.scale(3)
        container.move_to(DOWN * 1.5)
        self.play(Create(container), run_time=2)
        self.wait(1)

        # 初始粒子分布（粒子集中在容器左侧）
        particles = VGroup(*[Dot(color=YELLOW).scale(0.5) for _ in range(50)])
        for i, particle in enumerate(particles):
            particle.move_to(container.get_left() + RIGHT * 0.5 * (i % 5) + UP * 0.5 * (i // 5))
        self.play(FadeIn(particles), run_time=2)
        self.wait(1)

        # 显示箭头和熵增加方向的文字
        arrow = Arrow(start=container.get_left(), end=container.get_right(), color=WHITE, buff=0.5)
        arrow_label = Text("熵增加方向", font_size=24, color=WHITE)
        arrow_label.next_to(arrow, UP, buff=0.2)
        self.play(Create(arrow), Write(arrow_label), run_time=2)
        self.wait(1)

        # 粒子开始逐渐随机移动，填充整个容器
        animations = []
        for particle in particles:
            animations.append(particle.animate.move_to(
                container.get_center() + (UP * (2 * random.random() - 1)) + (RIGHT * (2 * random.random() - 1))
            ))
        self.play(*animations, run_time=4, rate_func=linear)
        self.wait(1)

        # 强调不可逆性
        irreversible_text = Text("自然过程是不可逆的", font_size=32, color=RED)
        irreversible_text.to_edge(DOWN)
        self.play(Write(irreversible_text), run_time=2)
        self.wait(2)

        # 总结与升华
        summary_formula = entropy_formula.copy()
        summary_text = Text("熵是自然界的时间箭头", font_size=28, color=WHITE)
        summary_text.next_to(summary_formula, DOWN, buff=0.5)
        self.play(FadeOut(arrow, arrow_label, irreversible_text), run_time=1)
        self.play(Transform(entropy_formula, summary_formula), Write(summary_text), run_time=2)
        self.wait(2)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)), run_time=2)