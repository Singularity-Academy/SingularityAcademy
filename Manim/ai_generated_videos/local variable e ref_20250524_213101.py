from manim import *

class NewtonThirdLawDance(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#87CEEB"  # 浅蓝背景
        grid = NumberPlane(background_line_style={"stroke_opacity": 0.2, "stroke_width": 1})
        self.add(grid)

        # 标题和公式
        title = Text("牛顿第三定律", font_size=36, color=WHITE)
        title.to_corner(UR)
        formula = MathTex(r"F_A = -F_B", font_size=36, color=YELLOW)
        formula.to_corner(DL)

        self.play(Write(title), FadeIn(formula))
        self.wait(1)

        # 主要对象
        ball_a = Circle(radius=0.5, color=RED, fill_opacity=1).move_to(LEFT*3)
        ball_b = Circle(radius=0.5, color=BLUE, fill_opacity=1).move_to(RIGHT*3)
        arrow_ab = Arrow(ball_a.get_center(), ball_b.get_center(), color=GREEN, buff=0.5)
        arrow_ba = Arrow(ball_b.get_center(), ball_a.get_center(), color=PURPLE, buff=0.5)
        label_ab = Text("作用力", font_size=24, color=GREEN).next_to(arrow_ab, UP)
        label_ba = Text("反作用力", font_size=24, color=PURPLE).next_to(arrow_ba, UP)

        self.play(FadeIn(ball_a), FadeIn(ball_b))
        self.wait(1)

        # 动画：施加作用力
        self.play(Create(arrow_ab), Write(label_ab))
        self.wait(0.5)
        self.play(Create(arrow_ba), Write(label_ba))
        self.wait(1)

        # 动画：球体移动
        spring = Line(ball_a.get_center(), ball_b.get_center(), color=GRAY, stroke_width=3)
        self.play(Create(spring))
        self.wait(1)

        self.play(
            ball_a.animate.shift(RIGHT*2),
            ball_b.animate.shift(RIGHT*2),
            spring.animate.put_start_and_end_on(ball_a.get_center(), ball_b.get_center()),
            arrow_ab.animate.put_start_and_end_on(ball_a.get_center(), ball_b.get_center()),
            arrow_ba.animate.put_start_and_end_on(ball_b.get_center(), ball_a.get_center()),
            label_ab.animate.next_to(arrow_ab, UP),
            label_ba.animate.next_to(arrow_ba, UP),
            run_time=2
        )
        self.wait(1)

        # 动画：总结与强调
        summary = Text("每个作用力都有一个大小相等、方向相反的反作用力", font_size=30, color=WHITE)
        summary.to_edge(DOWN)

        self.play(Write(summary))
        self.wait(2)

        # 结束场景
        self.play(FadeOut(VGroup(ball_a, ball_b, arrow_ab, arrow_ba, label_ab, label_ba, spring, formula, title, summary)))
        final_formula = MathTex(r"F_A = -F_B", font_size=48, color=YELLOW)
        self.play(Write(final_formula))
        self.wait(1)
        self.play(FadeOut(final_formula))