from manim import *
import numpy as np

class NewtonThirdLawScene(Scene):
    def construct(self):
        # 设置背景和地面
        background = Rectangle(width=FRAME_WIDTH, height=FRAME_HEIGHT, color=BLUE, fill_opacity=1)
        background.set_color_by_gradient(BLUE, DARK_BLUE)
        ground = Rectangle(width=FRAME_WIDTH, height=0.5, color=GRAY, fill_opacity=1)
        ground.to_edge(DOWN)
        stars = VGroup(*[Dot(point=np.random.uniform([-FRAME_WIDTH/2, FRAME_WIDTH/2], [-FRAME_HEIGHT/2, FRAME_HEIGHT/2]), 
                            color=WHITE, radius=0.02) for _ in range(50)])
        
        self.add(background, stars, ground)
        
        # 创建物体
        cube_A = Square(side_length=1, color=RED, fill_opacity=0.8)
        cube_A.move_to(LEFT * 2 + DOWN * 0.5)
        ball_B = Circle(radius=0.6, color=GREEN, fill_opacity=0.8)
        ball_B.move_to(RIGHT * 2 + DOWN * 0.5)
        
        self.play(FadeIn(cube_A), FadeIn(ball_B))
        self.wait(1)
        
        # 作用力和反作用力箭头
        action_arrow = Arrow(start=cube_A.get_center(), end=cube_A.get_center() + RIGHT, color=RED)
        reaction_arrow = Arrow(start=ball_B.get_center(), end=ball_B.get_center() + LEFT, color=GREEN)
        
        # Step 2: 物体A开始推动物体B
        self.play(cube_A.animate.shift(RIGHT * 1), Create(action_arrow), run_time=2)
        self.wait(1)
        
        # Step 3: 物体B反应并出现反作用力箭头
        self.play(ball_B.animate.shift(RIGHT * 1), Create(reaction_arrow), run_time=2)
        self.wait(1)
        
        # Step 4: 展示牛顿第三定律公式
        formula = MathTex(r"F_{\text{作用}} = -F_{\text{反作用}}", font_size=48)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(1)
        
        # Step 5: 动态文本解释
        explanation_text = Text("每一个作用力都有一个大小相等、方向相反的反作用力。", font_size=32, color=WHITE)
        explanation_text.to_edge(DOWN)
        self.play(Write(explanation_text))
        self.wait(2)
        
        # Step 6: 结束场景，显示标题
        title = Text("牛顿第三定律：力量的平衡", font_size=36, color=YELLOW)
        title.move_to(ORIGIN)
        self.play(FadeOut(VGroup(cube_A, ball_B, action_arrow, reaction_arrow, formula, explanation_text)), FadeIn(title))
        self.wait(2)
        
        # 收尾
        self.play(FadeOut(title, background, stars, ground))