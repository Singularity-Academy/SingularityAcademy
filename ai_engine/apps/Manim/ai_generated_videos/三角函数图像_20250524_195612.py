from manim import *

class ExploreTrigFunctions(Scene):
    def construct(self):
        # 设置背景颜色和闪烁星星
        self.camera.background_color = "#001f3f"
        stars = VGroup(*[
            Dot(point=[x, y, 0], radius=0.02, color=WHITE).set_opacity(0.5)
            for x, y in zip(
                np.random.uniform(-7, 7, 50),
                np.random.uniform(-4, 4, 50)
            )
        ])
        self.add(stars)
        self.play(FadeIn(stars), run_time=2)
        
        # 绘制坐标系
        axes = Axes(
            x_range=[-2 * PI, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": [-2 * PI, -PI, 0, PI, 2 * PI]},
            y_axis_config={"numbers_to_include": [-1, 0, 1]},
        )
        labels = axes.get_axis_labels(
            x_label=MathTex("x"),
            y_label=MathTex("y")
        )
        grid = axes.get_grid_lines(color=GREY)

        self.play(Create(axes), Create(grid), Write(labels), run_time=2)
        
        # 添加公式展示
        sin_formula = MathTex(r"y = \sin(x)", color=RED).to_edge(UP)
        cos_formula = MathTex(r"y = \cos(x)", color=BLUE).next_to(sin_formula, DOWN)
        self.play(Write(sin_formula), Write(cos_formula), run_time=2)
        
        # 动态绘制正弦函数
        sin_curve = axes.plot(lambda x: np.sin(x), x_range=[-2 * PI, 2 * PI], color=RED)
        sin_dot = Dot(color=YELLOW).move_to(axes.c2p(0, np.sin(0)))
        sin_label = Text("正弦函数的实时点", font_size=24, color=YELLOW).next_to(sin_dot, RIGHT)
        
        self.play(Create(sin_curve), FadeIn(sin_dot), Write(sin_label), run_time=2)
        
        sin_tracker = ValueTracker(0)
        sin_dot.add_updater(lambda m: m.move_to(axes.c2p(sin_tracker.get_value(), np.sin(sin_tracker.get_value()))))
        
        self.play(sin_tracker.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        self.wait(1)
        
        # 动态绘制余弦函数
        cos_curve = axes.plot(lambda x: np.cos(x), x_range=[-2 * PI, 2 * PI], color=BLUE)
        cos_dot = Dot(color=YELLOW).move_to(axes.c2p(0, np.cos(0)))
        cos_label = Text("余弦函数的实时点", font_size=24, color=YELLOW).next_to(cos_dot, RIGHT)
        
        self.play(Create(cos_curve), FadeIn(cos_dot), Write(cos_label), run_time=2)
        
        cos_tracker = ValueTracker(0)
        cos_dot.add_updater(lambda m: m.move_to(axes.c2p(cos_tracker.get_value(), np.cos(cos_tracker.get_value()))))
        
        self.play(cos_tracker.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        self.wait(1)
        
        # 展示关键点和周期
        sin_peak = axes.c2p(PI / 2, 1)
        sin_valley = axes.c2p(3 * PI / 2, -1)
        cos_start = axes.c2p(0, 1)
        cos_period = axes.c2p(2 * PI, 1)
        
        key_points = VGroup(
            Dot(sin_peak, color=YELLOW),
            Dot(sin_valley, color=YELLOW),
            Dot(cos_start, color=YELLOW),
            Dot(cos_period, color=YELLOW)
        )
        key_labels = VGroup(
            Text("峰值", font_size=20, color=YELLOW).next_to(sin_peak, UP),
            Text("谷值", font_size=20, color=YELLOW).next_to(sin_valley, DOWN),
            Text("起点", font_size=20, color=YELLOW).next_to(cos_start, LEFT),
            Text("周期结束", font_size=20, color=YELLOW).next_to(cos_period, RIGHT)
        )
        
        self.play(FadeIn(key_points), Write(key_labels), run_time=2)
        self.wait(2)
        
        # 展示相位差
        phase_line = DashedLine(axes.c2p(0, 0), axes.c2p(PI / 2, 0), color=GREEN)
        phase_label = Text("相位差 π/2", font_size=24, color=GREEN).next_to(phase_line, UP)
        self.play(Create(phase_line), Write(phase_label), run_time=2)
        self.wait(2)
        
        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)), run_time=2)