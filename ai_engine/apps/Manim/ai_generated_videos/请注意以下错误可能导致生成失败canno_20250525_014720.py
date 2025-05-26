from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#87CEEB"  # 浅蓝色背景
        ground_line = Line(start=LEFT*6, end=RIGHT*6, color=GRAY)
        ground_line.to_edge(DOWN)
        self.add(ground_line)

        # 标题
        title = Text("牛顿第三定律：作用力与反作用力", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 方块A和方块B
        block_a = Square(side_length=1, color=RED, fill_opacity=0.8)
        block_b = Square(side_length=1, color=BLUE, fill_opacity=0.8)
        block_a.move_to(LEFT*2 + ground_line.get_center())
        block_b.move_to(RIGHT*2 + ground_line.get_center())
        label_a = Text("物体A", font_size=24, color=WHITE).next_to(block_a, UP)
        label_b = Text("物体B", font_size=24, color=WHITE).next_to(block_b, UP)
        self.play(FadeIn(block_a), FadeIn(block_b), Write(label_a), Write(label_b))
        self.wait(1)

        # 红色箭头（作用力）
        action_arrow = Arrow(
            start=block_a.get_right(),
            end=block_b.get_left(),
            color=RED,
            stroke_width=5
        )
        action_label = Text("作用力", font_size=24, color=RED).next_to(action_arrow, UP)
        self.play(Create(action_arrow), Write(action_label))
        self.wait(1)

        # 蓝色箭头（反作用力）
        reaction_arrow = Arrow(
            start=block_b.get_left(),
            end=block_a.get_right(),
            color=BLUE,
            stroke_width=5
        )
        reaction_label = Text("反作用力", font_size=24, color=BLUE).next_to(reaction_arrow, DOWN)
        self.play(Create(reaction_arrow), Write(reaction_label))
        self.wait(1)

        # 动态展示箭头长度变化
        self.play(
            action_arrow.animate.scale(1.5, about_point=action_arrow.get_start()),
            reaction_arrow.animate.scale(1.5, about_point=reaction_arrow.get_start()),
            run_time=2
        )
        self.wait(1)

        # 展示公式
        formula = MathTex(r"F_{A \to B} = -F_{B \to A}", font_size=48, color=WHITE)
        formula.to_edge(UP).shift(DOWN*1)
        self.play(Write(formula))
        self.wait(1)

        # 强调箭头方向相反（闪烁效果）
        self.play(
            action_arrow.animate.set_opacity(0.5),
            reaction_arrow.animate.set_opacity(0.5),
            run_time=0.5
        )
        self.play(
            action_arrow.animate.set_opacity(1),
            reaction_arrow.animate.set_opacity(1),
            run_time=0.5
        )
        self.wait(1)

        # 真实世界例子
        example_text = Text("现实例子：两人推对方", font_size=28, color=WHITE)
        example_text.to_edge(DOWN)
        self.play(Write(example_text))
        self.wait(1)

        # 结束总结
        summary_text = Text(
            "作用力与反作用力：自然界的力量平衡法则",
            font_size=28,
            color=WHITE
        )
        summary_text.to_edge(DOWN)
        self.play(Transform(example_text, summary_text))
        self.wait(2)

        # 整体淡出
        self.play(FadeOut(VGroup(*self.mobjects)))