from manim import *

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=14, height=8, color=BLUE, fill_opacity=1).to_edge(DOWN)
        ground = Line(start=LEFT*7, end=RIGHT*7, color=GRAY).shift(DOWN*3)
        self.play(Create(background), Create(ground))
        self.wait(1)

        # 场景标题
        title = Text("力与反作用力的舞蹈：牛顿第三定律生动演绎", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 主要对象
        box = Rectangle(width=1.5, height=1, color=YELLOW, fill_opacity=0.8).move_to(DOWN*2)
        person = VGroup(
            Dot(point=DOWN*1.5 + LEFT*2, color=GREEN),  # 头部
            Line(start=DOWN*1.5 + LEFT*2, end=DOWN*2 + LEFT*2, color=GREEN),  # 身体
            Line(start=DOWN*2 + LEFT*2, end=DOWN*2.5 + LEFT*2.5, color=GREEN),  # 左腿
            Line(start=DOWN*2 + LEFT*2, end=DOWN*2.5 + LEFT*1.5, color=GREEN),  # 右腿
            Line(start=DOWN*2 + LEFT*2, end=DOWN*2.2 + LEFT*2.5, color=GREEN),  # 左手
            Line(start=DOWN*2 + LEFT*2, end=DOWN*2.2 + LEFT*1.5, color=GREEN),  # 右手
        )
        self.play(FadeIn(box), FadeIn(person))
        self.wait(1)

        # 推动箱子动画
        self.play(person.animate.shift(RIGHT*0.5), run_time=1)
        self.play(box.animate.shift(RIGHT*2), run_time=2)
        
        # 箭头表示作用力和反作用力
        action_arrow = Arrow(start=DOWN*2.2 + LEFT*1.5, end=DOWN*2.2 + RIGHT*0.5, color=RED)
        reaction_arrow = Arrow(start=DOWN*2, end=DOWN*2 + LEFT*1.5, color=BLUE)
        self.play(Create(action_arrow), Create(reaction_arrow))
        self.wait(1)

        # 显示公式
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=48, color=WHITE)
        formula.to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1)
        self.play(formula.animate.scale(1.2), run_time=1)
        self.wait(1)

        # 静止状态解释
        self.play(FadeOut(action_arrow), FadeOut(reaction_arrow), run_time=1)
        explanation_text = Text(
            "作用力和反作用力互相抵消，但它们作用在不同物体上。",
            font_size=28, color=WHITE
        ).to_edge(DOWN)
        self.play(Write(explanation_text))
        self.wait(2)

        # 重复概念演示
        self.play(FadeOut(explanation_text), person.animate.shift(LEFT*0.5), box.animate.shift(LEFT*2), run_time=1)
        repeat_action_arrow = Arrow(start=DOWN*2.2 + LEFT*1.5, end=DOWN*2.2 + RIGHT*0.5, color=RED)
        repeat_reaction_arrow = Arrow(start=DOWN*2, end=DOWN*2 + LEFT*1.5, color=BLUE)
        self.play(Create(repeat_action_arrow), Create(repeat_reaction_arrow))
        self.wait(2)
        
        # 结束场景
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=2)