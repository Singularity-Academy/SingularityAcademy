from manim import *
import numpy as np

class VariableAdventure(Scene):
    def construct(self):
        # 标题
        title = Text("一坨💩的编程奇遇：变量未定义的冒险！", font_size=32, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景设置
        desk = Rectangle(width=12, height=6, color=ORANGE, fill_opacity=0.3)
        desk.to_edge(DOWN)
        self.play(FadeIn(desk))

        # 笔记本电脑
        laptop = Rectangle(width=5, height=3, color=LIGHT_BLUE, fill_opacity=0.8)
        laptop.move_to(UP * 1.5)
        self.play(Create(laptop))

        # 显示错误代码
        error_code = Text(
            "def calculate():\n    print(e)\n    e = 5\ncalculate()",
            font_size=24,
            color=WHITE,
        )
        error_code.move_to(laptop.get_center())
        self.play(FadeIn(error_code))
        self.wait(1)

        # 一坨💩跳出来
        poop = Text("💩", font_size=48)
        poop.move_to(laptop.get_center() + DOWN * 1.5)
        self.play(FadeIn(poop))
        self.wait(1)

        # 一坨💩说话
        speech_box = Rectangle(width=4, height=2, color=WHITE, fill_opacity=0.8)
        speech_box.next_to(poop, UP)
        speech_text = Text("哎呀！变量 'e' 没有定义，我该怎么办？", font_size=24, color=BLACK)
        speech_text.move_to(speech_box.get_center())
        self.play(FadeIn(speech_box), Write(speech_text))
        self.wait(2)

        self.play(FadeOut(speech_box), FadeOut(speech_text))

        # 显示错误提示
        error_message = Text(
            "local variable 'e' referenced before assignment",
            font_size=24,
            color=RED,
        )
        error_message.move_to(laptop.get_center() + DOWN * 1.5)
        self.play(Write(error_message))
        self.wait(2)
        self.play(FadeOut(error_message))

        # 旁白解释错误
        explanation_box = Rectangle(width=6, height=2, color=WHITE, fill_opacity=0.8)
        explanation_box.to_edge(UP)
        explanation_text = Text(
            "在代码中，你试图在定义变量之前引用它，这是不允许的。",
            font_size=24,
            color=BLACK,
        )
        explanation_text.move_to(explanation_box.get_center())
        self.play(FadeIn(explanation_box), Write(explanation_text))
        self.wait(2)
        self.play(FadeOut(explanation_box), FadeOut(explanation_text))

        # 一坨💩拿放大镜
        magnifying_glass = Circle(radius=0.7, color=WHITE)
        handle = Line(start=ORIGIN, end=DOWN * 0.5, color=WHITE)
        magnifying_glass.add(handle)
        magnifying_glass.move_to(poop.get_center() + RIGHT * 1)
        self.play(Create(magnifying_glass))
        self.wait(1)

        # 放大错误代码部分
        highlight_box = Rectangle(width=3, height=1, color=RED, fill_opacity=0.2)
        highlight_box.move_to(error_code.get_center() + UP * 0.5)
        self.play(FadeIn(highlight_box))
        self.wait(2)
        self.play(FadeOut(highlight_box))

        # 显示修正代码
        correct_code = Text(
            "def calculate():\n    e = 5\n    print(e)\ncalculate()",
            font_size=24,
            color=GREEN,
        )
        self.play(Transform(error_code, correct_code))
        self.wait(1)

        # 一坨💩开心地跳起来
        happy_poop = poop.copy()
        happy_poop.move_to(UP * 1.5)
        self.play(Transform(poop, happy_poop))
        self.wait(1)

        happy_text = Text("我懂了！先定义，再调用，这样就没问题啦！", font_size=24, color=WHITE)
        happy_text.next_to(poop, UP)
        self.play(Write(happy_text))
        self.wait(2)
        self.play(FadeOut(happy_text))

        # 显示总结
        summary_box = Rectangle(width=6, height=2, color=WHITE, fill_opacity=0.8)
        summary_box.to_edge(DOWN)
        summary_text = Text(
            "记住：变量必须先定义后使用，否则会报错哦！",
            font_size=24,
            color=BLACK,
        )
        summary_text.move_to(summary_box.get_center())
        self.play(FadeIn(summary_box), Write(summary_text))
        self.wait(2)

        # 结束
        self.play(FadeOut(VGroup(*self.mobjects)))