from manim import *

class ExploreSineCosine(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = DARK_BLUE

        # 中文标题
        title = Text("探索正弦与余弦的神秘波动", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建单位圆和坐标轴
        unit_circle = Circle(radius=2, color=WHITE)
        axes = Axes(
            x_range=[-PI, PI, PI/4],
            y_range=[-1, 1, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"color": WHITE},
            tips=False
        ).shift(RIGHT*4)
        x_axis_label = Text("x轴", font_size=24, color=GREEN).next_to(axes.x_axis, DOWN)
        y_axis_label = Text("y轴", font_size=24, color=YELLOW).next_to(axes.y_axis, LEFT)

        # 添加单位圆和坐标轴到场景中
        self.play(Create(unit_circle), Create(axes), FadeIn(x_axis_label), FadeIn(y_axis_label))
        self.wait(1)

        # 添加单位圆的动态点
        moving_dot = Dot(color=YELLOW).move_to(unit_circle.point_at_angle(0))
        theta = ValueTracker(0)
        dot_label = MathTex(r"\theta", font_size=24, color=WHITE).next_to(moving_dot, UP)

        # 垂直虚线和正弦曲线
        vertical_line = always_redraw(
            lambda: Line(
                moving_dot.get_center(), 
                [axes.coords_to_point(theta.get_value(), np.sin(theta.get_value()))[0], 
                 axes.coords_to_point(theta.get_value(), np.sin(theta.get_value()))[1], 0],
                color=RED, stroke_width=2, dash_length=0.1
            )
        )
        sine_graph = axes.plot(lambda x: np.sin(x), color=RED)

        # 水平虚线和余弦曲线
        horizontal_line = always_redraw(
            lambda: Line(
                moving_dot.get_center(), 
                [axes.coords_to_point(theta.get_value(), np.cos(theta.get_value()))[0], 
                 axes.coords_to_point(theta.get_value(), np.cos(theta.get_value()))[1], 0],
                color=BLUE, stroke_width=2, dash_length=0.1
            )
        )
        cosine_graph = axes.plot(lambda x: np.cos(x), color=BLUE)

        # 动态点的移动
        self.play(FadeIn(moving_dot), FadeIn(dot_label))
        self.add(vertical_line, horizontal_line)

        # 动画：点沿单位圆移动，同时绘制波形
        self.play(
            theta.animate.set_value(PI*2),
            UpdateFromFunc(moving_dot, lambda m: m.move_to(unit_circle.point_at_angle(theta.get_value()))),
            run_time=12, rate_func=linear
        )

        # 分屏显示单位圆和波形
        self.play(unit_circle.animate.shift(LEFT*4), run_time=2)
        self.wait(1)

        # 添加正弦与余弦公式
        sin_text = MathTex(r"sin(\theta) = y/r", font_size=24, color=RED).next_to(sine_graph, UP)
        cos_text = MathTex(r"cos(\theta) = x/r", font_size=24, color=BLUE).next_to(cosine_graph, DOWN)
        self.play(Write(sin_text), Write(cos_text))
        self.wait(1)

        # 总结文本
        summary_text = Text("正弦与余弦：从圆到波的奇妙映射", font_size=28, color=WHITE).to_edge(DOWN)
        self.play(FadeIn(summary_text))
        self.wait(3)

        # 结束动画
        self.play(FadeOut(Group(unit_circle, axes, x_axis_label, y_axis_label, moving_dot, dot_label, sin_text, cos_text, vertical_line, horizontal_line, summary_text)))
        self.wait(2)