from manim import *

class ExploreSineCosine(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#001F3F"  # 深蓝色背景
        
        # 中文标题
        title = Text("探索正弦和余弦：旋转中的美妙曲线", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 场景中央的单位圆及坐标轴
        unit_circle = Circle(radius=2, color=GREY)
        x_axis = Line(start=[-3, 0, 0], end=[3, 0, 0], color=WHITE)
        y_axis = Line(start=[0, -3, 0], end=[0, 3, 0], color=WHITE)
        self.play(Create(unit_circle), Create(x_axis), Create(y_axis))
        self.wait(1)

        # 半径线和角度标记
        radius_line = Line(start=[0, 0, 0], end=[2, 0, 0], color=YELLOW)
        angle_arc = Arc(radius=0.5, start_angle=0, angle=PI/4, color=GREEN)
        angle_label = MathTex(r"\theta", color=GREEN).next_to(angle_arc, RIGHT)
        
        self.play(Create(radius_line), Create(angle_arc), Write(angle_label))
        self.wait(1)

        # 动态展示正弦和余弦投影线
        sine_projection = Line(start=[1.414, 0, 0], end=[1.414, 1.414, 0], color=RED)
        cosine_projection = Line(start=[0, 1.414, 0], end=[1.414, 1.414, 0], color=BLUE)
        self.play(Create(sine_projection), Create(cosine_projection))
        self.wait(1)

        # 正弦和余弦函数的公式
        sine_formula = MathTex(r"\sin(\theta) = \text{y投影}", color=RED).to_edge(LEFT)
        cosine_formula = MathTex(r"\cos(\theta) = \text{x投影}", color=BLUE).to_edge(RIGHT)
        self.play(Write(sine_formula), Write(cosine_formula))
        self.wait(1)

        # 函数图像展示
        sine_graph = Axes(
            x_range=[0, 2 * PI, PI / 4],
            y_range=[-1, 1, 0.5],
            axis_config={"color": WHITE},
        ).to_edge(RIGHT).shift(UP)
        cosine_graph = Axes(
            x_range=[0, 2 * PI, PI / 4],
            y_range=[-1, 1, 0.5],
            axis_config={"color": WHITE},
        ).to_edge(RIGHT).shift(DOWN)
        
        self.play(Create(sine_graph), Create(cosine_graph))
        self.wait(1)

        # 动态绘制正弦和余弦函数曲线
        sine_curve = sine_graph.plot(lambda x: np.sin(x), color=RED)
        cosine_curve = cosine_graph.plot(lambda x: np.cos(x), color=BLUE)
        
        self.play(Create(sine_curve), run_time=3)
        self.play(Create(cosine_curve), run_time=3)
        self.wait(1)

        # 加速展示旋转一圈
        self.play(
            Rotate(radius_line, angle=2 * PI, about_point=[0, 0, 0], rate_func=smooth, run_time=3),
            Rotate(angle_arc, angle=2 * PI, about_point=[0, 0, 0], rate_func=smooth, run_time=3),
        )
        self.wait(1)

        # 标记周期和对称性
        sine_period = MathTex(r"\text{周期: } 2\pi", color=RED).next_to(sine_graph, DOWN)
        cosine_period = MathTex(r"\text{周期: } 2\pi", color=BLUE).next_to(cosine_graph, DOWN)
        sine_peak = Text("峰值: 1 和 -1", font_size=24, color=RED).next_to(sine_period, DOWN)
        cosine_peak = Text("峰值: 1 和 -1", font_size=24, color=BLUE).next_to(cosine_period, DOWN)

        self.play(Write(sine_period), Write(cosine_period))
        self.play(Write(sine_peak), Write(cosine_peak))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)