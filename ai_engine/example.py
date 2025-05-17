import asyncio
from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import HumanMessage

# 1. Create custom async callback handler
class MyAsyncCallbackHandler(AsyncCallbackHandler):
    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Handle new streaming token asynchronously"""
        print(f"{token}", end="", flush=True)

# 2. Create async chat completion function
async def stream_response():
    llm = ChatOpenAI(
        api_key="sk-deepseekapikeybutnotforreal",
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        streaming=True,
        temperature=0,
        callbacks=[MyAsyncCallbackHandler()]
    )
    
    response = await llm.agenerate([[HumanMessage(content="Tell me a joke")]])
    return response

# 3. Run the async event loop
async def main():
    print("Streaming response:")
    await stream_response()
    print("\n\nStreaming complete!")

if __name__ == "__main__":
    asyncio.run(main())