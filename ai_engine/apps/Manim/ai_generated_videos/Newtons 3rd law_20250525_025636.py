from manim import *
import numpy as np

class NewtonThirdLaw(Scene):
    def construct(self):
        # 定义颜色和变量
        LIGHT_BLUE = "#87CEFA"
        YELLOW = "#FFFF00"
        RED = "#FF0000"
        GREEN = "#00FF00"
        PURPLE = "#800080"
        GRAY = "#D3D3D3"
        WHITE = "#FFFFFF"

        # 阶段1：引入定律
        self.camera.background_color = LIGHT_BLUE
        title = Text("Newton's Third Law", font_size=48, color=WHITE).to_edge(UP)
        formula = MathTex(r"F_{action} = -F_{reaction}", font_size=48, color=WHITE).next_to(title, DOWN)
        explanation = Text("Every action has an equal and opposite reaction.", font_size=24, color=WHITE).next_to(formula, DOWN)
        self.play(FadeIn(title))
        self.wait(1)
        self.play(Write(formula))
        self.wait(1)
        self.play(FadeIn(explanation))
        self.wait(2)
        self.play(FadeOut(title, formula, explanation))

        # 阶段2：球和立方体交互
        ground = Line(start=np.array([-6, -2, 0]), end=np.array([6, -2, 0]), color=GRAY)
        ball = Circle(radius=0.5, color=YELLOW, fill_opacity=1).shift(np.array([-3, -1.5, 0]))
        cube = Square(side_length=1, color=RED, fill_opacity=1).shift(np.array([3, -1.5, 0]))
        self.play(Create(ground), Create(ball), Create(cube))

        # 动画：球碰撞立方体
        action_arrow = Arrow(start=ball.get_center(), end=cube.get_center(), color=GREEN, buff=0.1)
        reaction_arrow = Arrow(start=cube.get_center(), end=ball.get_center(), color=PURPLE, buff=0.1)
        self.play(ball.animate.shift(RIGHT * 2.5), Create(action_arrow))
        self.play(Create(reaction_arrow))
        self.wait(1)

        # 阶段3：动态展示
        action_text = Text("Action", font_size=24, color=GREEN).next_to(action_arrow, UP)
        reaction_text = Text("Reaction", font_size=24, color=PURPLE).next_to(reaction_arrow, UP)
        self.play(FadeIn(action_text), FadeIn(reaction_text))
        self.play(ball.animate.shift(LEFT * 2), cube.animate.shift(RIGHT * 2))
        self.wait(2)

        # 阶段4：总结
        self.play(FadeOut(ball, cube, action_arrow, reaction_arrow, ground, action_text, reaction_text))
        formula_final = MathTex(r"F_{action} = -F_{reaction}", font_size=48, color=WHITE)
        self.play(Write(formula_final))
        summary = Text("Newton's Third Law governs all interactions in mechanics.", font_size=24, color=WHITE).next_to(formula_final, DOWN)
        self.play(Write(summary))
        self.wait(3)