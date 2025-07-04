from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Code Plagiarism Detector"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./plagiarism_detector.db"
    
    # AI/ML Settings
    OPENAI_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    
    # Code analysis settings
    MAX_FILE_SIZE: int = 1024 * 1024  # 1MB
    SUPPORTED_LANGUAGES: List[str] = ["python", "javascript", "java", "cpp", "c", "csharp"]
    
    # Similarity threshold
    SIMILARITY_THRESHOLD: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings()
