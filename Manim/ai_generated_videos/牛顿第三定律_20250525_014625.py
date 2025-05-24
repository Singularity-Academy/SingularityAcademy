from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#001F4D"  # 深蓝色背景
        stars = VGroup(*[
            Dot(point=np.random.uniform(-7, 7, size=3), color=WHITE, radius=0.02)
            for _ in range(50)
        ])
        self.add(stars)

        # 地面
        ground = Line(start=LEFT*7, end=RIGHT*7, color=GRAY, stroke_width=3)
        ground.shift(DOWN*2.5)
        self.add(ground)

        # 标题
        title = Text("牛顿第三定律：作用力与反作用力", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 物体A和物体B
        box_a = Square(side_length=1, color=RED, fill_opacity=0.7)
        box_b = Square(side_length=1, color=BLUE, fill_opacity=0.7)
        box_a.shift(LEFT*2 + DOWN*2)
        box_b.shift(RIGHT*2 + DOWN*2)
        self.play(FadeIn(box_a), FadeIn(box_b))
        self.wait(1)

        # 作用力箭头和文字
        force_arrow_a_to_b = Arrow(
            start=box_a.get_center(), 
            end=box_b.get_center(), 
            color=GREEN, 
            stroke_width=5
        )
        action_text = Text("作用力", font_size=24, color=GREEN)
        action_text.next_to(force_arrow_a_to_b, UP)

        self.play(Create(force_arrow_a_to_b), Write(action_text))
        self.wait(1)

        # 反作用力箭头和文字
        force_arrow_b_to_a = Arrow(
            start=box_b.get_center(), 
            end=box_a.get_center(), 
            color=ORANGE, 
            stroke_width=5
        )
        reaction_text = Text("反作用力", font_size=24, color=ORANGE)
        reaction_text.next_to(force_arrow_b_to_a, UP)

        self.play(Create(force_arrow_b_to_a), Write(reaction_text))
        self.wait(1)

        # 动态公式
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=48, color=YELLOW)
        formula.move_to(UP*1)
        self.play(Write(formula))
        self.wait(1)

        # 公式闪烁
        self.play(formula.animate.set_opacity(0.2), run_time=0.5)
        self.play(formula.animate.set_opacity(1), run_time=0.5)
        self.play(formula.animate.set_opacity(0.2), run_time=0.5)
        self.play(formula.animate.set_opacity(1), run_time=0.5)

        # 箭头动画
        self.play(
            force_arrow_a_to_b.animate.scale(1.2), 
            force_arrow_b_to_a.animate.scale(1.2),
            run_time=1.5
        )
        self.play(
            force_arrow_a_to_b.animate.scale(0.8), 
            force_arrow_b_to_a.animate.scale(0.8),
            run_time=1.5
        )

        # 总结文字
        summary_text = Text("每一个作用力都有一个大小相等、方向相反的反作用力", font_size=32, color=WHITE)
        summary_text.to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(box_a, box_b, force_arrow_a_to_b, force_arrow_b_to_a, action_text, reaction_text, formula, summary_text, stars, ground, title)))