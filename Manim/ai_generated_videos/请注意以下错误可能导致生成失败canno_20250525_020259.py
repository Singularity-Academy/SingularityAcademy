from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            fill_color=BLUE_E,
            fill_opacity=1
        )
        background.set_z_index(-1)
        self.add(background)

        ground = Rectangle(width=FRAME_WIDTH, height=0.2, color=GRAY, fill_opacity=1)
        ground.move_to(DOWN * 3.5)
        self.add(ground)

        # 标题
        title = Text("牛顿第三定律", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建两个球体
        red_ball = Circle(radius=0.5, color=RED, fill_color=RED, fill_opacity=1)
        blue_ball = Circle(radius=0.5, color=BLUE, fill_color=BLUE, fill_opacity=1)
        red_ball.move_to(LEFT * 2)
        blue_ball.move_to(RIGHT * 2)

        self.play(FadeIn(red_ball), FadeIn(blue_ball))
        self.wait(1)

        # 球体碰撞
        self.play(red_ball.animate.shift(RIGHT * 4), run_time=2)
        self.wait(0.5)

        # 力箭头
        action_arrow = Arrow(
            start=red_ball.get_center(),
            end=blue_ball.get_center(),
            color=RED,
            buff=0.1
        )
        reaction_arrow = Arrow(
            start=blue_ball.get_center(),
            end=red_ball.get_center(),
            color=BLUE,
            buff=0.1
        )

        action_label = Text("作用力", font_size=24, color=RED)
        reaction_label = Text("反作用力", font_size=24, color=BLUE)
        action_label.next_to(action_arrow, UP, buff=0.2)
        reaction_label.next_to(reaction_arrow, UP, buff=0.2)

        self.play(Create(action_arrow), Write(action_label))
        self.play(Create(reaction_arrow), Write(reaction_label))
        self.wait(1)

        # 力的公式展示
        force_formula = MathTex(r"F_{1} = -F_{2}", font_size=48, color=WHITE)
        force_formula.to_edge(DOWN)
        self.play(Write(force_formula))
        self.wait()

        # 解释文字
        explanation = Text(
            "作用力和反作用力大小相等，方向相反，总是成对出现。",
            font_size=28,
            color=WHITE
        )
        explanation.to_edge(UP)
        self.play(Write(explanation))
        self.wait(2)

        # 生活场景拓展
        self.play(FadeOut(VGroup(red_ball, blue_ball, action_arrow, reaction_arrow, action_label, reaction_label, force_formula)))

        person = Rectangle(width=0.5, height=1, color=WHITE, fill_color=WHITE, fill_opacity=1)
        ground_force_arrow = Arrow(start=DOWN * 3, end=DOWN * 2.5, color=BLUE)
        person_force_arrow = Arrow(start=DOWN * 2.5, end=DOWN * 3, color=RED)

        ground_force_label = Text("地面对脚的力", font_size=24, color=BLUE)
        person_force_label = Text("脚对地的力", font_size=24, color=RED)

        person.move_to(DOWN * 2)
        ground_force_label.next_to(ground_force_arrow, LEFT, buff=0.2)
        person_force_label.next_to(person_force_arrow, RIGHT, buff=0.2)

        self.play(FadeIn(person))
        self.play(Create(ground_force_arrow), Write(ground_force_label))
        self.play(Create(person_force_arrow), Write(person_force_label))
        self.wait(2)

        # 结束
        self.play(FadeOut(VGroup(*self.mobjects)))