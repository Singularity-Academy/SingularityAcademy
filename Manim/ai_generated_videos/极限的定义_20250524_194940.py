from manim import *

class RevealLimitDefinition(Scene):
    def construct(self):
        # 中文标题
        title = Text("揭开极限的秘密：直观理解ε-δ定义", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景设置
        background_grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.2}
        )
        self.add(background_grid)

        # 函数曲线：f(x) = x^2
        function_curve = background_grid.plot(lambda x: x**2, x_range=[-2.5, 2.5], color=BLUE)
        self.play(Create(function_curve), run_time=2)
        self.wait(1)

        # 标记点和坐标轴说明
        a = 1  # x趋近的点
        L = a**2  # f(a)对应的值

        a_dot = Dot(background_grid.c2p(a, L), color=YELLOW)
        a_label = MathTex(r"(a, L)").next_to(a_dot, UP)
        self.play(FadeIn(a_dot), Write(a_label))
        self.wait(1)

        # ε-区间
        epsilon = 0.5
        epsilon_rect = Rectangle(
            width=6, 
            height=2 * epsilon, 
            color=GREEN, 
            fill_opacity=0.3
        ).move_to(background_grid.c2p(0, L))
        epsilon_label = Text("ε-区间", font_size=24, color=GREEN).next_to(epsilon_rect, RIGHT)
        self.play(FadeIn(epsilon_rect), Write(epsilon_label))
        self.wait(1)

        # δ-区间
        delta = 0.5
        delta_rect = Rectangle(
            height=6, 
            width=2 * delta, 
            color=RED, 
            fill_opacity=0.3
        ).move_to(background_grid.c2p(a, 0))
        delta_label = Text("δ-区间", font_size=24, color=RED).next_to(delta_rect, DOWN)
        self.play(FadeIn(delta_rect), Write(delta_label))
        self.wait(1)

        # 高亮函数曲线在δ区间内的部分
        highlighted_curve = background_grid.plot(
            lambda x: x**2, x_range=[a-delta, a+delta], color=YELLOW, stroke_width=4
        )
        self.play(Create(highlighted_curve), run_time=2)

        # 数学公式展示
        limit_formula = MathTex(
            r"\lim_{x \to a} f(x) = L \quad \text{当且仅当} \quad \forall \epsilon > 0, \exists \delta > 0, \text{使得} |x-a|<\delta \implies |f(x)-L|<\epsilon",
            font_size=32,
            color=YELLOW
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(limit_formula), run_time=3)
        self.wait(2)

        # 动态缩小ε和δ区间
        new_epsilon = 0.2
        new_delta = 0.2

        new_epsilon_rect = Rectangle(
            width=6, 
            height=2 * new_epsilon, 
            color=GREEN, 
            fill_opacity=0.3
        ).move_to(background_grid.c2p(0, L))
        new_delta_rect = Rectangle(
            height=6, 
            width=2 * new_delta, 
            color=RED, 
            fill_opacity=0.3
        ).move_to(background_grid.c2p(a, 0))

        self.play(Transform(epsilon_rect, new_epsilon_rect), Transform(delta_rect, new_delta_rect), run_time=2)
        self.wait(1)

        # 总结文本
        conclusion = Text(
            "极限的定义要求我们能够找到一个足够小的δ，使得函数值始终落入指定的ε区间。",
            font_size=28, color=WHITE
        ).to_edge(DOWN, buff=1)
        self.play(Write(conclusion), run_time=2)
        self.wait(2)

        # 结束动画
        self.play(FadeOut(Group(*self.mobjects)))