from manim import *

class NewtonFirstLawScene(Scene):
    def construct(self):
        # 设置背景
        self.camera.background_color = DARK_BLUE
        
        # 标题动画
        title = Text("牛顿第一定律", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        
        # 公式展示
        formula = MathTex(r"F = 0 \rightarrow v = constant", font_size=36, color=YELLOW)
        formula.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(formula), run_time=2)
        self.wait(1)
        
        # 左侧静止物体演示
        static_text = Text("静止状态：没有外力作用，物体保持静止。", font_size=24, color=WHITE)
        static_text.to_edge(LEFT).shift(UP * 2)
        self.play(Write(static_text), run_time=2)
        
        # 静止物体
        block = Square(side_length=1, color=WHITE, fill_opacity=1)
        block.to_edge(LEFT).shift(DOWN * 1.5)
        self.play(FadeIn(block), run_time=2)

        # 力箭头尝试推动方块
        force_arrow = Arrow(start=block.get_left(), end=block.get_right(), color=RED, buff=0.1)
        self.play(Create(force_arrow), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(force_arrow), run_time=1)  # 力箭头消失，方块保持静止
        self.wait(1)

        # 渐隐左侧文字和物体
        self.play(FadeOut(static_text, block), run_time=2)
        self.wait(0.5)

        # 右侧匀速运动物体演示
        motion_text = Text("匀速运动：没有外力作用，物体保持匀速直线运动。", font_size=24, color=WHITE)
        motion_text.to_edge(RIGHT).shift(UP * 2)
        self.play(Write(motion_text), run_time=2)

        # 匀速运动小球
        ball = Circle(radius=0.5, color=ORANGE, fill_opacity=1)
        ball.to_edge(RIGHT).shift(DOWN * 1.5)
        self.play(FadeIn(ball), run_time=1)

        # 小球匀速滚动
        self.play(ball.animate.shift(LEFT * 6), run_time=3, rate_func=linear)

        # 力箭头短暂出现
        force_arrow_ball = Arrow(start=ball.get_left(), end=ball.get_right(), color=RED, buff=0.1)
        self.play(Create(force_arrow_ball), run_time=0.5)
        self.play(FadeOut(force_arrow_ball), run_time=0.5)

        # 渐隐右侧文字和小球
        self.play(FadeOut(motion_text, ball), run_time=2)
        self.wait(0.5)

        # 总结与结束
        summary_text = Text("牛顿第一定律揭示了物体运动的基本规律——惯性。", font_size=24, color=WHITE)
        summary_text.to_edge(DOWN)
        self.play(Write(summary_text), run_time=2)
        self.wait(2)

        self.play(FadeOut(Group(*self.mobjects)), run_time=2)