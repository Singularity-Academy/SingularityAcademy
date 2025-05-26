from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLUE, fill_opacity=1)
        background.set_gradient(BLUE, WHITE)
        self.add(background)
        self.wait(0.5)

        # 地面设置
        ground = Line(start=LEFT*6, end=RIGHT*6, color=GRAY)
        ground.shift(DOWN*2.5)
        self.play(Create(ground))
        self.wait(0.5)

        # 添加星光点缀
        stars = VGroup(
            *[Dot(point=np.random.uniform(-FRAME_WIDTH/2, FRAME_WIDTH/2)*RIGHT + 
                  np.random.uniform(-FRAME_HEIGHT/2, FRAME_HEIGHT/2)*UP, color=WHITE) 
              for _ in range(20)]
        )
        self.play(FadeIn(stars))
        self.wait(0.5)

        # 两个圆形物体
        red_circle = Circle(radius=0.5, color=RED, fill_opacity=0.5)
        blue_circle = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        red_circle.move_to(LEFT*3 + DOWN*2)
        blue_circle.move_to(RIGHT*3 + DOWN*2)
        self.play(FadeIn(red_circle), FadeIn(blue_circle))
        self.wait(0.5)

        # 圆形物体滑入屏幕中央
        self.play(
            red_circle.animate.shift(RIGHT*1.5),
            blue_circle.animate.shift(LEFT*1.5),
            run_time=2
        )
        self.wait(0.5)

        # 作用力和反作用力箭头
        force_arrow_red = Arrow(start=red_circle.get_center(), end=blue_circle.get_center(), color=GREEN)
        force_arrow_blue = Arrow(start=blue_circle.get_center(), end=red_circle.get_center(), color=GREEN)
        self.play(Create(force_arrow_red))
        self.wait(0.5)
        self.play(Create(force_arrow_blue))
        self.wait(0.5)

        # 箭头动态弹跳效果
        self.play(
            force_arrow_red.animate.shift(UP*0.2),
            force_arrow_blue.animate.shift(DOWN*0.2),
            run_time=0.5
        )
        self.play(
            force_arrow_red.animate.shift(DOWN*0.2),
            force_arrow_blue.animate.shift(UP*0.2),
            run_time=0.5
        )
        self.wait(1)

        # 公式展示
        formula = MathTex(r"\vec{F}_{AB} = -\vec{F}_{BA}", font_size=48, color=WHITE)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 添加文字说明
        action_text = Text("作用力", font_size=32, color=WHITE).next_to(force_arrow_red, UP)
        reaction_text = Text("反作用力", font_size=32, color=WHITE).next_to(force_arrow_blue, UP)
        self.play(Write(action_text), Write(reaction_text))
        self.wait(1)

        # 放大展示箭头和物体的交互
        self.play(
            self.camera.frame.animate.scale(0.8).move_to((red_circle.get_center() + blue_circle.get_center())/2),
            run_time=2
        )
        self.wait(1)

        # 渐隐所有元素，仅保留公式
        self.play(FadeOut(VGroup(red_circle, blue_circle, force_arrow_red, force_arrow_blue, action_text, reaction_text, ground, stars)))
        self.play(formula.animate.move_to(ORIGIN))
        self.wait(2)