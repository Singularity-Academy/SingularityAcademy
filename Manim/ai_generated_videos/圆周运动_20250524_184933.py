from manim import *
import random

class CircularMotionScene(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#001F3F"

        # 添加背景星点
        stars = VGroup(*[Dot(color=WHITE).move_to(
            [random.uniform(-7, 7), random.uniform(-4, 4), 0]) for _ in range(50)])
        self.add(stars)
        
        # 星点闪烁动画
        for star in stars:
            self.play(star.animate.set_opacity(random.uniform(0.3, 1)), run_time=0.1)

        # 场景标题
        title = Text("探索圆周运动：从圆到速度矢量", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 显示圆周和圆心
        circle = Circle(radius=2, color=WHITE)
        center_dot = Dot(point=ORIGIN, color=BLUE)
        center_label = Text("圆心", font_size=24, color=BLUE).next_to(center_dot, DOWN)
        self.play(Create(circle), FadeIn(center_dot), Write(center_label))
        self.wait(1)

        # 坐标轴
        x_axis = Line(start=LEFT * 4, end=RIGHT * 4, color=GRAY)
        y_axis = Line(start=DOWN * 3, end=UP * 3, color=GRAY)
        self.play(Create(x_axis), Create(y_axis))
        self.wait(1)

        # 圆周运动的小球
        ball = Dot(color=YELLOW).move_to(circle.point_at_angle(0))
        self.play(FadeIn(ball))
        self.wait(1)

        # 速度矢量箭头
        velocity_arrow = Arrow(start=ball.get_center(),
                               end=ball.get_center() + RIGHT,
                               color=RED,
                               buff=0)
        self.play(FadeIn(velocity_arrow))
        self.wait(1)

        # 圆周运动动画和速度矢量方向变化
        def update_arrow(arrow):
            ball_position = ball.get_center()
            direction = ball_position / np.linalg.norm(ball_position)
            arrow.put_start_and_end_on(ball_position, ball_position + np.array([-direction[1], direction[0], 0]))

        velocity_arrow.add_updater(update_arrow)
        self.add(velocity_arrow)
        self.play(MoveAlongPath(ball, circle, rate_func=linear, run_time=10))
        self.wait(1)

        # 显示角速度公式
        omega_formula = MathTex(r"\omega = \frac{\Delta \theta}{\Delta t}",
                                font_size=36, color=WHITE)
        omega_formula.to_edge(LEFT).shift(UP * 1.5)
        self.play(Write(omega_formula))
        self.wait(1)

        # 显示线速度公式
        velocity_formula = MathTex(r"v = r\omega", font_size=36, color=WHITE)
        velocity_formula.next_to(omega_formula, DOWN, buff=0.8)
        self.play(Write(velocity_formula))
        self.wait(1)

        # 圆周高亮闪烁
        self.play(circle.animate.set_color(YELLOW), run_time=0.5)
        self.play(circle.animate.set_color(WHITE), run_time=0.5)
        self.wait(1)

        # 总结文字
        summary_text = Text("圆周运动的基本原理", font_size=36, color=WHITE)
        self.play(FadeOut(title), FadeOut(omega_formula), FadeOut(velocity_formula))
        self.play(Write(summary_text))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)))