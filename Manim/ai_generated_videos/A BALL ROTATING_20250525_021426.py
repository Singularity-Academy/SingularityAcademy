from manim import *
import numpy as np

class RotatingBallWithAngularVelocity(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#001a33"  # 深蓝色背景
        stars = VGroup(*[
            Dot(point=np.random.uniform(-7, 7, 3), color=WHITE).scale(0.1)
            for _ in range(150)
        ])
        self.add(stars)
        
        # 标题
        title = Text("旋转的球与角速度的奥秘", font_size=32, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 球体设置
        sphere = Sphere(radius=2, color=WHITE)
        sphere.set_fill(BLUE_E, opacity=0.6)
        sphere.set_gloss(0.9)  # 光滑纹理
        sphere_mesh = VGroup(*[
            Circle(radius=2, color=WHITE).rotate(angle, axis=RIGHT)
            for angle in np.linspace(0, PI, 8)
        ])
        sphere_mesh.add(*[
            Circle(radius=2, color=WHITE).rotate(angle, axis=UP)
            for angle in np.linspace(0, PI, 8)
        ])
        sphere.add(sphere_mesh)
        sphere.move_to(ORIGIN)
        self.play(FadeIn(sphere), run_time=2)
        
        # 旋转轴
        rotation_axis = Arrow(start=ORIGIN, end=UP * 3, color=WHITE, buff=0)
        rotation_axis_label = Text("旋转轴", font_size=24, color=WHITE).next_to(rotation_axis, UP)
        self.play(Create(rotation_axis), Write(rotation_axis_label))
        self.wait(1)
        
        # 角速度矢量
        angular_velocity_vector = Arrow(start=ORIGIN, end=UP * 2.5, color=RED, buff=0)
        angular_velocity_label = Text("角速度", font_size=24, color=RED).next_to(angular_velocity_vector, UP)
        self.play(Create(angular_velocity_vector), Write(angular_velocity_label))
        self.wait(1)
        
        # 角速度公式
        formula = MathTex(r"\vec{\omega} = \frac{\Delta \theta}{\Delta t}", font_size=36, color=YELLOW)
        formula.to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1)
        
        # 球旋转动画
        rotation_time = 6
        time_label = Text(f"时间: 0.00 s", font_size=24, color=WHITE).to_corner(UL)
        self.add(time_label)
        
        def update_time_label(mob, dt):
            mob.text = f"时间: {self.time_tracker.get_value():.2f} s"

        self.time_tracker = ValueTracker(0)
        time_label.add_updater(update_time_label)
        
        self.play(
            sphere.animate.rotate(2 * PI, axis=UP),
            angular_velocity_vector.animate.rotate_about_origin(2 * PI, axis=UP),
            self.time_tracker.animate.set_value(rotation_time),
            run_time=rotation_time,
            rate_func=linear
        )
        self.wait(1)
        
        # 停止后总结
        summary_text = Text("角速度方向与大小的影响", font_size=28, color=WHITE)
        summary_text.to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(2)
        
        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))