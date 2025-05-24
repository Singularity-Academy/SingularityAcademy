from manim import *

class NewtonFirstLaw(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#87CEFA"  # 柔和蓝色背景

        # 场景标题
        title = Text("物体的静止与运动：揭开牛顿第一定律的奥秘", font_size=36, color=WHITE)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title))

        # 定义牛顿第一定律文字
        law_text = Tex(
            r"如果一个物体不受外力作用，\\它将保持静止或匀速直线运动状态。",
            font_size=36,
            color=WHITE,
        )
        self.play(FadeIn(law_text, shift=UP), run_time=2)
        self.wait(2)

        # 淡出定律文字
        self.play(FadeOut(law_text))

        # 场景1: 静止物体
        ground = Line(start=LEFT*6, end=RIGHT*6, color=WHITE).shift(DOWN*2)
        box = Square(color=GREY, fill_opacity=1).shift(DOWN*1.5)
        static_label = Tex(r"静止状态", font_size=28).next_to(box, UP)
        no_force_label = Tex(r"无外力作用", font_size=28).next_to(box, RIGHT)
        zero_force_arrow = Arrow(
            start=box.get_center() + RIGHT * 0.5,
            end=box.get_center() + RIGHT * 0.5,
            color=GREY,
        )

        self.play(Create(ground))
        self.play(FadeIn(box))
        self.play(Write(static_label))
        self.play(Write(no_force_label))
        self.play(Create(zero_force_arrow))
        self.wait(2)

        # 镜头轻微摇动以强调静止状态
        self.play(
            self.camera.frame.animate.shift(LEFT*0.2).shift(RIGHT*0.4).shift(LEFT*0.2),
            run_time=2,
        )
        self.wait(1)

        # 场景2: 匀速运动物体
        self.play(FadeOut(box, static_label, no_force_label, zero_force_arrow))

        ball = Circle(color=YELLOW, fill_opacity=1).shift(LEFT * 5 + DOWN * 1.5)
        velocity_arrow = Arrow(
            start=ball.get_center(),
            end=ball.get_center() + RIGHT * 1.5,
            color=GREEN,
        )
        velocity_label = Tex(r"匀速运动", font_size=28).next_to(ball, UP)

        self.play(FadeIn(ball))
        self.play(Create(velocity_arrow))
        self.play(Write(velocity_label))
        self.wait(1)

        # 球匀速运动动画
        self.play(
            ball.animate.shift(RIGHT * 8),
            velocity_arrow.animate.shift(RIGHT * 8),
            run_time=4,
        )
        self.wait(1)

        # 场景3: 外力作用
        force_arrow = Arrow(
            start=ball.get_center(),
            end=ball.get_center() + UP * 2 + LEFT * 1.5,
            color=RED,
        )
        force_label = Tex(r"外力作用下改变运动状态", font_size=28).next_to(force_arrow, UP)

        self.play(Create(force_arrow))
        self.play(Write(force_label))
        self.wait(1)

        # 球改变运动方向
        self.play(
            ball.animate.shift(UP * 2 + LEFT * 3),
            velocity_arrow.animate.shift(UP * 2 + LEFT * 3),
            run_time=3,
        )
        self.wait(1)

        # 场景4: 总结
        self.play(FadeOut(ball, velocity_arrow, force_arrow, force_label))

        summary_text = Tex(
            r"F_{\text{net}} = 0 \implies \text{物体保持静止或匀速直线运动}",
            font_size=36,
            color=WHITE,
        )
        conclusion_text = Text(
            "惯性让物体保持平稳，力改变一切。",
            font_size=28,
            color=YELLOW,
        ).next_to(summary_text, DOWN)

        self.play(FadeIn(summary_text, shift=UP), run_time=2)
        self.wait(2)
        self.play(FadeIn(conclusion_text, shift=UP), run_time=2)
        self.wait(3)
        self.play(FadeOut(summary_text, conclusion_text))