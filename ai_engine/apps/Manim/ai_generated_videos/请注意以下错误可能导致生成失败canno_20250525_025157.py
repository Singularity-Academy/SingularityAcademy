from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 定义常量
        BACKGROUND_COLOR = "#87CEEB"  # 淡蓝色
        WALL_COLOR = "#4F4F4F"  # 深灰色
        GROUND_COLOR = "#D3D3D3"  # 浅灰色
        BALL_COLOR = RED
        FORCE_COLOR = GREEN
        REACTION_COLOR = BLUE
        TEXT_COLOR = WHITE
        RUN_TIME = 2
        
        # 设置背景
        self.camera.background_color = BACKGROUND_COLOR
        
        # 地面
        ground = Rectangle(width=FRAME_WIDTH, height=0.3, color=GROUND_COLOR, fill_color=GROUND_COLOR, fill_opacity=1)
        ground.to_edge(DOWN)
        
        # 墙壁
        wall = Rectangle(width=0.3, height=FRAME_HEIGHT, color=WALL_COLOR, fill_color=WALL_COLOR, fill_opacity=1)
        wall.to_edge(RIGHT)
        
        # 球体
        ball = Circle(radius=0.5, color=BALL_COLOR, fill_color=BALL_COLOR, fill_opacity=1)
        ball.move_to(LEFT * 4 + DOWN * 2.5)  # 初始位置
        
        # 标题
        title = Text("牛顿第三定律：作用力与反作用力定律", font_size=36, color=TEXT_COLOR)
        title.to_edge(UP)
        
        # 添加地面、墙壁、标题和球体
        self.play(FadeIn(ground), FadeIn(wall), Write(title), FadeIn(ball))
        self.wait(1)
        
        # 球体移动
        self.play(ball.animate.shift(RIGHT * 7), run_time=RUN_TIME, rate_func=rush_into)
        self.wait(0.5)
        
        # 作用力箭头
        force_arrow = Arrow(start=ball.get_center(), end=ball.get_center() + RIGHT, color=FORCE_COLOR, buff=0)
        force_label = Text("作用力", font_size=24, color=FORCE_COLOR).next_to(force_arrow, UP)
        
        # 反作用力箭头
        reaction_arrow = Arrow(start=wall.get_center() + LEFT * 0.5, end=wall.get_center() + LEFT * 1.5, color=REACTION_COLOR, buff=0)
        reaction_label = Text("反作用力", font_size=24, color=REACTION_COLOR).next_to(reaction_arrow, UP)
        
        # 公式
        formula = MathTex(r"F_{\text{作用}} = - F_{\text{反作用}}", font_size=32)
        formula.to_edge(DOWN)
        
        # 碰撞场景
        self.play(Create(force_arrow), Write(force_label))
        self.play(Create(reaction_arrow), Write(reaction_label))
        self.play(Write(formula))
        self.wait(1)
        
        # 球体反弹
        self.play(ball.animate.shift(LEFT * 3), run_time=RUN_TIME, rate_func=smooth)
        self.play(FadeOut(force_arrow), FadeOut(force_label), FadeOut(reaction_arrow), FadeOut(reaction_label))
        self.wait(0.5)
        
        # 总结文字
        summary_text = Text("作用力与反作用力大小相等，方向相反", font_size=28, color=TEXT_COLOR)
        self.play(Write(summary_text))
        self.wait(2)
        
        # 结束场景
        self.play(FadeOut(VGroup(*self.mobjects)))