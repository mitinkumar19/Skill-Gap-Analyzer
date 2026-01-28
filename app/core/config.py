import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Generative Skill Gap Analyzer"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # AI/ML Config
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # Fast and efficient
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", 6333))
    
    # LLM Config
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Paths
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

settings = Settings()
