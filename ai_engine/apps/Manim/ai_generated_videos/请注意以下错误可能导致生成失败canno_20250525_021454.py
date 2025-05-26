from manim import *
import numpy as np

class RotatingBall(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#001f3f"  # 深蓝色背景

        # 标题
        title = Text("圆周运动与角速度", font_size=36, color=WHITE)
        title.to_corner(UP + LEFT)
        self.play(FadeIn(title))

        # 圆轨迹
        circle = Circle(radius=3, color=BLUE_E, stroke_width=2).shift(DOWN)
        self.play(Create(circle))

        # 小球
        ball = Dot(color=RED).move_to(circle.point_at_angle(0))
        self.play(FadeIn(ball))

        # 半径线
        radius_line = Line(circle.get_center(), ball.get_center(), color=GREEN)
        self.play(Create(radius_line))

        # 速度箭头
        velocity_arrow = Arrow(ball.get_center(), ball.get_center() + RIGHT, color=ORANGE, buff=0.1)
        self.play(Create(velocity_arrow))

        # 公式
        formula = MathTex(r"v = \omega r", font_size=36, color=WHITE)
        formula.to_corner(UP + RIGHT)
        self.play(Write(formula))

        # 动态更新球和向量
        def update_ball_and_vectors(mob, dt):
            angle = dt * 2  # 控制角速度
            mob.rotate(angle, about_point=circle.get_center())
            radius_line.put_start_and_end_on(circle.get_center(), mob.get_center())
            velocity_direction = mob.get_center() - circle.get_center()
            velocity_direction = np.array([-velocity_direction[1], velocity_direction[0], 0])  # 90度旋转方向
            velocity_arrow.put_start_and_end_on(
                mob.get_center(), mob.get_center() + 0.5 * velocity_direction / np.linalg.norm(velocity_direction)
            )

        ball.add_updater(update_ball_and_vectors)

        # 让球旋转一段时间
        self.wait(8)

        # 淡出所有元素
        self.play(FadeOut(VGroup(title, circle, ball, radius_line, velocity_arrow, formula)))
        self.wait(1)