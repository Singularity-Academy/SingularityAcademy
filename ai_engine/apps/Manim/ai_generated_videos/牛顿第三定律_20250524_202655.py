from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=14, height=8, color=BLUE, fill_opacity=1).set_gradient(start_color=BLUE, end_color=WHITE, direction=UP)
        grid = NumberPlane(x_range=[-7, 7], y_range=[-4, 4], background_line_style={"stroke_color": WHITE, "stroke_opacity": 0.2})
        platform = Rectangle(width=12, height=0.5, color=GREY, fill_opacity=1).shift(DOWN * 2.5)
        
        self.add(background, grid, platform)
        
        # 标题
        title = Text("牛顿第三定律", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(FadeIn(title))
        self.wait(1)
        
        # 主要对象
        red_ball = Circle(radius=0.5, color=RED, fill_opacity=1).shift(LEFT * 2 + DOWN * 2)
        blue_ball = Circle(radius=0.5, color=BLUE, fill_opacity=1).shift(RIGHT * 2 + DOWN * 2)
        
        self.play(FadeIn(red_ball), FadeIn(blue_ball))
        
        # 初始力的箭头
        action_arrow = Arrow(start=red_ball.get_center(), end=blue_ball.get_center(), color=RED, buff=0.5)
        reaction_arrow = Arrow(start=blue_ball.get_center(), end=red_ball.get_center(), color=BLUE, buff=0.5)
        
        self.play(Create(action_arrow))
        self.wait(0.5)
        self.play(Create(reaction_arrow))
        self.wait(1)
        
        # 动态演示
        def update_action_arrow(arrow):
            arrow.become(Arrow(start=red_ball.get_center(), end=blue_ball.get_center(), color=RED, buff=0.5))
        
        def update_reaction_arrow(arrow):
            arrow.become(Arrow(start=blue_ball.get_center(), end=red_ball.get_center(), color=BLUE, buff=0.5))
        
        action_arrow.add_updater(update_action_arrow)
        reaction_arrow.add_updater(update_reaction_arrow)
        
        self.play(
            red_ball.animate.shift(LEFT * 1),
            blue_ball.animate.shift(RIGHT * 1),
            run_time=2,
            rate_func=smooth
        )
        
        self.play(
            red_ball.animate.shift(RIGHT * 2),
            blue_ball.animate.shift(LEFT * 2),
            run_time=2,
            rate_func=smooth
        )
        
        action_arrow.remove_updater(update_action_arrow)
        reaction_arrow.remove_updater(update_reaction_arrow)
        
        self.wait(1)
        
        # 公式展示
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=36, color=WHITE)
        formula.shift(DOWN * 3)
        
        self.play(Write(formula))
        self.wait(2)
        
        # 总结
        summary_text = Text("每个力都有一个大小相等、方向相反的伙伴", font_size=28, color=WHITE)
        summary_text.move_to(ORIGIN)
        
        self.play(FadeOut(title), FadeOut(VGroup(red_ball, blue_ball, action_arrow, reaction_arrow, formula)))
        self.play(FadeIn(summary_text))
        self.wait(2)
        
        # 结束
        self.play(FadeOut(summary_text))