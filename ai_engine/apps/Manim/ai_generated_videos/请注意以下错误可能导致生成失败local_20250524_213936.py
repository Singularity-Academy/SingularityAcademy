from manim import *
import numpy as np

class ThermodynamicSecondLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLUE, fill_opacity=1)
        gradient = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=WHITE, fill_opacity=0.1)
        self.add(background)
        self.play(FadeIn(gradient, run_time=2))

        # 标题
        title = Text("热力学第二定律", font_size=36, color=WHITE, glow_factor=0.5)
        title.to_corner(UL)
        self.play(Write(title))
        self.wait(1)

        # 孤立系统容器
        container = Rectangle(width=6, height=4, color=WHITE)
        container_text = Text("孤立系统", font_size=24, color=WHITE)
        container_text.next_to(container, UP)
        self.play(Create(container), Write(container_text))
        self.wait(1)

        # 初始状态粒子
        red_particles = VGroup(*[Dot(color=RED).move_to(container.get_left() + np.array([np.random.random()*2-1, np.random.random()*1.8-0.9, 0])) for _ in range(20)])
        blue_particles = VGroup(*[Dot(color=BLUE).move_to(container.get_right() + np.array([np.random.random()*2-1, np.random.random()*1.8-0.9, 0])) for _ in range(20)])
        self.play(FadeIn(red_particles), FadeIn(blue_particles))
        self.wait(1)

        # 粒子运动模拟
        def random_motion(dot):
            dot.add_updater(lambda obj: obj.move_to(container.get_center() + np.array([np.random.random()*6-3, np.random.random()*4-2, 0])))

        for dot in red_particles:
            random_motion(dot)
        for dot in blue_particles:
            random_motion(dot)

        self.play(red_particles.animate, blue_particles.animate, run_time=5)

        # 公式展示
        formula = MathTex(r"\Delta S \geq 0", font_size=48, color=WHITE)
        formula.to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1)

        # 时间轴展示
        timeline = Line(start=LEFT*4, end=RIGHT*4, color=WHITE)
        timeline.to_edge(DOWN, buff=1.5)
        arrow = Arrow(start=timeline.get_left(), end=timeline.get_right(), color=YELLOW)
        initial_state = Text("初始状态", font_size=24, color=WHITE).next_to(timeline.get_left(), UP)
        middle_state = Text("中间状态", font_size=24, color=WHITE).move_to(timeline.get_center() + UP*0.5)
        final_state = Text("最终状态", font_size=24, color=WHITE).next_to(timeline.get_right(), UP)

        self.play(Create(timeline), Create(arrow))
        self.play(Write(initial_state), Write(middle_state), Write(final_state))
        self.wait(1)

        # 状态解释
        explanation = Text("熵：系统无序程度的度量", font_size=28, color=WHITE)
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)

        # 混合状态展示
        mixed_particles = VGroup(*[Dot(color=np.random.choice([RED, BLUE])).move_to(container.get_center() + np.array([np.random.random()*6-3, np.random.random()*4-2, 0])) for _ in range(40)])
        self.play(FadeOut(red_particles), FadeOut(blue_particles), FadeIn(mixed_particles))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(container, container_text, timeline, arrow, initial_state, middle_state, final_state, mixed_particles, explanation)))
        self.play(Transform(formula, title))
        self.wait(2)