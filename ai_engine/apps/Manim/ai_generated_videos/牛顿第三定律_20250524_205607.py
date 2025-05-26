from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color=BLUE, fill_opacity=1)
        ground = Line(start=LEFT * 6, end=RIGHT * 6, color=GREY)
        ground.shift(DOWN * 3)
        self.add(background, ground)

        # 场景标题
        title = Text("牛顿第三定律：作用力与反作用力", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 小球与墙
        ball = Circle(radius=0.5, color=ORANGE, fill_opacity=0.8).shift(LEFT * 3 + DOWN * 2.5)
        ball_label = Text("球", font_size=24, color=WHITE).next_to(ball, UP)
        wall = Rectangle(width=0.5, height=2, color=DARK_GREY, fill_opacity=0.8).shift(RIGHT * 3 + DOWN * 2)
        wall_label = Text("墙", font_size=24, color=WHITE).next_to(wall, UP)
        self.play(FadeIn(ball), FadeIn(ball_label), FadeIn(wall), FadeIn(wall_label))
        self.wait(1)

        # 小球撞墙动画
        self.play(ball.animate.shift(RIGHT * 6), run_time=3)
        self.wait(0.5)

        # 力箭头展示
        action_arrow = Arrow(start=ball.get_center(), end=wall.get_center(), color=RED, stroke_width=6)
        reaction_arrow = Arrow(start=wall.get_center(), end=ball.get_center(), color=GREEN, stroke_width=6)
        action_label = Text("作用力", font_size=24, color=RED).next_to(action_arrow, UP)
        reaction_label = Text("反作用力", font_size=24, color=GREEN).next_to(reaction_arrow, DOWN)
        self.play(Create(action_arrow), Write(action_label), Create(reaction_arrow), Write(reaction_label))
        self.wait(1)

        # 公式展示
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=48, color=WHITE)
        formula.to_edge(UP)
        self.play(FadeOut(action_arrow, reaction_arrow, action_label, reaction_label), Write(formula))
        self.wait(2)

        # 日常实例：人站在地面上
        person = SVGMobject("person.svg").scale(0.5).shift(DOWN * 1.5)
        ground_force_arrow = Arrow(start=person.get_bottom(), end=person.get_bottom() + UP * 1, color=RED, stroke_width=6)
        person_force_arrow = Arrow(start=person.get_bottom(), end=person.get_bottom() + DOWN * 1, color=GREEN, stroke_width=6)
        ground_force_label = Text("地面对人的力", font_size=24, color=RED).next_to(ground_force_arrow, LEFT)
        person_force_label = Text("人对地面的力", font_size=24, color=GREEN).next_to(person_force_arrow, RIGHT)
        self.play(FadeOut(ball, ball_label, wall, wall_label, formula), FadeIn(person))
        self.play(Create(ground_force_arrow), Write(ground_force_label), Create(person_force_arrow), Write(person_force_label))
        self.wait(2)

        # 字幕展示
        subtitle = Text("你站在地面上，地面也在‘站’着你！", font_size=36, color=WHITE)
        subtitle.to_edge(DOWN)
        self.play(Write(subtitle))
        self.wait(2)

        # 总结
        self.play(FadeOut(person, ground_force_arrow, person_force_arrow, ground_force_label, person_force_label, subtitle))
        final_formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=48, color=WHITE)
        final_formula.move_to(ORIGIN)
        final_text = Text("作用力与反作用力是自然界的平衡法则。", font_size=36, color=WHITE)
        final_text.next_to(final_formula, DOWN)
        self.play(Write(final_formula), Write(final_text))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))