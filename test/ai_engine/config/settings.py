from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str
    OPENAI_API_KEY: Optional[str] = None
    VECTOR_STORE_PATH: str = "vector_store"
    MANIM_OUTPUT_PATH: str = "media/videos"
    
    class Config:
        env_file = ".env"

settings = Settings() 