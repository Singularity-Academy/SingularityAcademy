from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 场景标题
        title = Text("热力学第二定律：熵的增长之旅", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景设置
        self.camera.background_color = "#001F3F"  # 深蓝色背景

        # 热源和冷源
        hot_source = Circle(radius=1, color=RED, fill_opacity=0.8).move_to(LEFT*4)
        cold_source = Circle(radius=1, color=BLUE, fill_opacity=0.8).move_to(RIGHT*4)
        self.play(FadeIn(hot_source), FadeIn(cold_source), run_time=2)
        self.wait(1)

        # 黄色箭头表示热量传递
        heat_arrow = Arrow(start=LEFT*3, end=RIGHT*3, color=YELLOW, stroke_width=6)
        self.play(Create(heat_arrow), run_time=2)
        
        # 热源颜色逐渐变暗，冷源颜色逐渐变浅
        self.play(
            hot_source.animate.set_fill(color=ORANGE, opacity=0.6),
            cold_source.animate.set_fill(color=LIGHT_BLUE, opacity=0.6),
            run_time=2
        )
        self.wait(1)

        # 显示熵公式
        entropy_formula = MathTex(r"\Delta S = \frac{Q}{T}", font_size=48)
        entropy_formula.move_to(DOWN*2)
        self.play(Write(entropy_formula), run_time=2)
        
        # 注解文字
        entropy_explanation = Text("熵是热量传递过程中不可逆的变化", font_size=24, color=WHITE)
        entropy_explanation.next_to(entropy_formula, DOWN)
        self.play(Write(entropy_explanation))
        self.wait(2)

        # 动态熵曲线图
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 5, 1],
            x_length=6,
            y_length=3,
            axis_config={"color": WHITE},
        ).to_edge(DOWN)

        labels = axes.get_axis_labels(x_label="时间", y_label="熵")
        self.play(Create(axes), Write(labels), run_time=2)

        entropy_curve = axes.plot(lambda x: 0.5 * x, x_range=[0, 9], color=YELLOW)
        self.play(Create(entropy_curve), run_time=3)
        
        # 曲线文字
        curve_text = Text("熵增加是不可逆的", font_size=24, color=WHITE)
        curve_text.next_to(entropy_curve, UP)
        self.play(Write(curve_text))
        self.wait(2)

        # 热源和冷源最终达到热平衡
        self.play(
            hot_source.animate.set_fill(color=GREY, opacity=0.8),
            cold_source.animate.set_fill(color=GREY, opacity=0.8),
            run_time=2
        )
        
        # 显示总结文字
        conclusion_text = Text("热力学第二定律：自然界中的能量趋于分散", font_size=32, color=WHITE)
        conclusion_text.move_to(DOWN*3)
        self.play(Write(conclusion_text))
        self.wait(3)

        # 场景淡出
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=2)