from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLACK, fill_opacity=1)
        background.set_fill("#001133", opacity=1)  # 深蓝色背景
        stars = VGroup(*[Dot(point=np.random.uniform(-7, 7, 3), color=WHITE, radius=0.02) for _ in range(150)])
        self.add(background, stars)

        # 标题
        title = Text("作用力与反作用力的优雅舞蹈", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 物体 A 和 B
        object_A = Circle(radius=0.5, color=RED, fill_opacity=0.8).shift(LEFT*2)
        object_B = Circle(radius=0.5, color=BLUE, fill_opacity=0.8).shift(RIGHT*2)
        label_A = Text("物体 A", font_size=24, color=WHITE).next_to(object_A, DOWN)
        label_B = Text("物体 B", font_size=24, color=WHITE).next_to(object_B, DOWN)
        self.play(FadeIn(object_A), FadeIn(object_B), Write(label_A), Write(label_B))
        self.wait(1)

        # 作用力箭头
        force_A_to_B = Arrow(start=object_A.get_center(), end=object_B.get_center(), color=RED, buff=0.5, max_stroke_width_to_length_ratio=5)
        force_B_to_A = Arrow(start=object_B.get_center(), end=object_A.get_center(), color=BLUE, buff=0.5, max_stroke_width_to_length_ratio=5)
        
        # 箭头动态变化
        self.play(Create(force_A_to_B))
        self.play(Create(force_B_to_A))
        self.wait(1)

        # 动态公式展示
        formula = MathTex(r"F_{A \to B} = -F_{B \to A}", font_size=48, color=WHITE)
        formula.move_to(UP*2)
        self.play(Write(formula))
        self.wait(1)

        # 总结文字
        summary_text = Text("牛顿第三定律：作用力与反作用力大小相等，方向相反。", font_size=24, color=WHITE)
        summary_text.to_edge(DOWN)
        self.play(FadeIn(summary_text))
        self.wait(2)

        # 结尾
        self.play(FadeOut(VGroup(object_A, object_B, label_A, label_B, force_A_to_B, force_B_to_A, formula, summary_text)))
        self.play(FadeOut(stars))
        self.wait(1)