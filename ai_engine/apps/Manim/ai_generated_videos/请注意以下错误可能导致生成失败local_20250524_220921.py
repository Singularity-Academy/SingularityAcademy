from manim import *
import numpy as np

class VariableScopeAdventure(Scene):
    def construct(self):
        # 场景标题
        title = Text("一坨💩的编程历险记：变量作用域探险", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景设置
        background = Rectangle(width=14, height=8, color=LIGHT_BLUE, fill_opacity=0.8)
        background.to_edge(DOWN)
        self.add(background)

        # 主角一坨💩
        poop = Text("💩", font_size=64, color=WHITE)
        poop.move_to(LEFT * 5 + DOWN * 2)
        self.play(FadeIn(poop))
        self.wait(1)

        # 编程森林中的代码元素
        code_line1 = Text("def my_function():", font_size=32, color=GREEN)
        code_line2 = Text("    x = 10", font_size=32, color=YELLOW)
        code_line3 = Text("    return x", font_size=32, color=GREEN)
        code_group = VGroup(code_line1, code_line2, code_line3).arrange(DOWN, buff=0.3)
        code_group.to_edge(LEFT)
        self.play(Write(code_group))
        self.wait(1)

        # 问题出现：红色错误提示框
        error_box = Rectangle(width=6, height=1, color=RED, fill_opacity=0.5)
        error_text = Text("local variable 'e' referenced before assignment", font_size=20, color=WHITE)
        error_group = VGroup(error_box, error_text)
        error_group.move_to(RIGHT * 3 + UP * 2)
        self.play(FadeIn(error_group))
        self.wait(1)

        # 错误状态：变量‘e’灰色
        variable_e = Text("e", font_size=48, color=GRAY)
        variable_e.move_to(RIGHT * 3)
        self.play(FadeIn(variable_e))
        self.wait(1)

        # 动画箭头指向变量‘e’，显示未定义状态
        arrow = Arrow(start=LEFT * 2, end=variable_e.get_center(), color=RED)
        arrow_text = Text("未定义", font_size=24, color=RED)
        arrow_text.next_to(arrow, UP)
        self.play(Create(arrow), Write(arrow_text))
        self.wait(1)

        # 一坨💩尝试引用变量‘e’，被弹回红色区域
        self.play(poop.animate.shift(RIGHT * 2))
        self.wait(0.5)
        self.play(poop.animate.shift(LEFT * 2))
        self.wait(1)

        # 解决问题：一坨💩捡起绿色代码片段并定义变量‘e’
        code_snippet = Text("e = 5", font_size=32, color=GREEN)
        code_snippet.move_to(DOWN * 2 + LEFT * 3)
        self.play(FadeIn(code_snippet))
        self.wait(1)
        self.play(code_snippet.animate.move_to(variable_e.get_center()))
        self.wait(1)

        # 变量‘e’变为绿色，错误提示框消失
        variable_e.set_color(GREEN)
        self.play(FadeOut(error_group), Transform(code_snippet, variable_e))
        self.wait(1)

        # 背景恢复明亮
        background.set_fill(opacity=1)
        self.play(FadeIn(background))
        self.wait(1)

        # 总结与欢呼
        solution_text = Text("定义变量‘e’后再引用它", font_size=28, color=GREEN)
        solution_text.to_edge(DOWN)
        self.play(Write(solution_text), poop.animate.shift(UP * 2))
        self.wait(1)

        # 森林中的代码元素闪烁，庆祝成功
        self.play(
            code_group.animate.set_color(YELLOW),
            run_time=2
        )
        self.wait(1)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))