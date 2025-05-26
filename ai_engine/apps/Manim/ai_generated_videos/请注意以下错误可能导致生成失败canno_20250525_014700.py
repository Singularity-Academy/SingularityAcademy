from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color="#87CEFA", fill_opacity=1)  # 浅蓝背景
        background.set_fill(color=["#87CEFA", "#D3D3D3"], opacity=1)  # 渐变浅蓝到浅灰
        background.to_edge(DOWN)
        self.add(background)

        # 地面平台
        platform = Rectangle(width=6, height=0.3, color=GRAY, fill_opacity=0.8)
        platform.move_to(DOWN * 2.5)
        self.add(platform)

        # 网格线背景
        grid = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1], background_line_style={"stroke_opacity": 0.3})
        self.add(grid)

        # 两个物体 A 和 B
        cube_a = Square(side_length=1, color=RED, fill_opacity=0.8)
        cube_b = Square(side_length=1, color=BLUE, fill_opacity=0.8)
        cube_a.move_to(LEFT * 2 + DOWN * 2)
        cube_b.move_to(RIGHT * 2 + DOWN * 2)
        self.add(cube_a, cube_b)

        # 摄像机拉近到场景中央
        self.play(self.camera.frame.animate.set_width(8).move_to(DOWN * 1.5), run_time=2)

        # 动画手指及作用力箭头
        hand = Dot(color=WHITE).scale(1.5)
        hand.move_to(cube_a.get_center() + LEFT * 1.5)
        self.play(FadeIn(hand), run_time=1)

        action_arrow = Arrow(start=hand.get_center(), end=cube_a.get_center() + RIGHT * 1.5, color=RED, buff=0.1)
        action_label = Text("作用力", font_size=32, color=RED).next_to(action_arrow, UP)
        self.play(Create(action_arrow), Write(action_label), run_time=1)

        # 反作用力箭头
        reaction_arrow = Arrow(start=cube_b.get_center(), end=cube_b.get_center() + LEFT * 1.5, color=BLUE, buff=0.1)
        reaction_label = Text("反作用力", font_size=32, color=BLUE).next_to(reaction_arrow, UP)
        self.play(Create(reaction_arrow), Write(reaction_label), run_time=1)

        # 动态公式展示
        formula = MathTex(r"F_{A \to B} = -F_{B \to A}", font_size=48).to_edge(UP)
        self.play(Write(formula), run_time=2)

        # 动画展示力作用下物体移动
        self.play(
            cube_a.animate.shift(RIGHT * 2),
            cube_b.animate.shift(LEFT * 2),
            action_arrow.animate.shift(RIGHT * 2),
            reaction_arrow.animate.shift(LEFT * 2),
            hand.animate.shift(RIGHT * 2),
            run_time=3
        )

        # 摄像机拉远，加入总结文字
        summary_text = Text("每一个力都有大小相等、方向相反的反作用力", font_size=36, color=WHITE).to_edge(DOWN)
        self.play(self.camera.frame.animate.set_width(FRAME_WIDTH).move_to(ORIGIN), Write(summary_text), run_time=3)

        # 场景结束
        self.wait(2)