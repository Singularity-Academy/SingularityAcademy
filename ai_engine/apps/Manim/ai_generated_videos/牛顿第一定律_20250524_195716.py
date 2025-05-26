from manim import *

class NewtonFirstLawVisualization(Scene):
    def construct(self):
        # 设置背景
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color=BLUE, fill_opacity=1)
        self.add(background)
        
        # 标题：牛顿第一定律
        title = Text("牛顿第一定律", font_size=48, color=YELLOW)
        title.to_edge(UP)
        self.play(FadeIn(title, run_time=2))
        self.wait(1)

        # 地面
        ground = Line(start=LEFT, end=RIGHT, color=GRAY, stroke_width=4).shift(DOWN * 2)
        self.play(Create(ground, run_time=2))
        self.wait(1)

        # 步骤 2: 静止演示
        static_ball = Circle(radius=0.3, color=WHITE, fill_opacity=1).shift(DOWN * 1.8 + LEFT * 3)
        self.play(FadeIn(static_ball, run_time=1))
        
        # 红色箭头表示外力
        force_arrow = Arrow(start=LEFT * 4 + DOWN * 1.8, end=LEFT * 3 + DOWN * 1.8, color=RED, buff=0.1)
        self.play(GrowArrow(force_arrow, run_time=1))
        self.wait(1)
        self.play(FadeOut(force_arrow, run_time=1))
        
        # 旁白文字
        static_text = Text("当没有外力作用时，物体保持静止。", font_size=24, color=WHITE).next_to(static_ball, UP)
        self.play(Write(static_text, run_time=2))
        self.wait(2)
        self.play(FadeOut(static_text))

        # 步骤 3: 匀速运动演示
        moving_ball = Circle(radius=0.3, color=WHITE, fill_opacity=1).shift(DOWN * 1.8 + LEFT * 3)
        self.play(FadeIn(moving_ball, run_time=1))
        
        # 动画：球匀速滑动
        self.play(moving_ball.animate.shift(RIGHT * 6), run_time=3, rate_func=linear)
        
        # 旁白文字
        moving_text = Text("若物体已经在运动，且未受外力，其将保持匀速直线运动。", font_size=24, color=WHITE).next_to(moving_ball, UP)
        self.play(Write(moving_text, run_time=2))
        self.wait(2)
        self.play(FadeOut(moving_text))

        # 步骤 4: 数学公式展示
        formula = MathTex(r"F = 0 \implies v = \text{常数}", font_size=48).shift(UP * 0.5)
        formula_annotation = Text("没有外力时，速度保持不变。", font_size=24, color=WHITE).next_to(formula, DOWN)
        self.play(Write(formula, run_time=2))
        self.play(FadeIn(formula_annotation, run_time=2))
        self.wait(2)

        # 步骤 5: 总结强调
        self.play(FadeOut(formula_annotation, run_time=1))
        self.play(
            static_ball.animate.scale(0.5).shift(LEFT * 2),
            moving_ball.animate.scale(0.5).shift(RIGHT * 2),
            FadeOut(formula, run_time=2),
        )
        self.wait(1)

        # 重新高亮标题
        self.play(ApplyWave(title, run_time=2))
        self.wait(1)

        # 背景星星闪烁效果
        stars = VGroup(
            *[Dot(color=WHITE).move_to([x, y, 0]) for x, y in zip(
                np.random.uniform(-FRAME_WIDTH / 2, FRAME_WIDTH / 2, 20),
                np.random.uniform(-FRAME_HEIGHT / 2, FRAME_HEIGHT / 2, 20)
            )]
        )
        self.play(FadeIn(stars, run_time=2))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects), run_time=2))