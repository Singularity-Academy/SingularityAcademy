from manim import *

class ThermodynamicsEntropy(Scene):
    def construct(self):
        # 场景标题
        title = Text("不可逆的热力学魔法：熵总是增加！", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 设置背景
        background = Rectangle(width=14, height=8, fill_color=BLUE_E, fill_opacity=1).to_edge(ORIGIN)
        stars = VGroup(*[Dot(color=WHITE).shift((LEFT*6 + UP*3) + (RIGHT*12 * np.random.rand() + DOWN*6 * np.random.rand())) for _ in range(50)])
        self.add(background, stars)

        # 创建红球和蓝球
        red_ball = Circle(radius=1, color=RED, fill_color=RED, fill_opacity=0.8).shift(LEFT*3)
        blue_ball = Circle(radius=1, color=BLUE, fill_color=BLUE, fill_opacity=0.8).shift(RIGHT*3)
        self.play(FadeIn(red_ball), FadeIn(blue_ball))
        
        # 显示“孤立系统”文字
        isolated_system_text = Text("孤立系统", font_size=32, color=WHITE).next_to(red_ball, UP, buff=1.5).shift(RIGHT * 3)
        self.play(Write(isolated_system_text))
        self.wait(1)

        # 热量流动动画
        heat_arrow = Arrow(start=red_ball.get_center(), end=blue_ball.get_center(), color=YELLOW, buff=0.2)
        self.play(Create(heat_arrow))
        self.wait(0.5)

        # 红球逐渐变暗，蓝球逐渐变亮
        self.play(red_ball.animate.set_fill(opacity=0.5), blue_ball.animate.set_fill(opacity=1.0), run_time=2)

        # 显示动态条形图表示熵的增加
        entropy_bar = Rectangle(width=1, height=0.5, color=GREEN, fill_color=GREEN, fill_opacity=0.8).to_edge(DOWN).shift(LEFT*5)
        entropy_text = Text("熵值", font_size=24, color=WHITE).next_to(entropy_bar, UP, buff=0.2)
        self.play(FadeIn(entropy_text), FadeIn(entropy_bar))
        
        for i in range(1, 5):
            new_height = 0.5 + i * 0.5
            self.play(entropy_bar.animate.stretch_to_fit_height(new_height, about_edge=DOWN), run_time=1)

        # 显示公式 ΔS ≥ 0
        entropy_formula = MathTex(r"\Delta S \geq 0", font_size=48, color=YELLOW).to_edge(UP).shift(DOWN*1.5)
        self.play(Write(entropy_formula))
        self.wait(1)

        # 两球最终颜色趋于一致，背景星点闪烁
        self.play(red_ball.animate.set_fill(opacity=0.8), blue_ball.animate.set_fill(opacity=0.8))
        for star in stars:
            self.play(star.animate.set_opacity(np.random.rand()), run_time=0.1)

        # 显示总结文字“熵总是增加！”
        summary_text = Text("熵总是增加！", font_size=36, color=GOLD).to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(2)

        # 结束动画，留下公式
        self.play(FadeOut(Group(*self.mobjects)))
        self.play(FadeIn(entropy_formula))
        self.wait(2)