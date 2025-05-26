from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = BLACK
        stars = VGroup(*[Dot(color=WHITE).move_to(np.random.random(3) * 7 - 3.5) for _ in range(50)])
        self.add(stars)

        # 标题
        title = Text("力的相互作用", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 两个物体
        object_a = Circle(radius=0.5, color=RED, fill_opacity=0.6).shift(LEFT * 2)
        object_b = Circle(radius=0.5, color=BLUE, fill_opacity=0.6).shift(RIGHT * 2)
        self.play(FadeIn(object_a), FadeIn(object_b))
        self.wait(1)

        # 动态箭头和力大小展示
        force_a_to_b = Arrow(start=object_a.get_center(), end=object_b.get_center(), color=YELLOW, stroke_width=3)
        force_b_to_a = Arrow(start=object_b.get_center(), end=object_a.get_center(), color=GREEN, stroke_width=3)
        force_text_a_to_b = Text("5 N", font_size=24, color=YELLOW).next_to(force_a_to_b, UP)
        force_text_b_to_a = Text("5 N", font_size=24, color=GREEN).next_to(force_b_to_a, DOWN)
        
        self.play(Create(force_a_to_b), FadeIn(force_text_a_to_b))
        self.play(Create(force_b_to_a), FadeIn(force_text_b_to_a))
        self.wait(2)

        # 展示公式
        formula = MathTex(r"F_{A \to B} = -F_{B \to A}", font_size=36, color=WHITE)
        formula.to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1)

        # 动态变化箭头长度和力大小
        for magnitude in [3, 6, 4, 5]:
            new_force_a_to_b = Arrow(start=object_a.get_center(), end=object_b.get_center(), color=YELLOW, stroke_width=3).scale(magnitude / 5)
            new_force_b_to_a = Arrow(start=object_b.get_center(), end=object_a.get_center(), color=GREEN, stroke_width=3).scale(magnitude / 5)
            new_force_text_a_to_b = Text(f"{magnitude} N", font_size=24, color=YELLOW).next_to(new_force_a_to_b, UP)
            new_force_text_b_to_a = Text(f"{magnitude} N", font_size=24, color=GREEN).next_to(new_force_b_to_a, DOWN)

            self.play(
                Transform(force_a_to_b, new_force_a_to_b),
                Transform(force_b_to_a, new_force_b_to_a),
                Transform(force_text_a_to_b, new_force_text_a_to_b),
                Transform(force_text_b_to_a, new_force_text_b_to_a),
                run_time=2
            )
            self.wait(1)

        # 结束场景
        ending_text = Text("作用力与反作用力，永远成对存在", font_size=36, color=WHITE)
        self.play(FadeOut(VGroup(object_a, object_b, force_a_to_b, force_b_to_a, force_text_a_to_b, force_text_b_to_a, formula)))
        self.play(FadeIn(ending_text))
        self.wait(2)
        self.play(FadeOut(ending_text))