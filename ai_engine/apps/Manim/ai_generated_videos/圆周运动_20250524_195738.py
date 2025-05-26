from manim import *

class CircularMotionScene(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#001f3f"  # 深蓝色背景

        # 场景标题
        title = Text("探索圆周运动：从位置到速度的动态之美", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 绘制圆形路径
        circle = Circle(radius=3, color=WHITE)
        circle_label = Text("圆形路径", font_size=24, color=WHITE)
        circle_label.next_to(circle, DOWN)
        self.play(Create(circle), Write(circle_label))
        self.wait(1)

        # 标注圆心
        center_dot = Dot(point=ORIGIN, color=WHITE)
        center_label = Text("圆心", font_size=24, color=WHITE)
        center_label.next_to(center_dot, LEFT)
        self.play(FadeIn(center_dot), Write(center_label))
        self.wait(1)

        # 红色点作为运动物体
        moving_dot = Dot(radius=0.15, color=RED)
        moving_dot.move_to(circle.point_at_angle(0))  # 初始位置在圆周右侧
        self.play(FadeIn(moving_dot))
        self.wait(0.5)

        # 位置向量（绿色箭头）
        position_vector = Arrow(start=ORIGIN, end=moving_dot.get_center(), color=GREEN, buff=0)
        self.play(GrowArrow(position_vector))
        self.wait(0.5)

        # 速度向量（蓝色箭头）
        velocity_vector = Arrow(start=moving_dot.get_center(), 
                                end=moving_dot.get_center() + RIGHT, 
                                color=BLUE, buff=0)
        self.play(GrowArrow(velocity_vector))
        self.wait(0.5)

        # 标注公式
        omega_formula = MathTex(r"\omega = \frac{d\theta}{dt}", font_size=36, color=YELLOW)
        omega_formula.to_edge(UP)
        self.play(Write(omega_formula))
        self.wait(1)

        # 时间计时器
        timer_text = Text("时间: 0.0 秒", font_size=24, color=WHITE)
        timer_text.to_corner(DR)
        self.play(FadeIn(timer_text))
        self.wait(0.5)

        # 更新函数
        def update_position_vector(vector):
            vector.put_start_and_end_on(ORIGIN, moving_dot.get_center())

        def update_velocity_vector(vector):
            position = moving_dot.get_center()
            tangent_direction = np.array([-position[1], position[0], 0])  # 垂直于位置向量
            tangent_direction /= np.linalg.norm(tangent_direction)  # 单位化
            vector.put_start_and_end_on(position, position + tangent_direction)

        def update_timer_text(text, dt):
            text.set_text(f"时间: {round(dt, 1)} 秒")

        # 动画运动
        angle_tracker = ValueTracker(0)
        timer_tracker = ValueTracker(0)

        moving_dot.add_updater(lambda dot: dot.move_to(circle.point_at_angle(angle_tracker.get_value())))
        position_vector.add_updater(update_position_vector)
        velocity_vector.add_updater(update_velocity_vector)
        timer_text.add_updater(lambda text: update_timer_text(text, timer_tracker.get_value()))

        self.play(
            angle_tracker.animate.increment_value(2 * PI),  # 顺时针运动一圈
            timer_tracker.animate.set_value(10),  # 时间计时器到10秒
            run_time=10, rate_func=linear
        )

        # 停止所有更新器
        moving_dot.clear_updaters()
        position_vector.clear_updaters()
        velocity_vector.clear_updaters()
        timer_text.clear_updaters()
        self.wait(0.5)

        # 总结文字
        summary_text = Text("位置、速度与角速度：圆周运动背后的动态关系", font_size=28, color=YELLOW)
        summary_text.to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)))