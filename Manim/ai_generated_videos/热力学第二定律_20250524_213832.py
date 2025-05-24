from manim import *
import numpy as np

class ThermodynamicsSecondLaw(Scene):
    def construct(self):
        # 深蓝色背景
        self.camera.background_color = "#001f3f"

        # 标题
        title = Text("从混乱到秩序：热力学第二定律的秘密", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 左侧橙色高温区域和右侧蓝色低温区域
        high_temp_box = Rectangle(width=3, height=2, color=ORANGE, fill_color=ORANGE, fill_opacity=0.5)
        low_temp_box = Rectangle(width=3, height=2, color=BLUE, fill_color=BLUE, fill_opacity=0.5)
        high_temp_box.shift(LEFT * 4)
        low_temp_box.shift(RIGHT * 4)

        self.play(Create(high_temp_box), Create(low_temp_box))
        self.wait(1)

        # 热能粒子（橙色小圆点）
        particles = VGroup(*[Dot(color=ORANGE).move_to(high_temp_box.get_center() + np.random.uniform(-1.5, 1.5, size=2) * [3, 1]) for _ in range(15)])

        self.play(FadeIn(particles))
        self.wait(1)

        # 粒子快速随机运动
        for _ in range(3):
            self.play(*[particle.animate.move_to(
                high_temp_box.get_center() + np.random.uniform(-1.5, 1.5, size=2) * [3, 1]
            ) for particle in particles], run_time=0.5)
        self.wait(1)

        # 热量传递箭头
        arrow = Arrow(start=high_temp_box.get_center(), end=low_temp_box.get_center(), color=YELLOW)
        self.play(Create(arrow))
        self.wait(1)

        # 粒子转移到低温区域
        self.play(*[particle.animate.move_to(
            low_temp_box.get_center() + np.random.uniform(-1.5, 1.5, size=2) * [3, 1]
        ) for particle in particles], run_time=2)

        # 颜色渐变到淡黄色
        self.play(
            high_temp_box.animate.set_fill(color="#FFD700", opacity=0.5),
            low_temp_box.animate.set_fill(color="#FFD700", opacity=0.5),
            run_time=2
        )
        self.wait(1)

        # 熵公式展示
        entropy_formula = MathTex(r"S = k \ln \Omega", font_size=48)
        entropy_formula.move_to(ORIGIN)
        self.play(Write(entropy_formula), run_time=2)
        self.wait(1)

        # 粒子运动减缓，展示复杂轨迹
        for particle in particles:
            self.play(particle.animate.move_to(
                particle.get_center() + np.random.uniform(-0.5, 0.5, size=2)
            ), run_time=0.5, rate_func=smooth)
        self.wait(1)

        # 文字说明
        explanation = Text("熵增意味着不可逆性", font_size=32, color=YELLOW)
        explanation.next_to(entropy_formula, DOWN)
        self.play(FadeIn(explanation))
        self.wait(2)

        # 总结与结论
        conclusion = Text("孤立系统的熵总是趋于增加", font_size=36, color=WHITE)
        conclusion.to_edge(DOWN)
        self.play(FadeIn(conclusion))
        self.wait(2)

        # 结束动画
        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(1)