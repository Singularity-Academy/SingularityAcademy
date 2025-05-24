from manim import *

class NewtonThirdLaw(Scene):
    def construct(self):
        # 背景设置
        self.camera.background_color = "#87CEEB"  # 蓝色背景
        grid = NumberPlane(x_range=[-6, 6], y_range=[-4, 4], background_line_style={"stroke_opacity": 0.2})
        self.add(grid)

        # 标题文字
        title = Text("牛顿第三定律", font_size=32, color=WHITE)
        title.to_corner(DR)
        self.add(title)

        # 创建物体A和物体B
        ball_A = Circle(radius=0.5, color=RED, fill_opacity=0.6).shift(LEFT * 2)
        ball_B = Circle(radius=0.5, color=BLUE, fill_opacity=0.6).shift(RIGHT * 2)
        label_A = Text("物体A", font_size=24, color=RED).next_to(ball_A, DOWN)
        label_B = Text("物体B", font_size=24, color=BLUE).next_to(ball_B, DOWN)

        # 地板线
        floor_line = Line(start=LEFT * 6, end=RIGHT * 6, color=GRAY)
        self.play(Create(floor_line))
        self.wait(0.5)

        # 添加物体和标签
        self.play(FadeIn(ball_A, ball_B, label_A, label_B))
        self.wait(0.5)

        # 作用力箭头和标签
        force_AB = Arrow(start=ball_A.get_center(), end=ball_B.get_center(), color=RED, buff=0.2, stroke_width=4)
        label_force_AB = Text("作用力", font_size=24, color=RED).next_to(force_AB, UP)

        # 反作用力箭头和标签
        force_BA = Arrow(start=ball_B.get_center(), end=ball_A.get_center(), color=BLUE, buff=0.2, stroke_width=4)
        label_force_BA = Text("反作用力", font_size=24, color=BLUE).next_to(force_BA, DOWN)

        # 添加作用力箭头和标签
        self.play(GrowArrow(force_AB), Write(label_force_AB))
        self.wait(0.5)
        self.play(GrowArrow(force_BA), Write(label_force_BA))
        self.wait(0.5)

        # 公式展示
        formula = MathTex(r"F_{AB} = -F_{BA}", font_size=48, color=WHITE).shift(DOWN * 2)
        self.play(Write(formula))
        self.wait(1)

        # 动态振动效果
        self.play(
            force_AB.animate.shift(UP * 0.1).shift(DOWN * 0.1),
            force_BA.animate.shift(DOWN * 0.1).shift(UP * 0.1),
            run_time=2,
            rate_func=there_and_back
        )
        self.wait(1)

        # 结束总结文字
        summary_text = Text("大小相等，方向相反——牛顿第三定律", font_size=32, color=WHITE).shift(DOWN * 3)
        self.play(Write(summary_text))
        self.wait(2)

        # 淡出所有元素
        self.play(FadeOut(VGroup(grid, ball_A, ball_B, label_A, label_B, force_AB, force_BA, label_force_AB, label_force_BA, formula, summary_text, floor_line)))