from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color=BLUE_D, fill_opacity=1)
        background.set_color_by_gradient(BLUE_D, BLUE_E)
        self.add(background)
        
        # 地面设置
        ground = Rectangle(width=FRAME_WIDTH, height=0.5, color=GREY, fill_opacity=1)
        ground.move_to(DOWN * 3.5)
        self.add(ground)
        
        # 添加网格线
        grid = NumberPlane(x_range=(-FRAME_WIDTH / 2, FRAME_WIDTH / 2, 1), 
                           y_range=(-FRAME_HEIGHT / 2, FRAME_HEIGHT / 2, 1), 
                           background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.3})
        self.add(grid)
        
        # 创建两个方块
        box_a = Square(side_length=1, color=RED, fill_color=RED, fill_opacity=0.8)
        box_b = Square(side_length=1, color=BLUE, fill_color=BLUE, fill_opacity=0.8)
        box_a.move_to(LEFT * 3)
        box_b.move_to(RIGHT * 3)
        
        # 显示方块动画
        self.play(FadeIn(box_a), FadeIn(box_b))
        self.wait(1)
        
        # 创建力箭头和标签
        force_a_arrow = Arrow(start=box_a.get_right(), end=box_b.get_left(), color=RED, buff=0.1, stroke_width=4)
        force_b_arrow = Arrow(start=box_b.get_left(), end=box_a.get_right(), color=BLUE, buff=0.1, stroke_width=4)
        label_a = Text("作用力", font_size=32, color=RED)
        label_b = Text("反作用力", font_size=32, color=BLUE)
        label_a.next_to(force_a_arrow, UP)
        label_b.next_to(force_b_arrow, UP)

        # 显示力箭头和标签动画
        self.play(Create(force_a_arrow), Write(label_a))
        self.wait(1)
        self.play(Create(force_b_arrow), Write(label_b))
        self.wait(1)
        
        # 显示公式
        formula = MathTex(r"F_A = -F_B", font_size=48, color=WHITE)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(1)
        
        # 动态展示方块互推
        box_a_target = box_a.copy().shift(RIGHT * 1.5)
        box_b_target = box_b.copy().shift(LEFT * 1.5)
        force_a_arrow_target = Arrow(start=box_a_target.get_right(), end=box_b_target.get_left(), color=RED, buff=0.1, stroke_width=4)
        force_b_arrow_target = Arrow(start=box_b_target.get_left(), end=box_a_target.get_right(), color=BLUE, buff=0.1, stroke_width=4)

        self.play(
            Transform(box_a, box_a_target),
            Transform(box_b, box_b_target),
            Transform(force_a_arrow, force_a_arrow_target),
            Transform(force_b_arrow, force_b_arrow_target),
            run_time=2
        )
        self.wait(1)
        
        # 动画结束时所有元素缩小并聚集到屏幕中央
        summary_group = VGroup(box_a, box_b, force_a_arrow, force_b_arrow, formula, label_a, label_b)
        self.play(summary_group.animate.scale(0.5).move_to(ORIGIN), run_time=2)
        
        # 总结性画面
        summary_text = Text("牛顿第三定律：每个作用力都有大小相等、方向相反的反作用力", font_size=32, color=WHITE)
        summary_text.next_to(formula, DOWN)
        self.play(Write(summary_text))
        self.wait(2)

        # 淡出所有元素
        self.play(FadeOut(VGroup(*self.mobjects)))