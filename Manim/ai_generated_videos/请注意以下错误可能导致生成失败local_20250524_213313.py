from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#0D1B2A"  # 深蓝渐变背景
        stars = VGroup(*[Dot(point=np.random.uniform(-8, 8, size=3), 
                             radius=0.02, color=WHITE) for _ in range(100)])
        self.add(stars)
        
        # 地面网格线
        ground = Line(start=LEFT*8, end=RIGHT*8, color=GRAY)
        ground.shift(DOWN*3)
        self.add(ground)
        
        # 标题
        title = Text("牛顿第三定律", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 主要对象
        ball_A = Circle(radius=0.5, color=RED, fill_opacity=0.8).shift(LEFT*3 + DOWN)
        ball_B = Circle(radius=0.5, color=BLUE, fill_opacity=0.8).shift(RIGHT*3 + DOWN)
        self.play(FadeIn(ball_A), FadeIn(ball_B))
        self.wait(1)

        # 第一阶段：静止的球体
        static_text = Text("静止状态下，球体之间无力的作用", font_size=24, color=WHITE)
        static_text.to_edge(DOWN)
        self.play(Write(static_text))
        self.wait(2)
        self.play(FadeOut(static_text))

        # 第二阶段：作用力和反作用力
        action_arrow = Arrow(start=ball_A.get_center(), 
                             end=ball_B.get_center(), 
                             color=RED, buff=0.5)
        reaction_arrow = Arrow(start=ball_B.get_center(), 
                               end=ball_A.get_center(), 
                               color=BLUE, buff=0.5)
        action_label = Text("作用力 (Action)", font_size=24, color=RED)
        reaction_label = Text("反作用力 (Reaction)", font_size=24, color=BLUE)
        action_label.next_to(action_arrow, UP)
        reaction_label.next_to(reaction_arrow, DOWN)
        
        self.play(ball_A.animate.shift(RIGHT*1),
                  Create(action_arrow), Write(action_label))
        self.wait(1)
        self.play(Create(reaction_arrow), Write(reaction_label))
        self.wait(1)

        # 第三阶段：公式动态展示
        formula = MathTex(r"F_{AB} = -F_{BA}", color=WHITE)
        formula.scale(1.5)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 振荡效果
        oscillation = ApplyWave(VGroup(action_arrow, reaction_arrow))
        self.play(oscillation, run_time=2)
        self.wait(1)

        # 第四阶段：注释框解释
        explanation = Text("每个作用力都有大小相等、方向相反的反作用力", 
                           font_size=24, color=WHITE)
        explanation.to_edge(DOWN)
        self.play(FadeIn(explanation))
        self.wait(2)

        # 第五阶段：淡出场景
        self.play(FadeOut(VGroup(ball_A, ball_B, action_arrow, reaction_arrow, 
                                 action_label, reaction_label, formula, explanation, ground)))
        self.play(FadeOut(stars))
        self.wait(1)