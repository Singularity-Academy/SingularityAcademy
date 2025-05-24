from manim import *

class SimpleNewton(Scene):
    def construct(self):
        # 标题
        title = Text("牛顿第一定律", font_size=48, color=WHITE)
        self.play(Write(title))
        self.wait(1)
        
        # 公式
        formula = MathTex(r"F = 0", font_size=36)
        formula.shift(DOWN)
        self.play(Write(formula))
        self.wait(1)
        
        # 方块演示
        box = Square(color=RED, fill_opacity=0.5)
        box.shift(LEFT*2)
        self.play(Create(box))
        
        # 说明
        text = Text("物体保持静止", font_size=24, color=GREEN)
        text.shift(DOWN*2)
        self.play(Write(text))
        self.wait(2)
        
        # 淡出
        self.play(FadeOut(Group(*self.mobjects)))
