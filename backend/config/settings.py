import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LLM_PROVIDER: str = "mock" # options: "mock", "openai", "vertex"
    LLM_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
