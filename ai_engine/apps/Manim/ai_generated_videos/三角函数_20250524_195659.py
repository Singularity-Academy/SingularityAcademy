from manim import *

class ExploreTrigFunctions(Scene):
    def construct(self):
        # 场景标题
        title = Text("探索三角函数：从单位圆到波动的世界", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 设置背景颜色为浅蓝色
        self.camera.background_color = "#87CEEB"

        # 创建单位圆及坐标轴
        unit_circle = Circle(radius=1, color=WHITE)
        unit_circle.shift(LEFT * 3)  # 移动到画面左侧
        self.play(Create(unit_circle))

        # 左侧单位圆的坐标轴
        axes_circle = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=3,
            y_length=3,
            axis_config={"color": WHITE},
        ).shift(LEFT * 3)
        self.play(Create(axes_circle))

        # 右侧正弦函数的坐标轴
        axes_function = Axes(
            x_range=[0, 7, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"color": WHITE},
            tips=False,
        ).shift(RIGHT * 3)
        axes_function_labels = axes_function.get_axis_labels(
            x_label=Text("时间", font_size=24, color=WHITE),
            y_label=Text("正弦值", font_size=24, color=WHITE),
        )
        self.play(Create(axes_function), Write(axes_function_labels))
        self.wait(1)

        # 标注数学公式
        formula = MathTex(r"\sin(\theta) = \text{y-coordinate of the point on the unit circle}")
        formula.scale(0.8).next_to(axes_function, DOWN)
        self.play(Write(formula))
        self.wait(1)

        # 动态展示单位圆上的向量和点
        radius_line = Line(ORIGIN, unit_circle.point_at_angle(0), color=YELLOW)
        dot_circle = Dot(unit_circle.point_at_angle(0), color=RED)
        angle_label = MathTex(r"\theta = 0").next_to(unit_circle, UP)

        self.play(Create(radius_line), FadeIn(dot_circle), Write(angle_label))

        def update_radius_line(mob):
            angle = mob.angle
            new_end = unit_circle.point_at_angle(angle)
            mob.become(Line(ORIGIN, new_end, color=YELLOW))

        def update_dot_circle(mob):
            angle = mob.angle
            mob.move_to(unit_circle.point_at_angle(angle))

        def update_angle_label(mob):
            angle = mob.angle
            mob.become(
                MathTex(rf"\theta = {angle:.2f}").next_to(unit_circle, UP)
            )

        # 动态生成正弦函数曲线
        sine_curve = axes_function.plot(lambda x: np.sin(x), color=RED)
        sine_curve.set_stroke(width=2)

        sine_dot = Dot(axes_function.coords_to_point(0, 0), color=RED)

        def update_sine_dot(mob):
            angle = mob.angle
            mob.move_to(axes_function.coords_to_point(angle, np.sin(angle)))

        # 动画
        def update_objects(obj_group, dt):
            obj_group.angle += dt * 2  # 增加角度
            for obj in obj_group.objects:
                obj.angle = obj_group.angle
                obj.update(obj)

        animated_group = AnimationGroup(
            radius_line,
            dot_circle,
            sine_dot,
            angle_label,
            update_func=update_objects,
        )

        self.play(
            animated_group,
            Create(sine_curve),
            run_time=8,
        )