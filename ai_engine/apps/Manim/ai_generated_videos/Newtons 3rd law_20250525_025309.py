from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#001f4d"  # 深蓝色背景
        grid = NumberPlane(background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.4})
        stars = VGroup(*[Dot(point=np.random.uniform(-7, 7, size=2), color=WHITE, radius=0.03) for _ in range(50)])
        self.add(grid, stars)

        # 标题
        title = Text("牛顿第三定律", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title))

        # 创建主要对象
        circle = Circle(radius=0.5, color=YELLOW, fill_opacity=0.8).shift(LEFT * 3)
        square = Square(side_length=1, color=BLUE_E, fill_opacity=0.8).shift(RIGHT * 3)
        self.play(Create(circle), Create(square))
        self.wait(1)

        # 力箭头和标签
        action_arrow = Arrow(start=circle.get_center(), end=square.get_center(), color=RED, stroke_width=4)
        reaction_arrow = Arrow(start=square.get_center(), end=circle.get_center(), color=GREEN, stroke_width=4)

        action_label = Text("作用力", font_size=24, color=RED).next_to(action_arrow, UP, buff=0.2)
        reaction_label = Text("反作用力", font_size=24, color=GREEN).next_to(reaction_arrow, DOWN, buff=0.2)

        self.play(Create(action_arrow), Write(action_label))
        self.play(Create(reaction_arrow), Write(reaction_label))
        self.wait(1)

        # 动作开始：物体运动
        self.play(
            circle.animate.shift(RIGHT * 2),
            square.animate.shift(RIGHT * 2),
            action_arrow.animate.shift(RIGHT * 2),
            reaction_arrow.animate.shift(RIGHT * 2),
            action_label.animate.shift(RIGHT * 2),
            reaction_label.animate.shift(RIGHT * 2),
            run_time=3,
        )
        self.wait(1)

        # 动态公式
        formula = MathTex(r"F_{\text{action}} = -F_{\text{reaction}}", font_size=48, color=WHITE)
        formula.to_edge(DOWN)
        self.play(Write(formula), run_time=2)
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(circle, square, action_arrow, reaction_arrow, action_label, reaction_label, formula)))
        end_title = Text("牛顿第三定律", font_size=36, color=WHITE).to_edge(UP)
        explanation = Text("作用力与反作用力永远相等且方向相反", font_size=24, color=WHITE).next_to(end_title, DOWN)
        self.play(Write(end_title), Write(explanation))
        self.wait(3)