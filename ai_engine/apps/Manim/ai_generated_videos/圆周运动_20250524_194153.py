from manim import *

class CircularMotionScene(Scene):
    def construct(self):
        # 设置背景色
        self.camera.background_color = "#001f3f"  # 深蓝色背景

        # 圆形轨迹
        radius = 3
        circle = Circle(radius=radius, color=GREEN, stroke_width=4)
        self.play(Create(circle), run_time=2)

        # 红色小球
        ball = Dot(color=RED, radius=0.15)
        ball.move_to(circle.point_from_proportion(0))  # 初始位置
        self.add(ball)

        # 速度箭头
        velocity_arrow = Arrow(
            ball.get_center(),
            ball.get_center() + RIGHT,
            color=YELLOW,
            buff=0.1,
            max_tip_length_to_length_ratio=0.3,
        )
        self.add(velocity_arrow)

        # 加速度箭头
        acceleration_arrow = Arrow(
            ball.get_center(),
            ball.get_center() + LEFT,
            color=PURPLE,
            buff=0.1,
            max_tip_length_to_length_ratio=0.3,
        )
        self.add(acceleration_arrow)

        # 数学公式
        velocity_formula = MathTex(r"v = r\omega", font_size=36, color=WHITE)
        acceleration_formula = MathTex(r"a_c = \frac{v^2}{r}", font_size=36, color=WHITE)
        velocity_formula.to_edge(UP, buff=1)
        acceleration_formula.next_to(velocity_formula, DOWN, buff=0.5)
        self.play(Write(velocity_formula), Write(acceleration_formula))
        self.wait(2)

        # 动态标注
        velocity_label = Text("切向速度", font_size=24, color=YELLOW)
        acceleration_label = Text("向心加速度", font_size=24, color=PURPLE)
        velocity_label.next_to(velocity_arrow, RIGHT, buff=0.5)
        acceleration_label.next_to(acceleration_arrow, DOWN, buff=0.5)
        self.play(FadeIn(velocity_label), FadeIn(acceleration_label))

        # 动画：红色小球沿圆周运动
        def update_ball_and_arrows(mob, dt):
            mob.angle += dt  # 更新角度
            angle = mob.angle
            mob.move_to(circle.point_from_proportion(angle % 1))
            
            # 更新速度箭头
            tangent_vector = circle.tangent_vector(angle % 1)
            velocity_arrow.put_start_and_end_on(
                mob.get_center(),
                mob.get_center() + tangent_vector * 1.5,
            )

            # 更新加速度箭头
            acceleration_arrow.put_start_and_end_on(
                mob.get_center(),
                mob.get_center() - mob.get_center() / radius * 1.5,
            )

        ball.angle = 0  # 初始角度
        ball.add_updater(update_ball_and_arrows)
        self.play(
            Rotate(ball, about_point=ORIGIN, angle=-TAU, rate_func=linear, run_time=8)
        )
        ball.remove_updater(update_ball_and_arrows)

        # 终止场景
        summary_text = Text(
            "圆周运动的关键：速度方向动态变化，加速度始终指向圆心",
            font_size=28,
            color=WHITE,
        )
        summary_text.to_edge(DOWN, buff=1)
        self.play(FadeOut(velocity_arrow), FadeOut(acceleration_arrow))
        self.play(Write(summary_text))
        self.wait(3)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)))