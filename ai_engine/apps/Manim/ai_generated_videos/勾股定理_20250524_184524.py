from manim import *

class PythagoreanTheoremScene(Scene):
    def construct(self):
        # 设置背景颜色和网格线
        self.camera.background_color = BLUE_E
        grid = NumberPlane(background_line_style={"stroke_opacity": 0.2})
        self.add(grid)

        # 场景标题
        title = Text("勾股定理", font_size=32, color=WHITE)
        title.to_corner(DR)
        self.add(title)

        # Step 1: 绘制直角三角形并标注边长
        triangle = Polygon(
            [0, 0, 0], [3, 0, 0], [0, 4, 0],
            color=WHITE
        ).set_fill(BLUE, opacity=0.3)
        a_label = MathTex("a=3").next_to(triangle, LEFT, buff=0.2)
        b_label = MathTex("b=4").next_to(triangle, DOWN, buff=0.2)
        c_label = MathTex("c=5").next_to(triangle, UP + RIGHT, buff=0.2)

        self.play(Create(triangle))
        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.wait(1)

        # Step 2: 动态生成正方形并显示面积公式
        square_a = Square(side_length=3, color=GREEN).next_to(triangle, LEFT, buff=0)
        square_b = Square(side_length=4, color=YELLOW).next_to(triangle, DOWN, buff=0)
        square_c = Square(side_length=5, color=BLUE).next_to(triangle, UP + RIGHT, buff=0)

        area_a_text = MathTex("a^2 = 3^2 = 9").next_to(square_a, LEFT, buff=0.4)
        area_b_text = MathTex("b^2 = 4^2 = 16").next_to(square_b, DOWN, buff=0.4)
        area_c_text = MathTex("c^2 = 5^2 = 25").next_to(square_c, UP, buff=0.4)

        self.play(Create(square_a))
        self.play(Write(area_a_text))
        self.wait(1)

        self.play(Create(square_b))
        self.play(Write(area_b_text))
        self.wait(1)

        self.play(Create(square_c))
        self.play(Write(area_c_text))
        self.wait(1)

        # Step 3: 拼接两个较小正方形的面积到大正方形
        square_a_target = square_a.copy().move_to(square_c.get_center() + LEFT * 2.5)
        square_b_target = square_b.copy().move_to(square_c.get_center() + DOWN * 2.5)

        self.play(
            Transform(square_a, square_a_target),
            Transform(square_b, square_b_target),
            run_time=2
        )
        self.wait(1)

        # Step 4: 显示公式并高亮相等关系
        formula = MathTex("a^2 + b^2 = c^2", font_size=48, color=WHITE)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        highlight_rect = SurroundingRectangle(formula, color=RED, buff=0.2)
        self.play(Create(highlight_rect))
        self.wait(1)

        # Step 5: 淡出所有对象并显示结束文字
        end_text = Text("数学的美，尽在勾股定理", font_size=36, color=WHITE)
        end_text.move_to(ORIGIN)

        self.play(FadeOut(Group(*self.mobjects)))
        self.play(FadeIn(end_text))
        self.wait(2)