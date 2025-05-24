from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#ADD8E6"  # 浅蓝色背景
        
        # 标题
        title = Text("牛顿第三定律", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 地面和墙
        ground = Line(start=LEFT * 6, end=RIGHT * 6, color=GREY).shift(DOWN * 2)
        wall = Rectangle(height=3, width=0.5, color=GREY, fill_opacity=1).next_to(ground, UP, buff=0).shift(RIGHT * 4)
        self.play(Create(ground), Create(wall))
        self.wait(1)
        
        # 球和初始力箭头
        ball = Circle(radius=0.5, color=RED, fill_opacity=0.8).shift(LEFT * 4 + DOWN * 1.5)
        self.play(FadeIn(ball))
        self.wait(1)
        
        # 动画序列：球移动并展示作用力箭头
        action_arrow = Arrow(start=ball.get_center(), end=RIGHT * 4 + DOWN * 1.5, color=GREEN, buff=0.1, stroke_width=5)
        self.play(ball.animate.shift(RIGHT * 5), GrowArrow(action_arrow), run_time=2)
        self.wait(0.5)
        
        # 墙展示反作用力箭头
        reaction_arrow = Arrow(start=RIGHT * 4 + DOWN * 1.5, end=ball.get_center(), color=ORANGE, buff=0.1, stroke_width=5)
        self.play(GrowArrow(reaction_arrow), run_time=1)
        self.wait(1)
        
        # 动态公式展示
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=36, color=WHITE).next_to(title, DOWN * 2)
        self.play(Write(formula))
        self.wait(0.5)
        
        # 强调负号
        negative_sign = formula[8:9]  # 提取负号部分
        self.play(negative_sign.animate.set_color(YELLOW).scale(1.5), run_time=1)
        self.wait(1)
        
        # 球反弹并箭头逐渐消失
        self.play(ball.animate.shift(LEFT * 2), Uncreate(action_arrow), Uncreate(reaction_arrow), run_time=2)
        self.wait(1)
        
        # 结束画面回顾
        recap_text = Text("每一个作用力都有大小相等、方向相反的反作用力", font_size=32, color=WHITE)
        recap_text.to_edge(DOWN)
        self.play(Write(recap_text))
        self.wait(2)
        
        # 画面定格
        self.play(FadeOut(VGroup(*self.mobjects)))