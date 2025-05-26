from manim import *
import numpy as np

class VariableMaze(Scene):
    def construct(self):
        # 参数设置
        maze_color = "#6A5ACD"
        error_color = RED
        correct_color = GREEN
        bg_gradient = [BLUE, PURPLE]

        # 背景设置
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color=bg_gradient[0], fill_opacity=1)
        background.set_fill(color=bg_gradient[1], opacity=1)
        self.add(background)

        # 场景标题
        title = Text("变量迷宫：解决e未定义的历险记", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 迷宫入口与出口
        entrance = Text("错误区域", font_size=24, color=error_color)
        entrance.move_to(LEFT * 5 + DOWN * 2)
        exit = Text("正确区域", font_size=24, color=correct_color)
        exit.move_to(RIGHT * 5 + UP * 2)

        # 迷宫设置
        maze = VGroup(
            Line(LEFT * 4, RIGHT * 4, color=maze_color),
            Line(LEFT * 4 + UP * 2, LEFT * 4 + DOWN * 2, color=maze_color),
            Line(RIGHT * 4 + UP * 2, RIGHT * 4 + DOWN * 2, color=maze_color),
            Line(LEFT * 2, LEFT * 2 + UP * 2, color=maze_color),
            Line(LEFT * 2 + UP * 2, RIGHT * 2 + DOWN * 2, color=maze_color),
            Line(RIGHT * 2 + UP * 2, RIGHT * 2, color=maze_color),
        )
        self.play(Create(maze), FadeIn(entrance), FadeIn(exit))
        self.wait(1)

        # 主角 "Shit" 出现
        shit_svg_path = "./shit.svg"  # 替换为实际文件路径
        shit = SVGMobject(shit_svg_path).scale(0.5).set_color(YELLOW)
        shit.move_to(LEFT * 5 + DOWN * 2)
        self.play(FadeIn(shit))
        self.wait(1)

        # 错误路径演示
        error_code = MathTex(
            r"\text{def calculate\_energy():}",
            r"\text{return e * c**2}",
            font_size=28
        ).arrange(DOWN, aligned_edge=LEFT).set_color(error_color)
        error_code.move_to(LEFT * 2 + UP * 1)
        error_warning = Text("变量未定义！请检查代码。", font_size=24, color=error_color)
        error_warning.move_to(LEFT * 2 + DOWN * 2)

        self.play(shit.animate.shift(RIGHT * 3), Write(error_code))
        self.wait(1)
        self.play(FadeIn(error_warning))
        self.wait(1)

        # 修正路径展示
        correct_code = MathTex(
            r"\text{def calculate\_energy():}",
            r"\text{e = 1  \# 定义变量}",
            r"\text{return e * c**2}",
            font_size=28
        ).arrange(DOWN, aligned_edge=LEFT).set_color(correct_color)
        correct_code.move_to(RIGHT * 2 + UP * 1)
        correct_tip = Text("变量必须在使用前定义！", font_size=24, color=correct_color)
        correct_tip.move_to(RIGHT * 2 + DOWN * 2)

        self.play(shit.animate.shift(RIGHT * 3), Write(correct_code))
        self.wait(1)
        self.play(FadeIn(correct_tip))
        self.wait(1)

        # 走向正确区域
        self.play(shit.animate.shift(RIGHT * 3 + UP * 4))
        self.wait(1)

        # 总结与结束
        summary = Text(
            "牢记：在使用变量之前，务必先赋值或定义它！",
            font_size=28,
            color=WHITE
        )
        summary.to_edge(DOWN)
        self.play(FadeIn(summary))
        self.wait(2)

        # 角色庆祝
        self.play(shit.animate.scale(1.5).rotate(PI / 2))
        self.wait(1)

        # 整体淡出
        self.play(FadeOut(VGroup(*self.mobjects)))