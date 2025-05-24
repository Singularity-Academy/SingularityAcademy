from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLUE, fill_opacity=1)
        grid = NumberPlane(x_range=(-7, 7, 1), y_range=(-4, 4, 1), background_line_style={"stroke_color": GREY})
        title = Text("牛顿第三定律", font_size=36, color=WHITE)
        title.to_corner(DR)
        
        self.add(background)
        self.play(Create(grid), FadeIn(title))
        self.wait(1)
        
        # 创建方块和箭头
        red_square = Square(side_length=1, color=RED, fill_opacity=0.8)
        blue_square = Square(side_length=1, color=BLUE, fill_opacity=0.8)
        
        red_square.move_to(LEFT*4)
        blue_square.move_to(RIGHT*4)
        
        self.play(FadeIn(red_square), FadeIn(blue_square))
        self.wait(1)
        
        # 方块移动到中央
        self.play(
            red_square.animate.shift(RIGHT*3),
            blue_square.animate.shift(LEFT*3),
            run_time=2
        )
        self.wait(1)
        
        # 添加作用力和反作用力箭头
        action_arrow = Arrow(start=red_square.get_center(), end=blue_square.get_center(), color=GREEN, buff=0.1)
        reaction_arrow = Arrow(start=blue_square.get_center(), end=red_square.get_center(), color=ORANGE, buff=0.1)
        
        action_label = Text("作用力", font_size=24, color=GREEN).next_to(action_arrow, UP)
        reaction_label = Text("反作用力", font_size=24, color=ORANGE).next_to(reaction_arrow, DOWN)
        
        self.play(Create(action_arrow), Write(action_label))
        self.wait(1)
        self.play(Create(reaction_arrow), Write(reaction_label))
        self.wait(1)
        
        # 添加公式
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=36, color=WHITE)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(2)
        
        # 方块被箭头推动
        self.play(
            red_square.animate.shift(LEFT*2),
            blue_square.animate.shift(RIGHT*2),
            run_time=2
        )
        self.wait(1)
        
        # 淡出所有元素，强调标题
        self.play(FadeOut(VGroup(red_square, blue_square, action_arrow, reaction_arrow, action_label, reaction_label, formula, grid)))
        emphasized_title = Text("力的对称性", font_size=48, color=WHITE).to_edge(UP)
        self.play(Transform(title, emphasized_title))
        self.wait(2)