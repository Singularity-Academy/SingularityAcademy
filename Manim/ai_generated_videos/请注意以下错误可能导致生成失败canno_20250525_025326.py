from manim import *
import numpy as np

class NewtonThirdLawDemo(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#1A1A40"
        ground_line = Line(
            start=LEFT*FRAME_WIDTH/2, 
            end=RIGHT*FRAME_WIDTH/2, 
            color=WHITE, 
            stroke_width=2
        ).move_to(DOWN*2)
        grid = NumberPlane(
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        self.add(grid, ground_line)

        # 牛顿第三定律公式
        formula = MathTex(
            r"\vec{F}_{\text{action}} = -\vec{F}_{\text{reaction}}", 
            font_size=48, 
            color=WHITE
        ).to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 两个球体
        red_ball = Dot(color=RED, radius=0.3).move_to(LEFT*3)
        blue_ball = Dot(color=BLUE, radius=0.3).move_to(RIGHT*3)
        self.play(FadeIn(red_ball), FadeIn(blue_ball))
        self.wait(1)

        # 动画：球体移动靠近
        self.play(
            red_ball.animate.shift(RIGHT*3),
            blue_ball.animate.shift(LEFT*3),
            run_time=2
        )

        # 作用力和反作用力箭头
        action_arrow = Arrow(
            start=red_ball.get_center(), 
            end=blue_ball.get_center(), 
            color=RED, 
            buff=0.2, 
            stroke_width=3
        )
        reaction_arrow = Arrow(
            start=blue_ball.get_center(), 
            end=red_ball.get_center(), 
            color=BLUE, 
            buff=0.2, 
            stroke_width=3
        )
        self.play(Create(action_arrow))
        self.wait(0.5)
        self.play(Create(reaction_arrow))
        self.wait(1)

        # 闪烁公式中的负号
        negative_sign = formula[7]
        self.play(negative_sign.animate.set_color(YELLOW), run_time=0.5)
        self.play(negative_sign.animate.set_color(WHITE), run_time=0.5)
        self.wait(1)

        # 球体反弹
        self.play(
            red_ball.animate.shift(LEFT*3),
            blue_ball.animate.shift(RIGHT*3),
            run_time=2
        )
        self.play(FadeOut(action_arrow), FadeOut(reaction_arrow))

        # 总结文字
        conclusion = Text(
            "作用力与反作用力大小相等，方向相反", 
            font_size=32, 
            color=WHITE
        ).move_to(DOWN*1.5)
        self.play(Write(conclusion))
        self.wait(2)

        # 场景结束
        self.play(FadeOut(VGroup(*self.mobjects)))