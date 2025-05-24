from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 深蓝色背景
        self.camera.background_color = "#001f3f"
        
        # 星光点缀
        stars = VGroup(*[Dot(point=np.random.random(3) * np.array([14, 8, 0]) - np.array([7, 4, 0]), 
                             radius=0.02, color=WHITE, fill_opacity=0.6) for _ in range(50)])
        self.add(stars)

        # 标题
        title = Text("热力学第二定律", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # 平坦表面
        surface = Line(start=LEFT * 6 + DOWN * 3, end=RIGHT * 6 + DOWN * 3, color=WHITE)
        self.play(Create(surface), run_time=2)
        self.wait(0.5)

        # 热库和热机
        hot_reservoir = Rectangle(width=2, height=1, color=RED, fill_opacity=0.6)
        cold_reservoir = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.6)
        hot_reservoir.shift(LEFT * 4 + DOWN * 2)
        cold_reservoir.shift(RIGHT * 4 + DOWN * 2)
        hot_label = MathTex(r"T_\text{hot}", color=WHITE).next_to(hot_reservoir, UP)
        cold_label = MathTex(r"T_\text{cold}", color=WHITE).next_to(cold_reservoir, UP)

        heat_machine = VGroup(
            Circle(radius=0.6, color=YELLOW, fill_opacity=0.3), 
            Line(start=LEFT * 0.5, end=RIGHT * 0.5, color=YELLOW),
            Line(start=UP * 0.5, end=DOWN * 0.5, color=YELLOW)
        )
        heat_machine.move_to(DOWN * 2)

        self.play(FadeIn(hot_reservoir), FadeIn(cold_reservoir), FadeIn(heat_machine))
        self.play(Write(hot_label), Write(cold_label))
        self.wait(1)

        # 热量流动箭头
        arrow = Arrow(start=hot_reservoir.get_right(), end=cold_reservoir.get_left(), color=ORANGE, buff=0.1)
        self.play(Create(arrow), run_time=2)
        self.wait(0.5)

        # 熵公式
        entropy_formula = MathTex(r"\Delta S \geq 0", color=GREEN).to_edge(UP * 2.5)
        self.play(Write(entropy_formula), run_time=2)
        self.wait(1)

        # 不可逆过程动画
        heat_flow_text = Text("热量流动", font_size=32, color=ORANGE).next_to(arrow, UP)
        self.play(Write(heat_flow_text), run_time=2)
        self.wait(0.5)

        entropy_bar = Rectangle(width=0.5, height=1, color=GREEN, fill_opacity=0.6)
        entropy_bar.move_to(DOWN * 3 + RIGHT * 2)
        entropy_label = MathTex(r"\Delta S", color=WHITE).next_to(entropy_bar, UP)
        self.play(FadeIn(entropy_bar), Write(entropy_label))
        self.wait(0.5)

        for i in range(1, 6):
            new_bar = Rectangle(width=0.5, height=1 + i * 0.5, color=GREEN, fill_opacity=0.6)
            new_bar.move_to(DOWN * 3 + RIGHT * 2)
            self.play(Transform(entropy_bar, new_bar), run_time=0.5)
            self.wait(0.2)

        # 总结文字
        summary_text = Text("热量总是从高温流向低温，熵始终增加", font_size=32, color=WHITE).to_edge(DOWN)
        self.play(Write(summary_text), run_time=2)
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=2)