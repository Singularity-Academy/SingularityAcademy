from manim import *

class SecondLawEntropyScene(Scene):
    def construct(self):
        # 场景标题
        title = Text("混乱的定律：热力学第二定律的神奇之旅", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景设置
        background = Rectangle(width=16, height=9, color=BLUE, fill_opacity=1)
        stars = VGroup(*[
            Dot(color=WHITE).move_to(
                [random.uniform(-7, 7), random.uniform(-4, 4), 0]
            )
            for _ in range(50)
        ])
        self.add(background, stars)

        # 第1步：整齐排列的小球（低熵状态）
        container1 = Square(color=WHITE).scale(2).shift(LEFT * 3)
        ordered_balls = VGroup(*[
            Dot(color=RED).move_to(container1.get_center() + [x, y, 0])
            for x in [-1, 0, 1] for y in [-1, 0, 1]
        ])
        self.play(FadeIn(container1), FadeIn(ordered_balls))
        self.wait(1)

        # 标题文字：“什么是熵？”
        question_text = Text("什么是熵？", font_size=32, color=WHITE).shift(UP * 3)
        self.play(Write(question_text))
        self.wait(1)

        # 第2步：熵公式展示
        entropy_formula = MathTex(r"S = k \ln \Omega", font_size=48).shift(UP * 1.5)
        self.play(Write(entropy_formula))
        self.wait(1)

        # 旁白气泡解释熵定义
        explanation_text = Text("熵是系统的微观状态数的度量", font_size=24, color=WHITE).next_to(entropy_formula, DOWN)
        self.play(FadeIn(explanation_text))
        self.wait(2)

        # 第3步：小球开始随机运动
        self.play(
            ordered_balls.animate.arrange_in_grid(3, 3, buff=1.5).shift(RIGHT * 3),
            run_time=3
        )
        self.wait(1)

        # 动态时间轴展示熵增加
        timeline = Line(LEFT * 2, RIGHT * 2, color=YELLOW).shift(DOWN)
        arrow = Arrow(LEFT, RIGHT, color=YELLOW).next_to(timeline, UP, buff=0.2)
        time_text = Text("时间", font_size=24, color=WHITE).next_to(timeline, DOWN)
        entropy_text = Text("熵增加", font_size=24, color=YELLOW).next_to(arrow, UP)
        self.play(FadeIn(timeline), FadeIn(arrow), FadeIn(time_text), FadeIn(entropy_text))
        self.wait(2)

        # 第4步：第二个容器（高熵状态）
        container2 = Square(color=WHITE).scale(2).shift(RIGHT * 3)
        random_balls = VGroup(*[
            Dot(color=RED).move_to(container2.get_center() + [random.uniform(-1, 1), random.uniform(-1, 1), 0])
            for _ in range(9)
        ])
        self.play(FadeIn(container2), FadeIn(random_balls))
        self.wait(1)

        # 文本说明：“从有序到无序，熵增加不可逆”
        irreversible_text = Text("从有序到无序，熵增加不可逆", font_size=24, color=WHITE).shift(DOWN * 2)
        self.play(FadeIn(irreversible_text))
        self.wait(2)

        # 第5步：热力学第二定律文字展示
        second_law_text = Text(
            "热力学第二定律：孤立系统的熵总是趋向于增加或保持不变",
            font_size=30, color=WHITE
        ).shift(UP)
        self.play(Transform(entropy_text, second_law_text))
        self.wait(2)

        # 放大熵公式
        self.play(entropy_formula.animate.scale(1.5).shift(DOWN))
        self.wait(2)

        # 第6步：结束场景
        self.play(FadeOut(Group(*self.mobjects)))
        final_title = Text("混乱的定律：热力学第二定律", font_size=36, color=WHITE)
        self.play(FadeIn(final_title))
        self.wait(3)