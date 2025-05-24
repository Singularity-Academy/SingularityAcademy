from manim import *

class NewtonFirstLaw(Scene):
    def construct(self):
        # 设置背景
        self.camera.background_color = "#0c1445"  # 深蓝色背景
        stars = VGroup(*[Dot(color=WHITE, radius=0.005).move_to(
            [x, y, 0]) for x, y in zip(
            np.random.uniform(-7, 7, 150), np.random.uniform(-4, 4, 150)
        )])
        self.add(stars)

        # 创建地面
        ground = Line(start=LEFT*7, end=RIGHT*7, color=LIGHT_GRAY).shift(DOWN*2.5)
        self.add(ground)

        # 创建球体
        ball = Circle(radius=0.3, color=WHITE, fill_opacity=1).shift(DOWN*2.2 + LEFT*4)

        # 静止状态文字
        static_text = Text("静止状态", font_size=36, color=YELLOW).next_to(ball, UP)

        # 序列1: 静止状态
        self.play(FadeIn(ball), FadeIn(static_text))
        self.wait(2)

        # 匀速运动状态文字
        moving_text = Text("匀速运动状态", font_size=36, color=YELLOW).next_to(ball, UP)
        formula = MathTex(r"\text{F}_{\text{net}} = 0", font_size=36, color=WHITE)
        formula.next_to(ball, RIGHT)

        # 序列2: 球体匀速滑动
        self.play(FadeOut(static_text), FadeIn(moving_text))
        self.play(ball.animate.shift(RIGHT*6), FadeIn(formula), rate_func=smooth, run_time=3)
        self.wait(1)

        # 外力作用文字与箭头
        force_text = Text("外力作用", font_size=36, color=YELLOW).next_to(ball, UP)
        force_arrow = Arrow(start=LEFT*1.5, end=ORIGIN, color=RED, buff=0.1).next_to(ball, LEFT)

        # 序列3: 外力作用
        self.play(FadeOut(moving_text), FadeIn(force_arrow), FadeIn(force_text))
        self.play(ball.animate.shift(RIGHT*2), rate_func=accelerate, run_time=2)
        self.wait(1)

        # 惯性继续发挥作用文字
        inertia_text = Text("惯性继续发挥作用", font_size=36, color=YELLOW).next_to(ball, UP)

        # 序列4: 箭头消失，匀速运动
        self.play(FadeOut(force_arrow), FadeOut(force_text), FadeIn(inertia_text))
        self.play(ball.animate.shift(RIGHT*2), rate_func=smooth, run_time=2)
        self.wait(1)

        # 牛顿第一定律公式
        final_formula = MathTex(r"\text{F}_{\text{net}} = 0 \implies \text{v} = \text{constant}", font_size=48, color=WHITE)
        final_formula.shift(UP*1)

        # 注释
        annotation = Text("物体的运动状态只有在受外力时才会改变", font_size=24, color=YELLOW).next_to(final_formula, DOWN)

        # 序列5: 展示公式与注释
        self.play(FadeOut(ball), FadeOut(inertia_text), FadeOut(formula))
        self.play(FadeIn(final_formula), FadeIn(annotation))
        self.wait(3)