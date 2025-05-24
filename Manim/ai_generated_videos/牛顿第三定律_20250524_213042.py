from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLUE_D, fill_opacity=1)
        grid = NumberPlane(x_range=(-7, 7, 1), y_range=(-4, 4, 1), background_line_style={"stroke_color": WHITE, "stroke_opacity": 0.3})
        self.add(background, grid)

        # 场景标题
        title = Text("力的对话：展示牛顿第三定律", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 两个球体
        red_ball = Circle(radius=0.5, color=RED, fill_opacity=0.8).move_to(LEFT*3)
        blue_ball = Circle(radius=0.5, color=BLUE, fill_opacity=0.8).move_to(RIGHT*3)
        label_A = Text("物体 A", font_size=24, color=WHITE).next_to(red_ball, UP)
        label_B = Text("物体 B", font_size=24, color=WHITE).next_to(blue_ball, UP)
        
        self.play(FadeIn(red_ball), FadeIn(blue_ball), FadeIn(label_A), FadeIn(label_B))
        self.wait(1)

        # 力箭头和标注
        force_A_to_B = Arrow(start=red_ball.get_center(), end=blue_ball.get_center(), color=RED, buff=0.5, stroke_width=4)
        force_B_to_A = Arrow(start=blue_ball.get_center(), end=red_ball.get_center(), color=BLUE, buff=0.5, stroke_width=4)
        label_force_A_to_B = MathTex(r"F_{A \to B}", color=RED).next_to(force_A_to_B, UP, buff=0.3)
        label_force_B_to_A = MathTex(r"F_{B \to A}", color=BLUE).next_to(force_B_to_A, DOWN, buff=0.3)

        self.play(Create(force_A_to_B), Write(label_force_A_to_B))
        self.wait(1)
        self.play(Create(force_B_to_A), Write(label_force_B_to_A))
        self.wait(1)

        # 展示公式
        formula = MathTex(r"F_{A \to B} = -F_{B \to A}", font_size=48, color=YELLOW)
        formula.scale(1.2)
        formula.to_edge(DOWN)
        self.play(Write(formula), formula.animate.scale(1.1).set_color(GOLD))
        self.wait(2)

        # 动态演示
        red_ball_target = red_ball.get_center() + LEFT * 1.5
        blue_ball_target = blue_ball.get_center() + RIGHT * 1.5
        
        self.play(
            red_ball.animate.shift(LEFT*1.5),
            blue_ball.animate.shift(RIGHT*1.5),
            force_A_to_B.animate.shift(LEFT*1.5),
            force_B_to_A.animate.shift(RIGHT*1.5),
            label_force_A_to_B.animate.shift(LEFT*1.5),
            label_force_B_to_A.animate.shift(RIGHT*1.5),
            run_time=2
        )
        self.wait(1)
        
        self.play(
            red_ball.animate.shift(RIGHT*1.5),
            blue_ball.animate.shift(LEFT*1.5),
            force_A_to_B.animate.shift(RIGHT*1.5),
            force_B_to_A.animate.shift(LEFT*1.5),
            label_force_A_to_B.animate.shift(RIGHT*1.5),
            label_force_B_to_A.animate.shift(LEFT*1.5),
            run_time=2
        )
        self.wait(1)

        # 结束场景
        end_text = Text("牛顿第三定律：作用力与反作用力永远成对出现", font_size=32, color=WHITE).to_edge(DOWN)
        self.play(FadeOut(red_ball, blue_ball, force_A_to_B, force_B_to_A, label_A, label_B, label_force_A_to_B, label_force_B_to_A), Write(end_text))
        self.wait(2)