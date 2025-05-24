from manim import *
import numpy as np

class NewtonLawsScene(Scene):
    def construct(self):
        # 设置背景
        self.camera.background_color = "#001f3f"  # 深蓝色背景
        stars = VGroup(*[Dot(point=np.random.uniform(-6, 6, 3), color=WHITE) for _ in range(150)])
        self.add(stars)
        
        # 添加地面网格
        grid = NumberPlane(background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.3})
        self.add(grid)
        
        # 添加右下角标题
        subtitle = Text("牛顿运动定律演示", font_size=24, color=YELLOW)
        subtitle.to_corner(DR)
        self.add(subtitle)

        # 第一定律
        ball = Circle(radius=0.5, color=WHITE, fill_opacity=0.8).move_to(ORIGIN)
        first_law_formula = MathTex(r"F = 0 \implies v = \text{const}").to_edge(UP)
        first_law_highlight = MathTex(r"F = 0").move_to(first_law_formula.get_center()).set_color(YELLOW)
        
        self.play(Write(first_law_formula))
        self.wait(1)
        self.play(Transform(first_law_formula, first_law_highlight))
        self.wait(1)
        self.play(Create(ball))
        self.wait(2)
        
        # 添加旁白
        first_law_text = Text("物体在没有外力作用时保持静止或匀速直线运动。", font_size=28, color=WHITE)
        first_law_text.to_edge(DOWN)
        self.play(Write(first_law_text))
        self.wait(2)
        self.play(FadeOut(first_law_formula, first_law_text, ball))

        # 第二定律
        ball = Circle(radius=0.5, color=WHITE, fill_opacity=0.8).move_to(LEFT*3)
        force_arrow = Arrow(start=LEFT*4, end=LEFT*3, color=YELLOW, buff=0.1)
        second_law_formula = MathTex(r"F = ma").to_edge(UP)
        self.add(ball)
        self.play(Create(force_arrow))
        self.play(Write(second_law_formula))
        self.wait(1)
        
        # 动画展示加速效果
        force_arrow = Arrow(start=LEFT*3, end=LEFT*2, color=YELLOW, buff=0.1)
        self.play(ball.animate.move_to(RIGHT*3), Transform(force_arrow, force_arrow.copy().scale(1.5)))
        self.wait(2)

        # 添加旁白
        second_law_text = Text("力与加速度成正比，与质量成反比。", font_size=28, color=WHITE)
        second_law_text.to_edge(DOWN)
        self.play(Write(second_law_text))
        self.wait(2)
        self.play(FadeOut(second_law_formula, second_law_text, ball, force_arrow))

        # 第三定律
        left_obj = Rectangle(width=1, height=1, color=BLUE).move_to(LEFT*2)
        right_obj = Rectangle(width=1, height=1, color=RED).move_to(RIGHT*2)
        action_arrow = Arrow(start=LEFT*2, end=LEFT*1, color=GREEN, buff=0.1)
        reaction_arrow = Arrow(start=RIGHT*2, end=RIGHT*3, color=ORANGE, buff=0.1)
        third_law_formula = MathTex(r"F_{\text{action}} = -F_{\text{reaction}}").to_edge(UP)

        self.play(Create(left_obj), Create(right_obj))
        self.wait(1)
        self.play(Write(third_law_formula))
        self.wait(1)
        
        # 动画展示作用力与反作用力
        self.play(Create(action_arrow), Create(reaction_arrow))
        self.play(left_obj.animate.shift(LEFT), right_obj.animate.shift(RIGHT))
        self.wait(2)

        # 添加旁白
        third_law_text = Text("作用力与反作用力总是同时出现且大小相等方向相反。", font_size=28, color=WHITE)
        third_law_text.to_edge(DOWN)
        self.play(Write(third_law_text))
        self.wait(2)
        self.play(FadeOut(third_law_formula, third_law_text, left_obj, right_obj, action_arrow, reaction_arrow))

        # 结束动画
        end_text = Text("这就是牛顿三大运动定律！", font_size=36, color=WHITE)
        self.play(Write(end_text))
        self.wait(3)
        self.play(FadeOut(end_text))