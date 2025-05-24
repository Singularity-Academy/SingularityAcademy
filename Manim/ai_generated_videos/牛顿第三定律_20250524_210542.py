from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 标题
        title = Text("相互作用的力量：牛顿第三定律的直观呈现", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景设置
        ground = Line(start=LEFT * 5, end=RIGHT * 5, color=WHITE).shift(DOWN * 2)
        cube = Square(side_length=1, color=WHITE, fill_opacity=1).move_to(DOWN)
        self.play(Create(ground), FadeIn(cube))
        self.wait(1)

        # 作用力箭头和文字
        action_arrow = Arrow(start=cube.get_left(), end=cube.get_left() + LEFT * 2, color=RED)
        action_label = Text("作用力", font_size=32, color=RED).next_to(action_arrow, UP)

        # 反作用力箭头和文字
        reaction_arrow = Arrow(start=cube.get_right(), end=cube.get_right() + RIGHT * 2, color=BLUE)
        reaction_label = Text("反作用力", font_size=32, color=BLUE).next_to(reaction_arrow, UP)

        # 动画序列
        self.play(GrowArrow(action_arrow), Write(action_label))
        self.wait(0.5)
        self.play(GrowArrow(reaction_arrow), Write(reaction_label))
        self.wait(1)

        # 公式展示
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}").scale(1.2).to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 动态变化强调
        self.play(
            action_arrow.animate.scale(1.5),
            reaction_arrow.animate.scale(1.5),
            run_time=1
        )
        self.play(
            action_arrow.animate.scale(1 / 1.5),
            reaction_arrow.animate.scale(1 / 1.5),
            run_time=1
        )
        self.wait(1)

        # 补充场景：日常生活示例
        human = SVGMobject("human.svg").scale(0.5).to_edge(LEFT)
        wall = Rectangle(height=2, width=0.5, color=GREY).to_edge(RIGHT)
        human_text = Text("人推墙", font_size=28, color=WHITE).next_to(human, DOWN)
        wall_text = Text("墙反作用", font_size=28, color=WHITE).next_to(wall, DOWN)

        self.play(FadeIn(human), FadeIn(wall))
        self.play(Write(human_text), Write(wall_text))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(action_arrow, reaction_arrow, action_label, reaction_label, formula, ground, cube, human, wall, human_text, wall_text)))
        ending_title = Text("牛顿第三定律", font_size=40, color=WHITE)
        self.play(Write(ending_title))
        self.wait(2)