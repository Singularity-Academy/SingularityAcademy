from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#001F3F"
        stars = VGroup(*[Dot(color=WHITE, radius=0.02).move_to(
            np.random.uniform(-7, 7) * RIGHT + np.random.uniform(-4, 4) * UP
        ) for _ in range(100)])
        self.add(stars)
        self.play(FadeIn(stars), run_time=2)
        
        # 标题
        title = Text("热力学第二定律", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        
        # 熵公式展示
        entropy_formula = MathTex(r"\Delta S \geq 0", font_size=64, color=WHITE)
        entropy_formula.to_edge(DOWN)
        self.play(FadeIn(entropy_formula, scale=0.5), run_time=1.5)
        self.wait(1)
        
        # 容器展示
        container_left = Rectangle(width=3, height=2, color=WHITE)
        container_left.shift(LEFT * 4)
        container_right = Rectangle(width=3, height=2, color=WHITE)
        container_right.shift(RIGHT * 4)
        self.play(Create(container_left), Create(container_right), run_time=1)
        
        # 气体分子
        molecules = VGroup(*[Dot(color=WHITE, radius=0.05).move_to(
            np.random.uniform(-1, 1) * RIGHT + np.random.uniform(-0.8, 0.8) * UP + LEFT * 4
        ) for _ in range(30)])
        self.play(FadeIn(molecules), run_time=1)
        
        # 气体扩散动画
        self.play(
            molecules.animate.arrange_in_grid(rows=5, buff=0.3).move_to(ORIGIN),
            run_time=3,
            rate_func=smooth
        )
        self.wait(1)
        
        # 熵计量条
        entropy_bar = Rectangle(width=7, height=0.4, color=GREEN, fill_opacity=1)
        entropy_bar.to_edge(DOWN, buff=1)
        self.play(FadeIn(entropy_bar), run_time=0.5)
        
        entropy_bar_high = Rectangle(width=7, height=0.4, color=RED, fill_opacity=1)
        entropy_bar_high.match_width(entropy_bar)
        entropy_bar_high.to_edge(DOWN, buff=1)
        self.play(Transform(entropy_bar, entropy_bar_high), run_time=3, rate_func=smooth)
        self.wait(1)
        
        # 公式强调
        self.play(entropy_formula.animate.scale(1.2).set_color(YELLOW), run_time=1)
        self.play(entropy_formula.animate.set_color(WHITE), run_time=1)
        self.wait(1)
        
        # 总结文字
        summary_text = Text("孤立系统的熵总是增加或保持不变。", font_size=36, color=WHITE)
        summary_text.move_to(DOWN * 2)
        self.play(Write(summary_text), run_time=2)
        self.wait(2)
        
        # 结束
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=2)