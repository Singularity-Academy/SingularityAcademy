from manim import *

class NewtonFirstLaw(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1e1e2e"  # 深色背景

        # 场景标题
        title = Text("牛顿第一定律 - 惯性原理", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # 牛顿第一定律公式
        formula = MathTex(r"F_{net} = 0 \Rightarrow v = \text{constant}")
        formula.scale(1.2)
        formula.to_edge(UP).shift(DOWN*0.8)
        self.play(Write(formula))
        self.wait(1)

        # 定律描述
        law_text = Text(
            "物体在不受外力或受平衡力时\n保持静止或匀速直线运动状态",
            font_size=28,
            color=BLUE
        )
        law_text.next_to(formula, DOWN, buff=0.5)
        self.play(FadeIn(law_text, shift=UP), run_time=2)
        self.wait(2)

        # 淡出描述文字
        self.play(FadeOut(law_text))

        # 创建地面
        ground = Line(start=LEFT*6, end=RIGHT*6, color=WHITE)
        ground.shift(DOWN*2)
        self.play(Create(ground))

        # 场景1: 静止物体
        box = Square(side_length=0.8, color=RED, fill_opacity=0.7)
        box.shift(LEFT*3 + DOWN*1.6)
        self.play(Create(box))
        
        static_label = Text("静止状态", font_size=24, color=GREEN)
        static_label.next_to(box, UP)
        self.play(Write(static_label))
        self.wait(2)

        # 场景2: 施加力
        force_arrow = Arrow(
            start=box.get_right() + RIGHT*0.5,
            end=box.get_right() + RIGHT*1.5,
            color=YELLOW,
            buff=0
        )
        force_label = Text("施加力 F", font_size=20, color=YELLOW)
        force_label.next_to(force_arrow, UP)

        self.play(
            FadeOut(static_label),
            Create(force_arrow),
            Write(force_label)
        )

        # 方块运动
        motion_text = Text("加速运动", font_size=24, color=ORANGE)
        motion_text.shift(UP*0.5)
        self.play(Write(motion_text))
        
        self.play(
            box.animate.shift(RIGHT*4),
            force_arrow.animate.shift(RIGHT*4),
            force_label.animate.shift(RIGHT*4),
            run_time=2
        )

        # 场景3: 撤除力后继续运动
        inertia_text = Text("撤除力后，物体保持匀速运动", font_size=24, color=PURPLE)
        inertia_text.shift(DOWN*3)

        self.play(
            FadeOut(force_arrow),
            FadeOut(force_label),
            FadeOut(motion_text),
            Write(inertia_text)
        )

        # 速度矢量
        velocity_arrow = Arrow(
            start=box.get_center(),
            end=box.get_center() + RIGHT*1,
            color=GREEN,
            buff=0
        )
        velocity_label = Text("v = 常数", font_size=18, color=GREEN)
        velocity_label.next_to(velocity_arrow, UP, buff=0.1)

        self.play(
            Create(velocity_arrow),
            Write(velocity_label)
        )

        # 继续匀速运动
        self.play(
            box.animate.shift(RIGHT*2),
            velocity_arrow.animate.shift(RIGHT*2),
            velocity_label.animate.shift(RIGHT*2),
            run_time=2,
            rate_func=linear
        )

        # 最终结论
        conclusion = Text("这就是牛顿第一定律 - 惯性原理", font_size=28, color=GREEN)
        conclusion.shift(DOWN*0.5)
        self.play(
            FadeOut(inertia_text),
            Write(conclusion)
        )
        self.wait(2)

        # 显示完整公式
        final_formula = MathTex(
            r"\sum F = 0 \Rightarrow \Delta v = 0",
            font_size=36,
            color=GOLD
        )
        final_formula.shift(DOWN*1.5)
        self.play(Write(final_formula))
        self.wait(2)

        # 淡出所有元素
        self.play(FadeOut(Group(*self.mobjects)))
        
        # 结束语
        end_text = Text("感谢观看！", font_size=36, color=WHITE)
        self.play(Write(end_text))
        self.wait(2)
        self.play(FadeOut(end_text)) 