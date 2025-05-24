from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 设置场景背景颜色
        self.camera.background_color = "#ADD8E6"  # 浅蓝色

        # 标题
        title = Text("牛顿第三定律：作用力与反作用力", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 地面
        ground = Line(start=LEFT * 7, end=RIGHT * 7, color=GRAY, stroke_width=2).shift(DOWN * 2)
        self.play(Create(ground))
        self.wait(1)

        # 创建物体 A 和物体 B
        object_A = Square(side_length=1, color=RED, fill_opacity=0.8).shift(LEFT * 2 + DOWN * 1.5)
        object_B = Square(side_length=1, color=BLUE, fill_opacity=0.8).shift(RIGHT * 2 + DOWN * 1.5)
        label_A = Text("物体 A", font_size=24, color=RED).next_to(object_A, DOWN)
        label_B = Text("物体 B", font_size=24, color=BLUE).next_to(object_B, DOWN)

        self.play(FadeIn(object_A, object_B), Write(label_A), Write(label_B))
        self.wait(1)

        # 创建力的箭头和标签
        force_AB = Arrow(
            start=object_A.get_right(), end=object_B.get_left(), color=RED, buff=0.1, stroke_width=4
        )
        force_BA = Arrow(
            start=object_B.get_left(), end=object_A.get_right(), color=BLUE, buff=0.1, stroke_width=4
        )
        force_AB_label = Text("作用力", font_size=24, color=RED).next_to(force_AB, UP)
        force_BA_label = Text("反作用力", font_size=24, color=BLUE).next_to(force_BA, DOWN)

        self.play(GrowArrow(force_AB), Write(force_AB_label))
        self.wait(0.5)
        self.play(GrowArrow(force_BA), Write(force_BA_label))
        self.wait(1)

        # 展示公式
        formula = MathTex(r"F_{AB} = -F_{BA}", font_size=36, color=WHITE).next_to(object_B, UP * 2)
        self.play(Write(formula))
        self.wait(1)

        # 模拟物体移动
        self.play(
            object_A.animate.shift(LEFT * 2),
            object_B.animate.shift(RIGHT * 2),
            run_time=2
        )
        self.wait(1)

        # 强调公式
        self.play(FadeOut(force_AB, force_BA, force_AB_label, force_BA_label))
        self.play(FocusOn(formula))
        self.wait(2)

        # 结束场景
        end_text = Text("作用力和反作用力总是成对出现", font_size=32, color=YELLOW).to_edge(DOWN)
        self.play(Write(end_text))
        self.wait(2)

        # 清除所有元素
        self.play(FadeOut(VGroup(*self.mobjects)))