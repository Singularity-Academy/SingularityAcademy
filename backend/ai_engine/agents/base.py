from abc import ABC, abstractmethod
from typing import Any, Dict
from langchain.schema import BaseMessage

class BaseAgent(ABC):
    @abstractmethod
    async def process(self, input_data: Any) -> Dict:
        """Process input data and return response"""
        pass
    
    @abstractmethod
    async def generate_response(self, context: Dict) -> BaseMessage:
        """Generate response based on context"""
        pass 