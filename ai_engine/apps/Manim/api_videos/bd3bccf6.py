from manim import *

class NewtonFirstLaw(Scene):
    def construct(self):
        # 设置背景
        self.camera.background_color = "#1e1e2e"
        
        # 标题
        title = Text("牛顿第一定律 - 惯性原理", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 公式
        formula = MathTex(r"F = 0 \Rightarrow a = 0")
        formula.scale(1.2)
        formula.shift(UP*0.5)
        self.play(Write(formula))
        self.wait(1)
        
        # 地面
        ground = Line(LEFT*5, RIGHT*5, color=WHITE)
        ground.shift(DOWN*2)
        self.play(Create(ground))
        
        # 方块
        box = Square(side_length=0.8, color=RED, fill_opacity=0.7)
        box.shift(LEFT*2 + DOWN*1.6)
        self.play(Create(box))
        
        # 说明文字
        text1 = Text("物体保持静止状态", font_size=24, color=GREEN)
        text1.shift(DOWN*0.5)
        self.play(Write(text1))
        self.wait(2)
        
        # 施加力
        force_arrow = Arrow(
            start=box.get_right() + RIGHT*0.3,
            end=box.get_right() + RIGHT*1,
            color=YELLOW
        )
        self.play(Create(force_arrow))
        
        # 运动
        self.play(
            box.animate.shift(RIGHT*3),
            force_arrow.animate.shift(RIGHT*3),
            run_time=2
        )
        
        # 撤除力
        self.play(FadeOut(force_arrow))
        text2 = Text("撤除力后保持匀速运动", font_size=20, color=BLUE)
        text2.shift(DOWN*3)
        self.play(Write(text2))
        
        # 继续运动
        self.play(box.animate.shift(RIGHT*1.5), run_time=2, rate_func=linear)
        
        # 结论
        conclusion = Text("这就是惯性原理！", font_size=28, color=GOLD)
        conclusion.shift(UP*2)
        self.play(Write(conclusion))
        self.wait(2)
        
        # 淡出
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)