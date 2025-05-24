from manim import *

class TrigonometricDance(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1a1a2e"
        
        # 1. 初始状态 (0-2秒)
        # 创建坐标轴
        axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": [-1, 0, 1]},
            y_axis_config={"numbers_to_include": [-1, 0, 1]},
        )
        
        # 创建单位圆
        unit_circle = Circle(
            radius=1,
            color="#4fc3f7",
            fill_opacity=0.3,
            stroke_width=2
        )
        
        # 半径标注
        radius_label = MathTex("r = 1", color=WHITE).next_to(unit_circle, UP, buff=0.2)
        
        # 初始角度θ=0°
        angle = 0
        theta_tracker = ValueTracker(angle)
        
        # 旋转半径
        def get_radius():
            angle = theta_tracker.get_value()
            end_point = np.array([np.cos(angle), np.sin(angle), 0])
            return Line(ORIGIN, end_point, color="#ff5252", stroke_width=4)
        
        radius = always_redraw(get_radius)
        
        # 角度标记弧线
        def get_angle_arc():
            angle = theta_tracker.get_value()
            arc = Arc(
                radius=0.3,
                start_angle=0,
                angle=angle,
                color=WHITE,
                arc_center=ORIGIN
            )
            angle_label = MathTex(r"\theta", color=WHITE).next_to(arc, RIGHT, buff=0.1)
            return VGroup(arc, angle_label)
        
        angle_arc = always_redraw(get_angle_arc)
        
        # 三角函数线
        def get_sin_line():
            angle = theta_tracker.get_value()
            end_point = radius.get_end()
            sin_line = DashedLine(
                end_point,
                np.array([end_point[0], 0, 0]),
                color="#ff80ab",
                stroke_width=3
            )
            return sin_line
        
        def get_cos_line():
            angle = theta_tracker.get_value()
            end_point = radius.get_end()
            cos_line = DashedLine(
                end_point,
                np.array([0, end_point[1], 0]),
                color="#ffd740",
                stroke_width=3
            )
            return cos_line
        
        sin_line = always_redraw(get_sin_line)
        cos_line = always_redraw(get_cos_line)
        
        # 公式显示
        formulas = VGroup(
            MathTex(r"\sin\theta = \frac{y}{r}"),
            MathTex(r"\cos\theta = \frac{x}{r}"),
            MathTex(r"r = 1")
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
        
        # 初始动画
        self.play(Create(axes), run_time=1)
        self.play(Create(unit_circle), Write(radius_label), run_time=1)
        self.wait(0.5)
        
        self.play(Create(radius), Create(angle_arc), run_time=1)
        self.wait(0.5)
        
        self.play(Create(sin_line), Create(cos_line), run_time=1)
        self.play(Write(formulas), run_time=1)
        self.wait(0.5)
        
        # 2. 旋转与投影 (2-10秒)
        self.play(
            theta_tracker.animate.set_value(2*PI),
            run_time=8,
            rate_func=linear
        )
        self.wait(0.5)
        
        # 3. 周期性强调 (10-15秒)
        special_angles = [PI/2, PI, 3*PI/2, 2*PI]
        angle_names = ["90^\\circ", "180^\\circ", "270^\\circ", "360^\\circ"]
        
        for angle, name in zip(special_angles, angle_names):
            self.play(
                theta_tracker.animate.set_value(angle),
                run_time=0.5
            )
            self.wait(0.5)
            
            # 高亮显示
            highlight = Text(f"θ={name}", font_size=24, color=YELLOW).to_edge(DOWN)
            self.play(Write(highlight), run_time=0.5)
            self.wait(0.5)
            self.play(FadeOut(highlight), run_time=0.5)
        
        # 4. 总结显示 (15-20秒)
        # 绘制正弦和余弦曲线轨迹
        sin_curve = ParametricFunction(
            lambda t: np.array([t, np.sin(t), 0]),
            t_range=[0, 2*PI],
            color="#ff80ab",
            stroke_width=3
        ).shift(ORIGIN)
        
        cos_curve = ParametricFunction(
            lambda t: np.array([t, np.cos(t), 0]),
            t_range=[0, 2*PI],
            color="#ffd740",
            stroke_width=3
        ).shift(ORIGIN)
        
        # 调整曲线位置
        sin_curve.apply_function(lambda p: np.array([p[0]/PI-1, p[1], 0]))
        cos_curve.apply_function(lambda p: np.array([p[0]/PI-1, p[1], 0]))
        
        periodic_text = Text("周期性: sin(θ+2π) = sinθ", font_size=24, color=WHITE)
        periodic_text.next_to(formulas, DOWN, aligned_edge=LEFT)
        
        self.play(theta_tracker.animate.set_value(0), run_time=1)
        self.wait(0.5)
        
        self.play(Create(sin_curve), Create(cos_curve), run_time=2)
        self.play(Write(periodic_text), run_time=1)
        self.wait(2)
        
        # 结束
        self.play(FadeOut(Group(*self.mobjects)), run_time=1)