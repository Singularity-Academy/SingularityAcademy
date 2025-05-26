from manim import *
import numpy as np

class VariableUndefinedMaze(Scene):
    def construct(self):
        # 场景标题
        title = Text("勇闯错误迷宫：理解变量未定义问题", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 背景迷宫
        maze = VGroup()
        rows, cols = 5, 5
        for i in range(rows):
            for j in range(cols):
                cell = Square(side_length=1, color=LIGHT_BLUE, fill_opacity=0.3)
                cell.move_to(np.array([j - cols // 2, rows // 2 - i, 0]))
                maze.add(cell)
        maze.shift(DOWN * 1)
        self.play(Create(maze))
        self.wait(1)

        # 红色警告标识
        warning_sign = Text("变量未定义", font_size=28, color=RED)
        warning_sign.move_to(maze.get_center())
        warning_sign.scale(1.5)
        self.play(FadeIn(warning_sign))
        self.wait(1)

        # Shit角色
        shit = VGroup(
            Circle(radius=0.4, color=BROWN, fill_opacity=1),
            Text("Shit", font_size=24, color=WHITE)
        )
        shit.arrange(DOWN, buff=0.1)
        shit.move_to(maze[0].get_center())  # 起点位置
        self.play(FadeIn(shit))
        self.wait(1)

        # Shit尝试走迷宫
        move_attempt = shit.animate.move_to(maze[12].get_center())  # 随机移动到一个未定义位置
        self.play(move_attempt)
        error_message = Text("local variable 'e' referenced before assignment", font_size=20, color=RED)
        error_message.next_to(shit, UP)
        self.play(Write(error_message))
        self.wait(1)

        # 弹回起点
        self.play(shit.animate.move_to(maze[0].get_center()), FadeOut(error_message))
        self.wait(1)

        # 发光的定义变量门
        definition_door = VGroup(
            Rectangle(width=2, height=1, color=YELLOW, fill_opacity=0.5),
            MathTex(r"e = 2.718").scale(0.8)
        )
        definition_door.arrange(DOWN, buff=0.2)
        definition_door.move_to(maze[24].get_center())  # 定义门位置
        self.play(FadeIn(definition_door))
        self.wait(1)

        # 提示箭头
        arrow = Arrow(start=maze[0].get_center(), end=maze[24].get_center(), color=GREEN)
        self.play(Create(arrow))
        self.wait(1)

        # Shit正确走向定义门
        self.play(shit.animate.move_to(maze[24].get_center()))
        self.wait(1)
        self.play(FadeOut(warning_sign))
        self.wait(1)

        # 迷宫墙壁淡化
        self.play(FadeOut(maze), FadeOut(definition_door), FadeOut(arrow))
        self.wait(1)

        # 成功运行公式动画
        success_formula = MathTex(r"e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots", font_size=28, color=GREEN)
        success_formula.move_to(UP * 0.5)
        self.play(Write(success_formula))
        self.wait(2)

        # 总结文字
        summary_text = Text("定义变量是程序运行的基础，确保逻辑顺序正确！", font_size=28, color=WHITE)
        summary_text.move_to(DOWN)
        self.play(Write(summary_text))
        self.wait(3)

        # 场景结束
        self.play(FadeOut(VGroup(*self.mobjects)))