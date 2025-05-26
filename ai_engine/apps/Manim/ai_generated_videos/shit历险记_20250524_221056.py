from manim import *
import numpy as np

class ShitAdventure(Scene):
    def construct(self):
        # 标题
        title = Text("Shit历险记：从混乱到秩序的数学启示", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 混乱背景
        chaotic_background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLACK, fill_color="#8B4513", fill_opacity=1)
        self.add(chaotic_background)

        # 飘动的微粒
        particles = VGroup(*[Dot(color=WHITE).shift(np.random.uniform(-FRAME_WIDTH / 2, FRAME_WIDTH / 2) * RIGHT + np.random.uniform(-FRAME_HEIGHT / 2, FRAME_HEIGHT / 2) * UP) for _ in range(30)])
        self.add(particles)

        # Shit角色
        shit_character = Circle(radius=0.5, color=BLACK, fill_color="#5A3D1A", fill_opacity=1)
        eyes = VGroup(Dot(color=WHITE).shift(LEFT * 0.15 + UP * 0.15), Dot(color=WHITE).shift(RIGHT * 0.15 + UP * 0.15))
        mouth = Arc(start_angle=PI / 2, angle=-PI, radius=0.2, color=BLACK).shift(DOWN * 0.1)
        shit_face = VGroup(shit_character, eyes, mouth)
        shit_face.move_to(ORIGIN)
        self.play(FadeIn(shit_face))
        self.wait(1)

        # 混乱的几何碎片
        chaotic_shapes = VGroup(
            *[
                Square(side_length=0.5, color=RED).move_to(np.random.uniform(-FRAME_WIDTH / 2, FRAME_WIDTH / 2) * RIGHT + np.random.uniform(-FRAME_HEIGHT / 2, FRAME_HEIGHT / 2) * UP),
                Circle(radius=0.3, color=BLUE).move_to(np.random.uniform(-FRAME_WIDTH / 2, FRAME_WIDTH / 2) * RIGHT + np.random.uniform(-FRAME_HEIGHT / 2, FRAME_HEIGHT / 2) * UP),
                Triangle(color=GREEN).move_to(np.random.uniform(-FRAME_WIDTH / 2, FRAME_WIDTH / 2) * RIGHT + np.random.uniform(-FRAME_HEIGHT / 2, FRAME_HEIGHT / 2) * UP)
            ]
            for _ in range(8)
        )
        self.play(FadeIn(chaotic_shapes))
        self.wait(1)

        # 熵公式出现
        entropy_formula = MathTex(r"S = k \ln W", font_size=48, color=WHITE)
        entropy_formula.to_edge(UP)
        self.play(Write(entropy_formula))
        entropy_explanation = Text("熵是混乱程度的数学衡量", font_size=32, color=WHITE)
        entropy_explanation.next_to(entropy_formula, DOWN)
        self.play(Write(entropy_explanation))
        self.wait(2)

        # Shit吸收碎片并形成网格
        self.play(
            shit_face.animate.shift(LEFT * 2),
            chaotic_shapes.animate.arrange_in_grid(rows=4, cols=4, buff=0.5).move_to(RIGHT * 2),
            run_time=3
        )
        self.wait(1)

        # 背景过渡到蓝绿色
        orderly_background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLACK, fill_color="#32CD32", fill_opacity=1)
        self.play(Transform(chaotic_background, orderly_background), run_time=2)

        # 网格形成
        orderly_grid = VGroup(*[Square(side_length=0.5, color=WHITE) for _ in range(16)])
        orderly_grid.arrange_in_grid(rows=4, cols=4, buff=0.1).move_to(RIGHT * 2)
        self.play(Transform(chaotic_shapes, orderly_grid))
        self.wait(1)

        # Shit满意表情
        satisfied_mouth = Arc(start_angle=-PI / 2, angle=PI, radius=0.2, color=BLACK).shift(DOWN * 0.1)
        satisfied_face = VGroup(shit_character, eyes, satisfied_mouth)
        self.play(Transform(shit_face, satisfied_face))
        self.wait(1)

        # 结尾文字
        conclusion = Text("混乱到秩序：熵的意义", font_size=36, color=WHITE)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))