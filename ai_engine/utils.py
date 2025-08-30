import functools
import inspect
import typing

__DEBUG__ = True  # Set this to False to disable strict type checking globally

def strict(func):
    """
    Decorator to enforce type hints at runtime. Raises ValueError on type mismatch.
    Only active if __DEBUG__ or __debug__ is True (not run with python -O).
    """
    if not (__debug__):
        return func

    sig = inspect.signature(func)
    type_hints = typing.get_type_hints(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        # Check argument types
        for name, value in bound.arguments.items():
            if name in type_hints:
                expected = type_hints[name]
                if not isinstance(value, expected) and value is not None:
                    raise ValueError(f"Argument '{name}' to {func.__name__} expected {expected}, got {type(value)}")
        result = func(*args, **kwargs)
        # Check return type
        if 'return' in type_hints and type_hints['return'] is not None:
            expected = type_hints['return']
            if not isinstance(result, expected) and result is not None:
                raise ValueError(f"Return value of {func.__name__} expected {expected}, got {type(result)}")
        return result
    return wrapper

def strip_markdown_code_blocks(response: str) -> str:
    """
    Strip markdown code block markers from LLM responses.
    
    Removes leading and trailing triple backticks (```) and optional language tags
    like 'json' that are commonly added by LLMs when generating structured responses.
    
    Args:
        response (str): The raw response from the LLM
        
    Returns:
        str: The cleaned response without markdown code block markers
    """
    response = response.strip()
    
    # Remove leading triple backticks and optional language tag
    if response.startswith("```"):
        response = response.lstrip("`").lstrip("json").strip()
    
    # Remove trailing triple backticks if present
    if response.endswith("```"):
        response = response.rstrip("```").strip()
    
    return response
