from manim import *
import numpy as np

class VariableUndefinedMystery(Scene):
    def construct(self):
        # 场景背景
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLUE, fill_opacity=1)
        self.add(background)

        # 标题
        title = Text("勇闯“变量未定义”之谜", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Shit角色
        shit = Circle(radius=0.5, color=ORANGE, fill_opacity=1)
        shit_text = Text("Shit", font_size=24, color=BLACK)
        shit_group = VGroup(shit, shit_text).move_to(LEFT * 4)
        self.play(Create(shit))
        self.play(Write(shit_text))
        self.wait(1)

        # 漂浮代码片段
        code_snippets = VGroup(
            Text("x = 42", font_size=24, color=GREEN),
            Text("y = x + 1", font_size=24, color=GREEN),
            Text("print(y)", font_size=24, color=GREEN)
        )
        code_snippets.arrange(DOWN, buff=0.5).to_edge(RIGHT)
        self.play(FadeIn(code_snippets))
        self.wait(1)

        # 变量“e”角色
        e_var = Circle(radius=0.5, color=WHITE, fill_opacity=0.3)  # 半透明
        e_text = Text("e", font_size=24, color=BLACK)
        e_group = VGroup(e_var, e_text).move_to(RIGHT * 4)
        self.play(FadeIn(e_group))
        self.wait(1)

        # 错误提示框
        error_box = Rectangle(width=5, height=1, color=RED, fill_opacity=1)
        error_text = Text("local variable 'e' referenced before assignment", font_size=20, color=WHITE)
        error_group = VGroup(error_box, error_text).to_edge(DOWN)
        self.play(FadeIn(error_group))
        self.wait(1)

        # Shit尝试调用“e”
        self.play(shit.animate.shift(RIGHT * 2))
        self.play(e_var.animate.shift(UP * 0.5).fade_to(color=BLUE, opacity=0.1))  # 消失
        self.wait(1)

        # 分析公式框
        formula_box = Rectangle(width=6, height=1.5, color=GREEN, fill_opacity=0.3)
        formula_text = MathTex(r"e = mc^2")
        formula_group = VGroup(formula_box, formula_text).move_to(UP * 2)
        self.play(FadeIn(formula_group))
        self.wait(1)

        # Shit解决问题
        code_pen = Line(start=ORIGIN, end=UP * 0.5, color=YELLOW).move_to(shit.get_center() + RIGHT * 0.5)
        self.play(Create(code_pen))
        self.wait(0.5)

        # 写下代码修复
        fixed_code = Text("e = 2.71", font_size=24, color=GREEN).move_to(formula_group.get_center() + DOWN * 2)
        self.play(Write(fixed_code))
        self.play(e_var.animate.set_fill(color=WHITE, opacity=1))  # 变量“e”从半透明变实心
        self.play(FadeOut(error_group))
        self.wait(1)

        # 成功庆祝
        celebration_text = Text("变量定义成功!", font_size=32, color=YELLOW)
        celebration_text.move_to(UP * 3)
        self.play(Write(celebration_text))

        # 背景颜色渐变
        self.play(background.animate.set_fill(color=GREEN, opacity=1))
        self.wait(1)

        # Shit和“e”跳舞
        self.play(
            shit.animate.shift(UP * 0.5).rotate(PI / 4),
            e_var.animate.shift(DOWN * 0.5).rotate(-PI / 4),
            run_time=2
        )
        self.wait(1)

        # 漂浮的代码片段重新排列成完整代码块
        final_code = VGroup(
            Text("e = 2.71", font_size=24, color=GREEN),
            Text("E = mc^2", font_size=24, color=GREEN),
            Text("print(E)", font_size=24, color=GREEN)
        )
        final_code.arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(Transform(code_snippets, final_code))
        self.wait(2)

        # 结束
        self.play(FadeOut(VGroup(*self.mobjects)))