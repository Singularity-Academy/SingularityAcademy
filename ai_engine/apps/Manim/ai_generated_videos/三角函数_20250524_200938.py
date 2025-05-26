from manim import *

class ExploreSineFunction(Scene):
    def construct(self):
        # 设置背景颜色为浅蓝色
        self.camera.background_color = "#87CEEB"  

        # 添加辅助网格
        grid = NumberPlane(
            x_range=[-7, 7, 1], 
            y_range=[-4, 4, 1], 
            color=GRAY, 
            faded_line_ratio=2
        )
        self.add(grid)

        # 标题
        title = Text("探索三角函数的奥秘", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(FadeIn(title), run_time=1.5)

        # 单位圆和坐标轴
        unit_circle = Circle(radius=2, color=WHITE)
        axes = Axes(
            x_range=[-3, 3, 1], 
            y_range=[-3, 3, 1], 
            axis_config={"color": WHITE}
        ).scale(1.5)
        self.play(Create(unit_circle), Create(axes), run_time=2)

        # 数学公式
        formula = MathTex(r"\sin(\theta) = \text{y-coordinate of point on unit circle}", color=YELLOW)
        formula.to_edge(DOWN)
        self.play(Write(formula), run_time=2)

        # 动态角度标注与红点
        theta_tracker = ValueTracker(0)  # 追踪角度值
        angle_arc = always_redraw(
            lambda: Arc(
                radius=1.5, 
                start_angle=0, 
                angle=theta_tracker.get_value(), 
                color=GREEN
            )
        )
        dot = always_redraw(
            lambda: Dot(
                point=[2 * np.cos(theta_tracker.get_value()), 2 * np.sin(theta_tracker.get_value()), 0], 
                color=RED
            )
        )
        self.add(angle_arc, dot)

        # 垂线
        vertical_line = always_redraw(
            lambda: Line(
                start=dot.get_center(), 
                end=[dot.get_center()[0], 0, 0], 
                color=YELLOW
            )
        )
        self.add(vertical_line)

        # 右侧正弦波坐标系
        sine_axes = Axes(
            x_range=[0, 2 * PI, PI / 2], 
            y_range=[-1.5, 1.5, 0.5], 
            axis_config={"color": BLUE}
        ).shift(RIGHT * 4)
        self.play(Create(sine_axes), run_time=2)
        
        sine_wave = VGroup()  # 用于动态生成正弦波点和线
        sine_graph = always_redraw(
            lambda: sine_axes.plot(
                lambda x: np.sin(x), 
                x_range=[0, theta_tracker.get_value()], 
                color=BLUE
            )
        )
        self.add(sine_graph)

        # 动态展示角度变化
        self.play(theta_tracker.animate.set_value(2 * PI), run_time=10, rate_func=linear)

        # 总结与强调
        summary_text = Text("三角函数连接了圆和波形的世界！", font_size=30, color=YELLOW)
        summary_text.to_edge(DOWN)
        self.play(FadeIn(summary_text), run_time=2)

        # 整体收尾
        self.play(FadeOut(Group(*self.mobjects)), run_time=2)