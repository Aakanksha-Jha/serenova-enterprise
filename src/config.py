import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Config:
    # This trick attempts to check Streamlit Secrets first, falling back to os.getenv
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    LLM_MODEL = st.secrets.get("LLM_MODEL", os.getenv("LLM_MODEL", "qwen/qwen3-32b"))
    
    HINDSIGHT_API_KEY = st.secrets.get("HINDSIGHT_API_KEY", os.getenv("HINDSIGHT_API_KEY"))
    HINDSIGHT_URL = st.secrets.get(
        "HINDSIGHT_VECTOR_DB_URL", 
        os.getenv("HINDSIGHT_VECTOR_DB_URL", "https://ui.hindsight.vectorize.io/api/v1")
    )

    @classmethod
    def validate(cls):
        # Allow running even if Hindsight keys aren't fully configured yet for local testing
        if not cls.GROQ_API_KEY:
            raise ValueError("Missing required environment variable: GROQ_API_KEY")