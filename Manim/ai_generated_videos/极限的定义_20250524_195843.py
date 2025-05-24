from manim import *

class RevealLimitMystery(Scene):
    def construct(self):
        # 设置背景颜色为浅蓝色渐变
        background_rect = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color=BLUE, fill_opacity=0.3)
        background_rect.set_z_index(-1)  # 放置在最底层
        self.add(background_rect)

        # 添加网格背景
        grid = NumberPlane()
        self.play(FadeIn(grid, run_time=1))
        self.wait(0.5)

        # 中文标题: "揭开极限的神秘面纱"
        title = Text("揭开极限的神秘面纱", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 显示公式: lim_{x \to a} f(x) = L
        formula = MathTex(r"\lim_{x \to a} f(x) = L", font_size=48, color=WHITE)
        formula.to_edge(UP + LEFT, buff=0.5)
        self.play(Write(formula))
        self.wait(1)

        # 缓缓出现文字: "什么是极限？"
        question_text = Text("什么是极限？", font_size=32, color=YELLOW)
        question_text.next_to(formula, DOWN, buff=0.5)
        self.play(FadeIn(question_text, run_time=1))
        self.wait(1)

        # 绘制函数曲线 f(x) = 1/x
        curve = FunctionGraph(lambda x: 1 / x, x_range=[0.1, 5], color=BLUE)
        self.play(Create(curve, run_time=2))
        explanation_text = Text("这是函数的图像", font_size=28, color=WHITE)
        explanation_text.next_to(curve, UP, buff=0.5)
        self.play(FadeIn(explanation_text))
        self.wait(1)

        # 标注趋近点和目标值
        a = 2  # x趋近的点
        L = 1 / a  # 极限值
        dot_a = Dot(point=[a, 0, 0], color=RED)
        label_a = MathTex(r"x = a", font_size=28, color=RED)
        label_a.next_to(dot_a, DOWN, buff=0.2)
        dot_L = Dot(point=[0, L, 0], color=GREEN)
        label_L = MathTex(r"y = L", font_size=28, color=GREEN)
        label_L.next_to(dot_L, LEFT, buff=0.2)
        self.play(FadeIn(dot_a), Write(label_a), FadeIn(dot_L), Write(label_L))
        self.wait(1)

        # 绘制辅助线
        x_line = DashedLine(start=[a, 0, 0], end=[a, L, 0], color=YELLOW)
        y_line = DashedLine(start=[0, L, 0], end=[a, L, 0], color=YELLOW)
        self.play(Create(x_line), Create(y_line))
        self.wait(1)

        # 动态演示趋近过程
        moving_dot = Dot(point=[0.5, 1 / 0.5, 0], color=PURPLE)
        self.add(moving_dot)
        self.play(moving_dot.animate.move_to([a, L, 0]), run_time=3, rate_func=smooth)
        dynamic_text = Text("当 x → a, f(x) → L", font_size=32, color=WHITE)
        dynamic_text.next_to(formula, DOWN, buff=0.5)
        self.play(FadeIn(dynamic_text))
        self.wait(2)

        # 显示公式并强调关键部分
        highlight = SurroundingRectangle(formula, color=YELLOW)
        self.play(Create(highlight))
        self.wait(1)

        # 场景逐渐暗淡，显示总结文字
        summary_text = Text("极限是数学分析的基石，定义了函数在特定点附近的行为", font_size=28, color=WHITE)
        summary_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(summary_text), FadeOut(grid, curve, dot_a, dot_L, x_line, y_line, moving_dot, dynamic_text, highlight))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(title, formula, summary_text, background_rect))