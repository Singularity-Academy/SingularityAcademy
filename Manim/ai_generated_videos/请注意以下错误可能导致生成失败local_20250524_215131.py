from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 深蓝背景
        self.camera.background_color = "#001f3f"
        
        # 地平线
        horizon = Line(start=LEFT*6, end=RIGHT*6, color=WHITE, stroke_width=2)
        horizon.shift(DOWN*2)
        self.add(horizon)
        
        # 星光点缀
        stars = VGroup(*[
            Dot(point=np.random.uniform(-6, 6)*RIGHT + np.random.uniform(-3, 3)*UP, color=WHITE, radius=0.02)
            for _ in range(50)
        ])
        self.add(stars)
        
        # 标题动画
        title = Text("Second Law of Thermodynamics", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # 红色小球和蓝色小球
        red_ball = Circle(radius=0.4, color=RED, fill_opacity=1).shift(LEFT*4 + DOWN*2)
        blue_ball = Circle(radius=0.4, color=BLUE, fill_opacity=1).shift(RIGHT*4 + DOWN*2)
        self.play(FadeIn(red_ball), FadeIn(blue_ball), run_time=2)
        self.wait(1)
        
        # 粒子流动画
        particles = VGroup(*[
            Dot(color=RED).shift(LEFT*4 + DOWN*2)
            for _ in range(20)
        ])
        for i, particle in enumerate(particles):
            particle.shift(RIGHT * i * 0.4)
            particle.set_color(interpolate_color(RED, BLUE, i / len(particles)))
        self.play(
            AnimationGroup(*[particle.animate.move_to(RIGHT*4 + DOWN*2) for particle in particles], lag_ratio=0.2),
            run_time=4
        )
        self.wait(1)
        
        # 显示熵公式
        entropy_formula = MathTex(r"\Delta S \geq 0", font_size=48, color=WHITE)
        entropy_formula.move_to(UP*1)
        self.play(Write(entropy_formula), run_time=2)
        
        # 熵背景条块动态增长
        entropy_bar = Rectangle(width=0.5, height=0.5, color=GREEN, fill_opacity=1)
        entropy_bar.move_to(DOWN*1.5)
        self.add(entropy_bar)
        self.play(
            entropy_bar.animate.scale(5).set_color(RED), 
            run_time=4
        )
        
        # 辅助文字
        auxiliary_text = Text("Entropy increases in irreversible processes", font_size=24, color=WHITE)
        auxiliary_text.move_to(DOWN*2.5)
        self.play(Write(auxiliary_text), run_time=2)
        
        # 强调不可逆
        irreversible_text = Text("irreversible", font_size=28, color=YELLOW)
        irreversible_text.next_to(auxiliary_text, RIGHT)
        self.play(Write(irreversible_text), run_time=1)
        
        # 停止粒子流，冻结场景
        self.wait(2)
        self.play(FadeOut(VGroup(*particles)), run_time=2)
        self.wait(2)
        
        # 结束动画
        self.play(FadeOut(VGroup(red_ball, blue_ball, entropy_formula, entropy_bar, auxiliary_text, irreversible_text, title, stars, horizon)))
        self.wait(1)