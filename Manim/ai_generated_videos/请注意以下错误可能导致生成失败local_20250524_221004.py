from manim import *
import numpy as np

class ProgrammingAdventure(Scene):
    def construct(self):
        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=LIGHT_GREY, fill_opacity=1)
        grid = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1], background_line_style={"stroke_color": YELLOW, "stroke_width": 0.5})
        self.add(background, grid)
        
        # 场景标题
        title = Text("一坨💩的编程冒险：变量赋值与错误排查", font_size=36, color=BLACK)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 主角💩
        poop = SVGMobject("poop.svg")
        poop.scale(0.5)
        poop.set_color(BROWN)
        poop.move_to(LEFT*5 + DOWN*1)
        book = Text("编程书", font_size=24, color=WHITE)
        book.next_to(poop, RIGHT, buff=0.5)
        poop_group = VGroup(poop, book)
        self.play(FadeIn(poop_group, shift=UP))
        self.wait(1)

        # 💩运行错误代码
        code_wrong = Code(
            code="""def calculate_area():
    return e * e""",
            language="Python",
            font="Monospace",
            background="rectangle",
            style="monokai",
            insert_line_no=False,
        )
        code_wrong.scale(0.7)
        code_wrong.to_edge(RIGHT)
        self.play(FadeIn(code_wrong, shift=DOWN))
        self.wait(1)
        
        # 错误信息
        error_message = Text("Error: local variable 'e' referenced before assignment", font_size=24, color=RED)
        error_message.next_to(code_wrong, DOWN, buff=0.5)
        self.play(Write(error_message))
        self.wait(1)

        # 放大镜展示错误
        magnifier = Circle(color=BLACK, radius=1.5)
        magnifier.move_to(code_wrong.get_center() + UP*0.5 + LEFT*1.5)
        highlight = Rectangle(width=1.5, height=0.5, color=RED, fill_opacity=0.5)
        highlight.move_to(code_wrong.get_center() + UP*0.5 + LEFT*1.5)
        self.play(Create(magnifier), FadeIn(highlight))
        self.wait(1)

        # 💩思考错误原因
        thought_bubble = SVGMobject("thought_bubble.svg")
        thought_bubble.set_color(GREY)
        thought_bubble.scale(0.8)
        thought_bubble.next_to(poop, UP, buff=0.5)
        reason_text = Text("我忘记定义变量‘e’了！", font_size=24, color=BLACK)
        reason_text.move_to(thought_bubble.get_center())
        self.play(FadeIn(thought_bubble), Write(reason_text))
        self.wait(1)

        # 正确代码展示
        code_correct = Code(
            code="""def calculate_area():
    e = 5
    return e * e""",
            language="Python",
            font="Monospace",
            background="rectangle",
            style="monokai",
            insert_line_no=False,
        )
        code_correct.scale(0.7)
        code_correct.next_to(code_wrong, DOWN, buff=1.5)
        self.play(FadeIn(code_correct, shift=DOWN))
        self.wait(1)

        # 变量‘e’状态变化
        e_undefined = Square(side_length=0.5, color=GREY)
        e_defined = e_undefined.copy().set_color(GREEN)
        e_undefined.move_to(code_wrong.get_center() + UP*0.5 + LEFT*3)
        e_defined.move_to(code_correct.get_center() + UP*0.5 + LEFT*3)
        self.play(FadeIn(e_undefined), Transform(e_undefined, e_defined))
        self.wait(1)

        # 运行正确代码
        result_text = Text("运行结果：25", font_size=24, color=BLUE)
        result_text.next_to(code_correct, DOWN, buff=0.5)
        self.play(Write(result_text))
        self.wait(1)

        # 💩庆祝成功
        self.play(poop.animate.shift(UP*0.5), FadeOut(error_message), FadeOut(thought_bubble), FadeOut(reason_text))
        self.play(poop.animate.shift(DOWN*0.5))
        self.wait(1)
        
        # 结尾总结
        summary = Text("记得在使用变量之前，先定义它！", font_size=28, color=BLACK)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)

        # 💩挥手告别
        self.play(FadeOut(poop_group), FadeOut(code_wrong), FadeOut(code_correct), FadeOut(result_text), FadeOut(summary))
        self.wait(1)