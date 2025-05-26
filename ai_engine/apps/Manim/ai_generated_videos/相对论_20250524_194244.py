from manim import *

class SpecialRelativityScene(Scene):
    def construct(self):
        # 设置背景颜色为深蓝色
        self.camera.background_color = "#1E1E2E"
        
        # 场景标题
        title = Text("光速之下：揭示相对论的奥秘", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 添加背景星星点缀
        stars = VGroup(*[Dot(color=WHITE).scale(0.5).move_to(
            [x, y, 0]) for x, y in zip(
            np.random.uniform(-7, 7, 50),
            np.random.uniform(-4, 4, 50))])
        self.add(stars)

        # 静止观察者和时钟
        observer = Text("观察者 A", font_size=24, color=WHITE)
        observer.shift(LEFT * 3 + DOWN * 1.5)
        clock = Circle(color=WHITE).scale(0.5).next_to(observer, RIGHT)
        clock_label = Text("标准时间", font_size=16, color=WHITE).next_to(clock, DOWN)
        self.play(FadeIn(observer), Create(clock), Write(clock_label))

        # 火箭和标签
        rocket = Polygon(
            [0, 0, 0], [0.5, 0, 0], [0.25, 1, 0],
            color=RED, fill_opacity=1
        ).scale(0.8).shift(RIGHT * 3)
        rocket_label = Text("火箭 B", font_size=24, color=WHITE).next_to(rocket, UP)
        self.play(FadeIn(rocket), Write(rocket_label))

        self.wait(1)

        # 经典力学公式
        classical_formula = MathTex(r"v = \frac{d}{t}", color=WHITE)
        classical_formula.to_edge(UP).shift(DOWN * 0.5)
        self.play(Write(classical_formula))
        self.wait(1)

        # 火箭低速移动
        self.play(rocket.animate.shift(LEFT * 2), run_time=3, rate_func=linear)
        self.wait(1)
        
        # 火箭加速至接近光速
        self.play(rocket.animate.shift(RIGHT * 4), run_time=2, rate_func=rush_into)

        # 光波线条与光速公式
        light_wave = VGroup(*[
            Arc(radius=0.5, start_angle=0, angle=PI, color=YELLOW).shift(
                RIGHT * 3 + UP * (i * 0.2)) for i in range(8)
        ])
        light_speed_formula = MathTex(r"c = 3 \times 10^8 \, \text{m/s}", color=YELLOW)
        light_speed_formula.next_to(light_wave, UP)
        self.play(FadeIn(light_wave), Write(light_speed_formula))
        self.wait(1)
        
        # 时间膨胀公式与效果
        time_dilation_formula = MathTex(
            r"\Delta t' = \Delta t \sqrt{1 - \frac{v^2}{c^2}}", color=WHITE
        ).to_edge(LEFT).shift(UP * 2)
        self.play(Write(time_dilation_formula))
        
        slow_clock = Circle(color=WHITE).scale(0.5).next_to(rocket, RIGHT)
        slow_clock_label = Text("膨胀时间", font_size=16, color=WHITE).next_to(slow_clock, DOWN)
        self.play(Create(slow_clock), Write(slow_clock_label))
        self.wait(1)

        # 火箭时间变慢动画
        self.play(slow_clock.animate.scale(0.8), run_time=2, rate_func=smooth)
        self.wait(1)

        # 长度收缩公式与效果
        length_contraction_formula = MathTex(
            r"L' = L \sqrt{1 - \frac{v^2}{c^2}}", color=WHITE
        ).to_edge(RIGHT).shift(UP * 2)
        self.play(Write(length_contraction_formula))
        
        # 火箭长度缩短动画
        self.play(rocket.animate.scale(0.5, about_edge=LEFT), run_time=2, rate_func=smooth)
        self.wait(1)

        # 火箭到达终点
        self.play(rocket.animate.shift(RIGHT * 2), run_time=2, rate_func=smooth)

        # 总结文字
        summary_text = Text(
            "时间和空间随着速度发生变化，这是狭义相对论的核心。",
            font_size=28, color=WHITE
        )
        self.play(FadeOut(Group(clock, clock_label, rocket_label, slow_clock, slow_clock_label, classical_formula, 
                                time_dilation_formula, length_contraction_formula, light_wave, light_speed_formula)),
                  FadeIn(summary_text))
        self.wait(2)

        # 结束
        self.play(FadeOut(Group(title, stars, summary_text)))