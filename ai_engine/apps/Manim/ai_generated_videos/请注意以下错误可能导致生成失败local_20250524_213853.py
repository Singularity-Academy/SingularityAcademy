from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#001F4D"  # 深蓝色背景
        
        # 热源和冷源
        hot_source = Rectangle(width=2, height=4, color=RED, fill_color=RED, fill_opacity=0.8)
        cold_source = Rectangle(width=2, height=4, color=BLUE, fill_color=BLUE, fill_opacity=0.8)
        hot_source.move_to(LEFT*4)
        cold_source.move_to(RIGHT*4)
        
        hot_label = Text("热源", font_size=32, color=WHITE).next_to(hot_source, UP)
        cold_label = Text("冷源", font_size=32, color=WHITE).next_to(cold_source, UP)

        # 分隔器
        separator = Rectangle(width=0.2, height=4, color=WHITE, fill_opacity=1)
        separator.move_to(ORIGIN)
        
        # 中央公式框
        formula_box = Rectangle(width=4, height=1.5, color=WHITE)
        formula_box.move_to(DOWN * 2)
        
        entropy_formula = MathTex(r"\Delta S \geq 0", font_size=48, color=WHITE)
        entropy_formula.move_to(formula_box.get_center())
        
        # 粒子初始化
        particles = VGroup(*[Dot(point=LEFT*3 + np.random.random(2) * 2 - np.array([1, 1]), color=YELLOW) for _ in range(50)])
        
        # 热源和冷源的动态展示
        self.play(FadeIn(hot_source), FadeIn(cold_source), FadeIn(hot_label), FadeIn(cold_label))
        self.play(Create(separator))
        self.wait(1)
        
        # 粒子展示
        self.play(FadeIn(particles))
        self.wait(1)
        
        # 分隔器打开动画
        self.play(separator.animate.shift(UP*5), run_time=2)
        
        # 粒子运动模拟
        def update_particles(particle_group):
            for particle in particle_group:
                particle.shift(np.random.random(2) * 0.1 - 0.05)
        
        particles.add_updater(update_particles)
        self.wait(3)
        particles.remove_updater(update_particles)
        
        # 熵公式展示
        self.play(FadeIn(formula_box), Write(entropy_formula))
        self.wait(1)
        
        # 动态箭头展示
        arrow = Arrow(start=hot_source.get_right(), end=cold_source.get_left(), color=YELLOW, stroke_width=4)
        self.play(Create(arrow))
        self.wait(1)
        
        # 动态文字展示
        entropy_text = Text("熵增加", font_size=32, color=WHITE)
        entropy_text.move_to(formula_box.get_top() + UP*0.5)
        self.play(Write(entropy_text))
        self.wait(1)
        
        # 结束动画，粒子均匀分布
        all_particles = VGroup(*[Dot(point=np.random.random(2) * 8 - np.array([4, 4]), color=YELLOW) for _ in range(100)])
        self.play(Transform(particles, all_particles), run_time=3)
        
        # 混合颜色的背景淡入
        mixed_background = Rectangle(width=16, height=9, fill_color=WHITE, fill_opacity=0.2)
        self.play(FadeIn(mixed_background), run_time=2)
        
        # 熵公式最终显示
        self.play(entropy_formula.animate.scale(1.5).move_to(ORIGIN))
        self.wait(2)
        
        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=2)