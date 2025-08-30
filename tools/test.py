"""
Test implementation of tool-enabled LLM using direct LangChain tools.
This demonstrates a simpler approach to tool calling using model binding.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ai_engine.apps.ai.llm import load_llm_config

# Load model configurations
CONFIG = load_llm_config()
MODEL_CONFIGS = CONFIG["models"]
DEFAULT_MODEL = CONFIG["default_model"]

# Use the default model configuration
model_config = MODEL_CONFIGS[DEFAULT_MODEL]

def get_model():
    return ChatOpenAI(
        model_name=model_config["model_id"],
        openai_api_key=model_config["api_key"],
        openai_api_base=model_config["api_base"]
    )
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate

# Define custom tools
@tool
def unknown(a: float, b: float) -> float:
    """An unknown tool that can be passed 2 integers."""
    print(f"\n[EXECUTING TOOL] unknown({a}, {b})")
    return 42

# Create tool list and lookup dictionary
tools = [unknown]
tool_map = {tool.name: tool for tool in tools}

# Initialize model with tool binding
model = get_model().bind_tools(tools)

print(model.kwargs)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful math assistant. You must use the tools provided to answer the question, even if it is simple."),
    ("human", "{input}"),
])

# Manual tool handling workflow
def run_chain_with_tools(question: str):
    # Step 1: Get initial model response
    chain = prompt | model
    response = chain.invoke({"input": question})
    
    print("\n=== INITIAL RESPONSE ===")
    print(response)
    
    # Step 2: Check for tool calls
    if not response.tool_calls:
        print("\nNo tool calls detected. Direct answer:")
        return response.content
    
    # Step 3: Execute all tool calls
    tool_messages = []
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]
        
        if tool_name in tool_map:
            # Execute the tool
            result = tool_map[tool_name].invoke(args)
            
            # Create tool message with result
            tool_messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                    name=tool_name
                )
            )
        else:
            tool_messages.append(
                ToolMessage(
                    content=f"Unknown tool: {tool_name}",
                    tool_call_id=tool_call["id"],
                    name=tool_name
                )
            )
    
    # Step 4: Send tool results back to model
    final_response = model.invoke([
        HumanMessage(content=question),
        AIMessage(content="", tool_calls=response.tool_calls),
        *tool_messages
    ])
    
    print("\n=== FINAL RESPONSE ===")
    return final_response.content

# Test the workflow
question = "What is the result of the tool call 'unknown' with parameters 6 and 7?"
result = run_chain_with_tools(question)
print(result)