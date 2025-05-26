from manim import *
import numpy as np

class EnergyFlowScene(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#001f3f"  # 深蓝色背景

        # 标题
        title = Text("热力学第二定律", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建容器
        red_container = Rectangle(width=2, height=1, color=RED, fill_opacity=0.6)
        blue_container = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.6)
        red_container.shift(LEFT*3)
        blue_container.shift(RIGHT*3)

        # 温度标签
        red_temp_label = MathTex(r"T_1 = 400 \, \text{K}", color=WHITE)
        blue_temp_label = MathTex(r"T_2 = 300 \, \text{K}", color=WHITE)
        red_temp_label.next_to(red_container, UP)
        blue_temp_label.next_to(blue_container, UP)

        # 显示容器和温度
        self.play(FadeIn(red_container), FadeIn(blue_container))
        self.play(Write(red_temp_label), Write(blue_temp_label))
        self.wait(1)

        # 热量流动箭头
        arrow_group = VGroup(
            *[Arrow(
                start=red_container.get_center() + RIGHT*i*0.5,
                end=blue_container.get_center() - LEFT*i*0.5,
                color=YELLOW
            ) for i in range(5)]
        )
        self.play(Create(arrow_group))
        self.wait(1)

        # 动态温度变化
        new_red_temp_label = MathTex(r"T_1 = 380 \, \text{K}", color=WHITE)
        new_blue_temp_label = MathTex(r"T_2 = 320 \, \text{K}", color=WHITE)
        new_red_temp_label.move_to(red_temp_label.get_center())
        new_blue_temp_label.move_to(blue_temp_label.get_center())

        self.play(
            Transform(red_temp_label, new_red_temp_label),
            Transform(blue_temp_label, new_blue_temp_label),
            run_time=2
        )
        self.wait(1)

        # 熵变化公式
        entropy_formula = MathTex(r"\Delta S = \frac{\Delta Q}{T}", font_size=48, color=WHITE)
        entropy_formula.scale(1.2).to_edge(DOWN)
        self.play(Write(entropy_formula))
        self.wait(1)

        # 分解熵公式
        system_entropy = MathTex(r"\Delta S_{\text{系统}} > 0", font_size=36, color=WHITE)
        total_entropy = MathTex(r"\Delta S_{\text{总}} \geq 0", font_size=36, color=WHITE)
        system_entropy.next_to(entropy_formula, UP, buff=0.5)
        total_entropy.next_to(entropy_formula, DOWN, buff=0.5)
        self.play(Write(system_entropy), Write(total_entropy))
        self.wait(1)

        # 时间轴和不可逆性强调
        time_axis = Line(LEFT*4, RIGHT*4, color=WHITE)
        time_axis.to_edge(DOWN, buff=1)
        time_label = Text("时间轴", font_size=24, color=WHITE)
        time_label.next_to(time_axis, DOWN)

        self.play(Create(time_axis), Write(time_label))
        self.wait(1)

        # 尝试逆向箭头
        reverse_arrow = Arrow(
            start=blue_container.get_center(),
            end=red_container.get_center(),
            color=RED
        )
        impossible_text = Text("不可能", font_size=36, color=RED)
        impossible_text.next_to(reverse_arrow, UP)

        self.play(Create(reverse_arrow))
        self.play(Write(impossible_text), run_time=1)
        self.wait(1)

        # 结束场景总结
        summary_text = Text(
            "热量总是从高温流向低温，熵总是增加。",
            font_size=32, color=WHITE
        )
        summary_text.to_edge(DOWN)
        self.play(Write(summary_text))
        self.wait(2)

        # 淡出所有对象
        self.play(FadeOut(VGroup(*self.mobjects)))