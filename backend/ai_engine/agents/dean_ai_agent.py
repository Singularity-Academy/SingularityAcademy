import os
import requests  # 新增导入
import json      # 新增导入
from langchain_community.llms import OpenAI
from langchain.chains import ConversationChain
from typing import List, Dict

class DeanAIAgent:
    def __init__(self, user_id: int, material: str):
        self.user_id = user_id
        self.material = material
        self.llm = OpenAI(model_name='gpt-4', temperature=0.7)
        self.conversation = ConversationChain(llm=self.llm)
        self.chunks = []
        self.course_material = ""

    def fetch_uploaded_files(self) -> str:
        # 检测文件名是否以用户id+'$'开头
        if not self.material.startswith(str(self.user_id) + "$"):
            return ""
        # 检测文件是否位于../materials中
        if not os.path.abspath(os.path.join('../materials', self.material)).startswith(os.path.abspath('../materials')):
            return ""
        # 检测文件是否存在
        if not os.path.isfile(os.path.join('../materials', self.material)):
            return ""
        # 从文件夹中获取用户请求的材料
        with open(os.path.join('../materials', self.material)) as material:
            return material.read()


    def generate_study_plan(self) -> List[Dict]:
        # 获取课程材料
        self.course_material = self.fetch_uploaded_files()

        # 构建提示词
        prompt = f"""
你是一位 AI 教学规划助手。根据以下的课程材料，为学生生成一份综合的学习计划，格式为 markdown，包括图片、链接等任何与该主题相关的内容。

课程材料：
{self.course_material}

请将学习计划拆分成较小的部分，每次在对话中可以逐一分享。每个部分应包含：
1. 用于执行 Manim 的 Python 脚本 (`manim_script`)
2. 要对学生说的话 (`message`)
3. 文字笔记 (`notes`)
请以 JSON 格式返回一个包含 `manim_script`、`message` 和 `notes` 键的对象列表。
"""

        response = self.llm(prompt)
        # 将响应解析为 JSON 对象列表
        try:
            chunks = json.loads(response)
        except json.JSONDecodeError:
            # 如果解析失败，返回空列表
            chunks = []
        return chunks

    def get_next_chunk(self) -> Dict:
        if self.chunks:
            return self.chunks.pop(0)
        else:
            return {"message": "学习计划已完成。你还有什么问题吗？"}

    def reset(self):
        # 生成新的学习计划并重置 chunks
        self.chunks = self.generate_study_plan()

    def handle_user_input(self, user_input: str) -> Dict:
        # 对话逻辑
        if '开始学习计划' in user_input:
            self.reset()
            return self.get_next_chunk()
        elif '下一步' in user_input:
            return self.get_next_chunk()
        else:
            # 继续对话
            response = self.conversation.predict(input=user_input)
            return {"message": response} 