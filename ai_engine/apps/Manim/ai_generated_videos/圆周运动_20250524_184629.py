from manim import *

class CircularMotionScene(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = DARK_BLUE

        # 场景标题
        title = Text("揭开圆周运动的奥秘：速度、加速度与向心力", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 星星背景元素
        stars = VGroup(
            *[
                Dot(color=WHITE).move_to(
                    [random.uniform(-6, 6), random.uniform(-3, 3), 0]
                )
                for _ in range(50)
            ]
        )
        self.add(stars)

        # 圆周轨迹
        circle = Circle(radius=3, color=WHITE)
        self.play(Create(circle), run_time=2)
        self.wait(1)

        # 圆的中心点
        center_dot = Dot(color=WHITE)
        center_label = Text("圆的中心", font_size=24, color=WHITE)
        center_label.next_to(center_dot, DOWN)
        self.play(FadeIn(center_dot), Write(center_label))
        self.wait(1)

        # 运动物体：红色小球
        ball = Dot(color=RED).move_to(circle.point_at_angle(0))
        self.play(FadeIn(ball))
        self.wait(1)

        # 物体沿圆形轨迹运动
        motion_text = Text("物体沿圆形轨迹运动", font_size=24, color=WHITE)
        motion_text.to_edge(DOWN)
        self.play(Write(motion_text))
        self.wait(1)

        # 切线速度向量：黄色箭头
        velocity_arrow = Arrow(
            start=ball.get_center(),
            end=ball.get_center() + RIGHT,
            color=YELLOW,
            buff=0,
        )
        velocity_label = MathTex(r"v", color=YELLOW)
        velocity_label.next_to(velocity_arrow, UP)
        self.play(FadeIn(velocity_arrow), Write(velocity_label))
        self.wait(1)

        # 向心加速度向量：绿色箭头
        acceleration_arrow = Arrow(
            start=ball.get_center(),
            end=center_dot.get_center(),
            color=GREEN,
            buff=0,
        )
        acceleration_label = Text("向心加速度", font_size=24, color=GREEN)
        acceleration_label.next_to(acceleration_arrow, LEFT)
        self.play(FadeIn(acceleration_arrow), Write(acceleration_label))
        self.wait(1)

        # 向心力向量：紫色箭头
        force_arrow = Arrow(
            start=ball.get_center(),
            end=center_dot.get_center(),
            color=PURPLE,
            buff=0,
        )
        force_label = MathTex(r"F = m \cdot \frac{v^2}{r}", color=PURPLE)
        force_label.to_edge(DOWN)
        self.play(FadeIn(force_arrow), Write(force_label))
        self.wait(1)

        # 动态展示小球运动及向量变化
        def update_ball_and_vectors(mob, dt):
            current_angle = dt * 2 * PI / 4  # 匀速运动
            mob.move_to(circle.point_at_angle(current_angle))

            # 更新切线速度向量
            velocity_arrow.put_start_and_end_on(
                mob.get_center(),
                mob.get_center()
                + normalize(np.cross([0, 0, 1], mob.get_center() - center_dot.get_center())),
            )

            # 更新向心加速度向量
            acceleration_arrow.put_start_and_end_on(
                mob.get_center(),
                center_dot.get_center(),
            )

            # 更新向心力向量
            force_arrow.put_start_and_end_on(
                mob.get_center(),
                center_dot.get_center(),
            )

        ball.add_updater(update_ball_and_vectors)
        self.wait(8)  # 动画时长

        # 总结文字
        summary_text = Text(
            "圆周运动的核心：切线速度、向心加速度和向心力",
            font_size=28,
            color=WHITE,
        )
        summary_text.to_edge(DOWN)
        self.play(Transform(motion_text, summary_text))
        self.wait(3)

        # 结束
        self.play(FadeOut(Group(*self.mobjects)))