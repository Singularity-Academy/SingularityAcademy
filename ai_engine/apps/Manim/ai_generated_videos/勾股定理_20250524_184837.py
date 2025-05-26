from manim import *

class UnlockTriangleMystery(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#87CEEB"  # 浅蓝色背景

        # 中文标题
        title = Text("解锁三角形的奥秘：勾股定理的视觉证明", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 场景开始 - 绘制直角三角形
        triangle = Polygon(
            ORIGIN, RIGHT * 3, UP * 4,
            color=WHITE
        ).shift(LEFT * 2)
        side_a = Text("a", font_size=24, color=RED).next_to(triangle, LEFT, buff=0.3)
        side_b = Text("b", font_size=24, color=GREEN).next_to(triangle, DOWN, buff=0.3)
        side_c = Text("c", font_size=24, color=BLUE).next_to(triangle, RIGHT, buff=0.3)

        self.play(Create(triangle), run_time=2)
        self.play(Write(side_a), Write(side_b), Write(side_c))
        self.wait(1)

        # 添加正方形
        square_a = Square(side_length=3, color=RED, fill_opacity=0.5).next_to(triangle, LEFT, buff=0)
        square_b = Square(side_length=4, color=GREEN, fill_opacity=0.5).next_to(triangle, DOWN, buff=0)
        square_c = Square(side_length=5, color=BLUE, fill_opacity=0.5).next_to(triangle, RIGHT, buff=0)

        self.play(FadeIn(square_a), FadeIn(square_b), FadeIn(square_c), run_time=2)
        self.wait(1)

        # 添加面积标签
        area_a = MathTex("a^2", color=RED).move_to(square_a.get_center())
        area_b = MathTex("b^2", color=GREEN).move_to(square_b.get_center())
        area_c = MathTex("c^2", color=BLUE).move_to(square_c.get_center())

        self.play(Write(area_a), Write(area_b), Write(area_c), run_time=2)
        self.wait(1)

        # 面积标签动态移动到斜边正方形
        self.play(
            Transform(area_a.copy(), area_c),
            Transform(area_b.copy(), area_c),
            run_time=3
        )
        self.wait(1)

        # 显示公式
        formula = MathTex("a^2 + b^2 = c^2", color=YELLOW, font_size=48)
        formula.move_to(DOWN * 2)
        self.play(Write(formula), run_time=2)
        self.wait(1)

        # 镜头拉远，显示完整场景
        self.play(
            self.camera.frame.animate.scale(1.5).move_to(ORIGIN),
            run_time=2
        )
        self.wait(2)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)), run_time=2)