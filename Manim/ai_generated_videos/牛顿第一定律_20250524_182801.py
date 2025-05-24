from manim import *

class NewtonFirstLaw(Scene):
    def construct(self):
        # 标题
        title = Text("牛顿第一定律 - 惯性原理", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 公式
        formula = MathTex(r"F = ma")
        formula.scale(1.2)
        formula.to_edge(UP).shift(DOWN)
        self.play(Write(formula))
        self.wait(1)
        
        # 地面
        ground = Line(LEFT * 6, RIGHT * 6, color=WHITE)
        ground.shift(DOWN * 2)
        self.play(Create(ground))
        
        # 方块
        box = Square(side_length=0.8, color=RED, fill_opacity=0.7)
        box.shift(LEFT * 3 + DOWN * 1.6)
        self.play(Create(box))
        self.wait(1)
        
        # 静止状态说明
        rest_text = Text("物体处于静止状态", font_size=24)
        rest_text.shift(UP * 0.5)
        self.play(Write(rest_text))
        self.wait(2)
        
        # 施加力
        force_arrow = Arrow(
            start=box.get_right() + RIGHT * 0.5, 
            end=box.get_right() + RIGHT * 1.5, 
            color=YELLOW,
            buff=0
        )
        force_label = Text("F", font_size=20, color=YELLOW)
        force_label.next_to(force_arrow, UP)
        
        self.play(
            FadeOut(rest_text),
            Create(force_arrow),
            Write(force_label)
        )
        
        # 方块运动
        self.play(
            box.animate.shift(RIGHT * 4),
            force_arrow.animate.shift(RIGHT * 4),
            force_label.animate.shift(RIGHT * 4),
            run_time=2
        )
        
        # 撤除力后继续运动
        motion_text = Text("撤除力后，物体保持匀速运动", font_size=24)
        motion_text.shift(UP * 0.5)
        
        self.play(
            FadeOut(force_arrow),
            FadeOut(force_label),
            Write(motion_text)
        )
        
        self.play(
            box.animate.shift(RIGHT * 2),
            run_time=2,
            rate_func=linear
        )
        
        # 结论
        conclusion = Text("这就是牛顿第一定律 - 惯性原理", font_size=28, color=GREEN)
        conclusion.shift(DOWN * 3)
        self.play(Write(conclusion))
        self.wait(3)
        
        # 淡出所有元素
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)