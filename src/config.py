import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3-32b")
    
    HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
    # Base endpoint URL for Hindsight cloud instances
    HINDSIGHT_URL = os.getenv("HINDSIGHT_VECTOR_DB_URL", "https://ui.hindsight.vectorize.io/api/v1")

    @classmethod
    def validate(cls):
        missing = [k for k, v in cls.__dict__.items() if not k.startswith("__") and v is None]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")