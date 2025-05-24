from manim import *

class Physics(Scene):
    def construct(self):
        # 标题
        title = Text("牛顿第一定律", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 物理公式
        formula = MathTex(r"\sum F = 0 \Rightarrow a = 0", font_size=32)
        self.play(Write(formula))
        self.wait(1)
        
        # 物体演示
        box = Square(side_length=1, color=RED, fill_opacity=0.7)
        box.shift(LEFT*2)
        self.play(Create(box))
        
        # 文字说明
        explanation = Text("物体保持静止或匀速运动", font_size=24, color=GREEN)
        explanation.shift(DOWN*2)
        self.play(Write(explanation))
        self.wait(2)
        
        # 结束
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)
