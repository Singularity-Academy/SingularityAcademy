from manim import *

class ExploreSineAndCosine(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#001A33"

        # 创建网格和星空效果（简化为网格）
        grid = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            background_line_style={"stroke_color": "#1E90FF", "stroke_opacity": 0.3}
        )
        self.add(grid)

        # 场景标题
        title = Text("探索正弦与余弦的奥秘", font_size=36, color=WHITE)
        subtitle = Text("从单位圆到波动世界", font_size=28, color=WHITE)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(2)

        # 创建单位圆和坐标轴
        unit_circle = Circle(radius=2, color=WHITE)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY}
        )
        self.play(Create(axes), Create(unit_circle))
        self.wait(1)

        # 动态角度线和黄色点
        angle_line = Line(ORIGIN, unit_circle.point_at_angle(0), color=YELLOW)
        moving_dot = Dot(unit_circle.point_at_angle(0), color=YELLOW)
        angle_value = MathTex(r"\theta", font_size=24, color=YELLOW).next_to(moving_dot, RIGHT)

        self.play(Create(angle_line), FadeIn(moving_dot), Write(angle_value))
        self.wait(1)

        # 正弦和余弦垂直线段
        sine_line = always_redraw(lambda: Line(moving_dot.get_center(), [moving_dot.get_x(), 0, 0], color=GREEN))
        cosine_line = always_redraw(lambda: Line(moving_dot.get_center(), [0, moving_dot.get_y(), 0], color=RED))
        self.add(sine_line, cosine_line)

        # 显示正弦和余弦公式
        sin_formula = MathTex(r"\sin(\theta) = \text{Y坐标}", font_size=24, color=RED).to_edge(RIGHT).shift(UP)
        cos_formula = MathTex(r"\cos(\theta) = \text{X坐标}", font_size=24, color=GREEN).to_edge(RIGHT).shift(DOWN)
        self.play(Write(sin_formula), Write(cos_formula))
        self.wait(1)

        # 动态角度变化动画
        def update_angle_line_and_dot(mob, dt):
            angle = mob.angle + dt * 2  # 每秒旋转 2 弧度
            mob.angle = angle
            angle_line.put_start_and_end_on(ORIGIN, unit_circle.point_at_angle(angle))
            moving_dot.move_to(unit_circle.point_at_angle(angle))
            angle_value.next_to(moving_dot, RIGHT)

        angle_line.add_updater(update_angle_line_and_dot)
        moving_dot.add_updater(update_angle_line_and_dot)
        self.wait(5)
        angle_line.remove_updater(update_angle_line_and_dot)
        moving_dot.remove_updater(update_angle_line_and_dot)

        # 动态生成正弦与余弦波
        sine_wave = axes.plot(lambda x: np.sin(x), color=RED)
        cosine_wave = axes.plot(lambda x: np.cos(x), color=GREEN)
        sine_label = Text("正弦波", font_size=24, color=RED).next_to(sine_wave, LEFT)
        cosine_label = Text("余弦波", font_size=24, color=GREEN).next_to(cosine_wave, LEFT)

        self.play(Create(sine_wave), Write(sine_label), run_time=2)
        self.play(Create(cosine_wave), Write(cosine_label), run_time=2)
        self.wait(2)

        # 显示波动公式
        wave_formula = MathTex(r"y = A \sin(\omega t + \phi)", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(wave_formula))
        self.wait(2)

        # 总结和静态展示
        summary_text = Text("正弦和余弦是周期性现象的数学语言", font_size=28, color=WHITE).next_to(wave_formula, UP)
        self.play(FadeIn(summary_text))
        self.wait(3)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)))