from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from typing import List, Dict
import asyncio

class CoordinatorAgent:
    def __init__(self, tools: List[BaseTool], model_name: str = "gpt-4"):
        self.llm = ChatOpenAI(model_name=model_name, temperature=0)
        self.tools = tools
        self.agent = create_structured_chat_agent(self.llm, self.tools, verbose=True)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    async def process_stream(self, frame_data: Dict):
        """Process incoming video/audio stream data and coordinate responses"""
        try:
            # Analyze the frame data using the agent executor
            response = await self.agent_executor.arun(
                input=f"Analyze this frame data and coordinate appropriate responses: {frame_data}"
            )
            return response
        except Exception as e:
            print(f"Error in coordinator agent: {str(e)}")
            return None 