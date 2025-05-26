from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 设置背景和标题
        grid = NumberPlane(x_range=[-8, 8, 1], y_range=[-4, 4, 1], background_line_style={"stroke_color": LIGHT_GRAY})
        self.add(grid)
        
        ground = Line(start=LEFT*8, end=RIGHT*8, color=WHITE)
        ground.shift(DOWN*2.5)
        self.add(ground)
        
        formula = MathTex(r"F_1 = -F_2", font_size=48, color=WHITE)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(1)
        
        # 创建物体和弹簧
        cube_a = Square(side_length=1, color=BLUE, fill_opacity=1)
        cube_b = Square(side_length=1, color=RED, fill_opacity=1)
        cube_a.move_to(LEFT*2 + DOWN*2)
        cube_b.move_to(RIGHT*2 + DOWN*2)
        
        spring = Line(start=cube_a.get_right(), end=cube_b.get_left(), color=GRAY)
        self.add(cube_a, cube_b, spring)
        
        # 静止状态展示
        self.wait(1)
        
        # 施加力
        force_a = Arrow(start=LEFT*3, end=LEFT*1, color=GREEN)
        force_a.next_to(cube_a, LEFT)
        self.play(Create(force_a))
        
        cube_a_target = cube_a.copy().shift(RIGHT*2)
        spring_stretch = Line(start=cube_a_target.get_right(), end=cube_b.get_left(), color=GRAY)
        
        force_b = Arrow(start=RIGHT*3, end=RIGHT*1, color=ORANGE)
        force_b.next_to(cube_b, RIGHT)
        
        self.play(
            cube_a.animate.shift(RIGHT*2),
            cube_b.animate.shift(LEFT*2),
            Transform(spring, spring_stretch),
            Create(force_b),
            run_time=2
        )
        
        # 速度变化展示
        velocity_a = Arrow(start=cube_a.get_center(), end=cube_a.get_center() + RIGHT, color=BLUE)
        velocity_b = Arrow(start=cube_b.get_center(), end=cube_b.get_center() + LEFT, color=RED)
        
        velocity_text_a = Text("速度增加", font_size=24, color=BLUE)
        velocity_text_b = Text("速度减少", font_size=24, color=RED)
        velocity_text_a.next_to(velocity_a, UP)
        velocity_text_b.next_to(velocity_b, UP)
        
        self.play(Create(velocity_a), Create(velocity_b), Write(velocity_text_a), Write(velocity_text_b))
        self.wait(2)
        
        # 力的平衡展示
        balanced_spring = Line(start=cube_a.get_right(), end=cube_b.get_left(), color=GRAY)
        self.play(
            cube_a.animate.shift(LEFT),
            cube_b.animate.shift(RIGHT),
            Transform(spring, balanced_spring),
            FadeOut(force_a),
            FadeOut(force_b),
            FadeOut(velocity_a),
            FadeOut(velocity_b),
            FadeOut(velocity_text_a),
            FadeOut(velocity_text_b),
            run_time=2
        )
        
        # 结尾总结
        self.play(formula.animate.set_color(YELLOW).scale(1.2))
        self.wait(1)
        self.play(FadeOut(VGroup(*self.mobjects)))