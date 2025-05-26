from manim import *

class ExploreCircle(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1E1E3F"
        
        # 中文标题 "探索圆的动态美：从点到完美形态"
        title = Text("什么是圆？", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(FadeIn(title))
        self.wait(1)

        # 网格背景
        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        self.play(FadeIn(grid))
        
        # 圆心标记
        center_dot = Dot(point=ORIGIN, color=RED)
        self.play(FadeIn(center_dot))
        self.wait(1)

        # 动态生成圆的点
        moving_dot = Dot(point=ORIGIN, color=WHITE)
        radius_tracker = ValueTracker(0)

        # 圆动态生成
        circle = Circle(color=WHITE, radius=0)
        circle.add_updater(lambda m: m.become(Circle(radius=radius_tracker.get_value(), color=WHITE)))

        self.add(circle)
        self.play(radius_tracker.animate.set_value(2), run_time=4, rate_func=smooth)
        self.wait(1)

        # 动态点运动生成轨迹
        def update_dot(dot):
            angle = radius_tracker.get_value() * PI  # 根据半径动态改变点的位置
            dot.move_to([2 * np.cos(angle), 2 * np.sin(angle), 0])

        moving_dot.add_updater(update_dot)
        self.add(moving_dot)

        # 数学公式
        formula = MathTex(r"x^2 + y^2 = r^2", font_size=36, color=WHITE)
        formula.to_edge(DOWN)
        self.play(FadeIn(formula))
        self.wait(2)

        # 径向线条展示对称性
        radial_lines = []
        for angle in np.linspace(0, 2 * PI, 12):
            line = Line(start=ORIGIN, end=[2 * np.cos(angle), 2 * np.sin(angle), 0], color=BLUE)
            radial_lines.append(line)
        
        self.play(*[Create(line) for line in radial_lines], run_time=3)

        # 添加文字说明
        symmetry_text = Text("所有点到圆心的距离相等", font_size=32, color=WHITE)
        symmetry_text.next_to(formula, UP)
        self.play(FadeIn(symmetry_text))
        self.wait(2)

        # 收尾动画
        self.play(FadeOut(Group(*self.mobjects)), run_time=2)
        end_text = Text("这就是圆的定义", font_size=36, color=WHITE)
        self.play(FadeIn(end_text))
        self.wait(2)
        self.play(FadeOut(end_text))