from manim import *
import numpy as np

class AdventureVariables(Scene):
    def construct(self):
        # 设置标题
        title = Text("冒险中的变量与定义：错误的启发之旅", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 背景变量漂浮效果
        variable_e = Text("e", font_size=48, color=BLUE)
        variable_x = Text("x", font_size=48, color=YELLOW)
        variable_y = Text("y", font_size=48, color=YELLOW)
        variable_e.shift(LEFT * 3 + UP * 2)
        variable_x.shift(RIGHT * 2 + UP)
        variable_y.shift(RIGHT * 3 + DOWN)
        self.play(FadeIn(variable_e), FadeIn(variable_x), FadeIn(variable_y))
        
        # 错误提示框
        error_box = Rectangle(width=5, height=1, color=RED)
        error_text = Text("local variable 'e' referenced before assignment", font_size=24, color=WHITE)
        error_group = VGroup(error_box, error_text)
        error_group.arrange(DOWN, buff=0.2)
        error_group.to_edge(DOWN)
        self.play(FadeIn(error_group))
        self.wait(1)
        
        # 引入冒险者 Shit
        adventurer = Text("Shit", font_size=36, color=WHITE)
        backpack = Rectangle(width=1, height=1.5, color=ORANGE)
        backpack_text = Text("Debug工具", font_size=18, color=WHITE)
        backpack_text.move_to(backpack.get_center())
        adventurer_group = VGroup(adventurer, backpack, backpack_text)
        adventurer_group.arrange(DOWN, buff=0.1)
        adventurer_group.to_edge(LEFT)
        self.play(FadeIn(adventurer_group))
        self.wait(1)
        
        # Shit 发现问题并使用工具
        magnifying_glass = Circle(radius=0.5, color=YELLOW)
        magnifying_glass.move_to(adventurer_group.get_center() + RIGHT * 2)
        self.play(FadeIn(magnifying_glass))
        self.play(magnifying_glass.animate.move_to(variable_e.get_center()))
        self.wait(1)
        
        # 修复变量 e
        repaired_e = Text("e = 2", font_size=48, color=GREEN)
        repaired_e.move_to(variable_e.get_center())
        self.play(Transform(variable_e, repaired_e))
        self.wait(1)
        
        # 公式生成
        formula = MathTex(r"E = mc^2", font_size=48, color=WHITE)
        formula.move_to(DOWN * 2)
        self.play(Write(formula))
        self.wait(1)
        
        # 总结与反思
        flag = Rectangle(width=3, height=1.5, color=YELLOW)
        flag_text = Text("定义变量，赋予生命！", font_size=24, color=BLACK)
        flag_text.move_to(flag.get_center())
        flag_group = VGroup(flag, flag_text)
        flag_group.to_edge(RIGHT)
        self.play(FadeIn(flag_group))
        self.wait(1)
        
        # 屏幕文字总结
        conclusion_text = Text("总是先定义变量再使用它们！", font_size=32, color=WHITE)
        conclusion_text.to_edge(DOWN)
        self.play(Write(conclusion_text))
        self.wait(2)
        
        # 淡出所有对象
        self.play(FadeOut(VGroup(*self.mobjects)))