from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#87CEEB"  # 浅蓝色渐变背景
        ground = Rectangle(width=FRAME_WIDTH, height=0.5, color=GRAY, fill_opacity=0.5).to_edge(DOWN)
        ground_label = Text("地面", font_size=24, color=WHITE).next_to(ground, UP, buff=0.2)

        # 创建背景和地面
        self.play(Create(ground), Write(ground_label))
        self.wait(1)

        # 标题
        title = Text("力的对话：牛顿第三定律的精彩演绎", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 主要对象
        red_square = Square(side_length=1, color=RED, fill_opacity=0.8)
        blue_circle = Circle(radius=0.6, color=BLUE, fill_opacity=0.8)

        # 对象位置
        red_square.move_to(LEFT * 3 + DOWN * 0.5)
        blue_circle.move_to(RIGHT * 3 + DOWN * 0.5)

        # 显示红色方块和蓝色球
        self.play(FadeIn(red_square), FadeIn(blue_circle))
        self.wait(1)

        # 力箭头和标签
        action_arrow = Arrow(start=red_square.get_center(), end=blue_circle.get_center(), color=RED, buff=0.2)
        action_label = Text("作用力", font_size=24, color=RED).next_to(action_arrow, UP, buff=0.2)

        reaction_arrow = Arrow(start=blue_circle.get_center(), end=red_square.get_center(), color=BLUE, buff=0.2)
        reaction_label = Text("反作用力", font_size=24, color=BLUE).next_to(reaction_arrow, DOWN, buff=0.2)

        # 显示作用力箭头和标签
        self.play(Create(action_arrow), Write(action_label))
        self.wait(1)

        # 显示反作用力箭头和标签
        self.play(Create(reaction_arrow), Write(reaction_label))
        self.wait(1)

        # 显示公式
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=36, color=WHITE)
        formula.to_edge(DOWN)
        explanation = Text("作用力与反作用力大小相等，方向相反", font_size=28, color=WHITE).next_to(formula, UP, buff=0.3)
        self.play(Write(formula), Write(explanation))
        self.wait(2)

        # 动态展示物体运动
        self.play(
            red_square.animate.shift(LEFT * 0.5),
            blue_circle.animate.shift(RIGHT * 0.5),
            run_time=2
        )
        self.wait(1)

        # 镜头拉远，展示总结文字
        summary = Text("牛顿第三定律在任何物体间均适用", font_size=30, color=WHITE)
        scene_application = Text("比如火箭发射：火箭向下喷气，地面反作用力推动火箭升空", font_size=24, color=WHITE)
        summary.to_edge(UP)
        scene_application.next_to(summary, DOWN, buff=0.5)

        # 展示总结场景
        self.play(FadeOut(VGroup(red_square, blue_circle, action_arrow, reaction_arrow, action_label, reaction_label, formula, explanation)))
        self.play(Write(summary), Write(scene_application))
        self.wait(3)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))