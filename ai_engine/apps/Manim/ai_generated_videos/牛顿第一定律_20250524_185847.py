from manim import *

class NewtonFirstLawScene(Scene):
    def construct(self):
        # 设置渐变背景颜色
        background = Rectangle(height=FRAME_HEIGHT, width=FRAME_WIDTH)
        background.set_fill(color=[BLUE, PURPLE], opacity=1)
        background.set_stroke(width=0)
        self.add(background)

        # 添加地面线
        ground = Line(start=LEFT * 6, end=RIGHT * 6, color=WHITE, stroke_width=2).shift(DOWN * 2)
        self.add(ground)

        # 添加星空背景点缀
        stars = VGroup(*[Dot(color=WHITE).shift(
            LEFT * np.random.uniform(-6, 6) + UP * np.random.uniform(-3, 3)
        ) for _ in range(50)])
        self.add(stars)

        # 场景标题
        title = Text("惯性与静止的秘密：牛顿第一定律动画解读", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 场景1: 静止状态展示
        ball = Circle(radius=0.3, color=YELLOW, fill_opacity=1).shift(DOWN * 2)
        f0_label = Text("F=0", font_size=24, color=WHITE).next_to(ball, UP)
        explanation1 = Text("物体在没有外力作用时保持静止或匀速运动", font_size=24, color=GREEN).shift(DOWN * 3)

        self.play(FadeIn(ball), Write(f0_label), Write(explanation1))
        self.wait(3)

        # 场景2: 匀速运动状态展示
        explanation2 = Text("匀速运动是惯性的体现", font_size=24, color=GREEN).shift(DOWN * 3)
        self.play(FadeOut(explanation1), Write(explanation2))
        self.play(ball.animate.shift(RIGHT * 3), run_time=3, rate_func=linear)
        self.wait(1)

        # 场景3: 外力作用并加速
        force_arrow = Arrow(start=LEFT * 3 + DOWN * 2, end=LEFT * 2 + DOWN * 2, color=RED, buff=0.1)
        explanation3 = Text("外力作用会改变物体的运动状态", font_size=24, color=GREEN).shift(DOWN * 3)

        self.play(FadeOut(explanation2), FadeIn(force_arrow), Write(explanation3))
        self.play(ball.animate.shift(RIGHT * 4).scale(1.2), run_time=3, rate_func=rush_into)
        self.wait(1)

        # 场景4: 外力消失，物体继续匀速运动
        explanation4 = Text("没有外力时，运动状态不会改变", font_size=24, color=GREEN).shift(DOWN * 3)
        self.play(FadeOut(force_arrow), FadeOut(explanation3), Write(explanation4))
        self.play(ball.animate.shift(RIGHT * 3), run_time=3, rate_func=linear)
        self.wait(2)

        # 场景5: 牛顿第一定律公式展示
        formula = MathTex(r"\text{若}\, F = 0, \, \text{则物体保持静止或匀速运动}", font_size=36, color=WHITE)
        formula.shift(UP * 1)
        explanation5 = Text("牛顿第一定律的核心思想", font_size=24, color=GREEN).shift(DOWN * 3)

        self.play(FadeOut(ball), FadeOut(explanation4), Write(formula), Write(explanation5))
        self.wait(3)

        # 淡出场景
        self.play(FadeOut(Group(*self.mobjects)))