from manim import *
import numpy as np

class ActionReaction(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color=BLUE_E, fill_opacity=1)
        self.add(background)
        
        # 标题
        title = Text("Newton's 3rd Law", font_size=36, color=WHITE)
        subtitle = Text("作用力与反作用力：力的大小相等，方向相反", font_size=24, color=WHITE)
        title.to_corner(UL)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        
        # 地面栅格网格
        ground = Rectangle(width=FRAME_WIDTH, height=1, fill_color=GRAY, fill_opacity=0.5)
        ground.to_edge(DOWN)
        grid = NumberPlane(x_range=[-7, 7, 1], y_range=[-2, 2, 1], background_line_style={"stroke_color": WHITE, "stroke_opacity": 0.3})
        grid.move_to(ground.get_center())
        self.add(grid, ground)
        
        # 创建两个方块
        red_block = Square(side_length=1, color=RED, fill_opacity=1)
        blue_block = Square(side_length=1, color=BLUE, fill_opacity=1)
        red_block.move_to(LEFT*2 + DOWN*1.5)
        blue_block.move_to(RIGHT*2 + DOWN*1.5)
        
        # 添加标签
        label_a = Text("物体A", font_size=24, color=RED)
        label_b = Text("物体B", font_size=24, color=BLUE)
        label_a.next_to(red_block, UP, buff=0.3)
        label_b.next_to(blue_block, UP, buff=0.3)
        
        self.play(FadeIn(red_block), FadeIn(blue_block), Write(label_a), Write(label_b))
        self.wait(1)
        
        # 作用力箭头
        action_arrow = Arrow(start=red_block.get_center(), end=blue_block.get_center(), color=RED, buff=0)
        reaction_arrow = Arrow(start=blue_block.get_center(), end=red_block.get_center(), color=BLUE, buff=0)
        
        # 添加箭头与动画
        self.play(Create(action_arrow))
        self.play(blue_block.animate.shift(RIGHT*2), Create(reaction_arrow))
        self.wait(1)
        
        # 展示公式
        formula = MathTex(r"F_{A \to B} = -F_{B \to A}", font_size=48, color=YELLOW)
        formula.to_edge(UP, buff=1)
        self.play(Write(formula))
        self.wait(1)
        
        # 箭头长度动态变化
        self.play(
            action_arrow.animate.scale(1.5),
            reaction_arrow.animate.scale(1.5),
            run_time=2
        )
        self.wait(1)
        
        # 生活场景联想
        human_a = Circle(radius=0.5, color=RED, fill_opacity=0.7).shift(LEFT*2 + UP*1)
        human_b = Circle(radius=0.5, color=BLUE, fill_opacity=0.7).shift(RIGHT*2 + UP*1)
        push_arrow = Arrow(start=human_a.get_center(), end=human_b.get_center(), color=RED, buff=0)
        push_reaction_arrow = Arrow(start=human_b.get_center(), end=human_a.get_center(), color=BLUE, buff=0)
        
        self.play(FadeOut(VGroup(red_block, blue_block, action_arrow, reaction_arrow, label_a, label_b, formula)))
        self.play(FadeIn(human_a), FadeIn(human_b), Create(push_arrow), Create(push_reaction_arrow))
        
        life_text = Text("无论是推墙还是划船，作用力与反作用力始终存在", font_size=24, color=WHITE)
        life_text.to_edge(DOWN)
        self.play(Write(life_text))
        self.wait(1)
        
        # 结尾
        final_formula = MathTex(r"F_{A \to B} = -F_{B \to A}", font_size=48, color=YELLOW)
        final_formula.move_to(ORIGIN)
        conclusion_text = Text("大小相等，方向相反", font_size=28, color=WHITE)
        conclusion_text.next_to(final_formula, DOWN, buff=0.5)
        
        self.play(FadeOut(VGroup(human_a, human_b, push_arrow, push_reaction_arrow, life_text)))
        self.play(Write(final_formula), Write(conclusion_text))
        self.wait(2)
        
        self.play(FadeOut(VGroup(final_formula, conclusion_text)))