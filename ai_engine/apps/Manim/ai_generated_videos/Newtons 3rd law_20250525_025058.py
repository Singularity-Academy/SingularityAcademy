from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            stroke_width=0,
            fill_color="#001f3f",
            fill_opacity=1,
        )
        self.add(background)

        # 添加星空点缀
        stars = VGroup(*[
            Dot(point=np.random.uniform([-FRAME_WIDTH/2, -FRAME_HEIGHT/2], [FRAME_WIDTH/2, FRAME_HEIGHT/2]),
                color=WHITE, radius=0.02) for _ in range(100)
        ])
        self.add(stars)

        # 渐变地面线条
        ground = Line(LEFT*5, RIGHT*5, color=GRAY)
        ground.shift(DOWN*2)
        self.add(ground)

        # 标题
        title = Text("Newton’s Third Law: Action and Reaction", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建方块 A 和 B
        square_a = Square(side_length=1, color=RED, fill_opacity=0.5)
        square_b = Square(side_length=1, color=BLUE, fill_opacity=0.5)
        square_a.shift(LEFT*1.5 + DOWN*1.5)
        square_b.shift(RIGHT*1.5 + DOWN*1.5)
        self.play(FadeIn(square_a), FadeIn(square_b))
        self.wait(1)

        # 动态展示作用力和反作用力
        action_arrow = Arrow(start=square_a.get_center(), end=square_b.get_center(), color=RED, buff=0.2)
        self.play(Create(action_arrow), run_time=1)
        self.wait(0.5)

        reaction_arrow = Arrow(start=square_b.get_center(), end=square_a.get_center(), color=BLUE, buff=0.2)
        self.play(Create(reaction_arrow), run_time=1)
        self.wait(0.5)

        # 添加公式和说明文字
        formula = MathTex(r"F_1 = -F_2", color=WHITE, font_size=48)
        formula.move_to(UP*1)
        explanation = Text("每一个作用力都伴随着大小相等、方向相反的反作用力。", font_size=24, color=WHITE)
        explanation.next_to(formula, DOWN)
        self.play(Write(formula), Write(explanation))
        self.wait(2)

        # 转换为小球并展示力的传递
        ball_a = Circle(radius=0.5, color=RED, fill_opacity=0.6)
        ball_b = Circle(radius=0.5, color=BLUE, fill_opacity=0.6)
        ball_a.move_to(square_a.get_center())
        ball_b.move_to(square_b.get_center())
        self.play(Transform(square_a, ball_a), Transform(square_b, ball_b))
        self.wait(1)

        collision_arrow = Arrow(start=ball_a.get_center(), end=ball_b.get_center(), color=RED, buff=0.2)
        reverse_arrow = Arrow(start=ball_b.get_center(), end=ball_a.get_center(), color=BLUE, buff=0.2)
        self.play(Create(collision_arrow), run_time=1)
        self.play(Create(reverse_arrow), run_time=1)

        # 增加小球回弹效果
        self.play(
            ball_a.animate.shift(LEFT*1),
            ball_b.animate.shift(RIGHT*1),
            run_time=1
        )
        self.wait(1)

        # 结束画面
        final_text = Text("Newton’s Third Law in Action", font_size=36, color=WHITE)
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)

        # 淡出所有元素
        self.play(FadeOut(VGroup(*self.mobjects)))