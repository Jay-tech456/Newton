from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./autolab_drive.db"
    
    # Storage
    storage_path: str = "./storage"
    frames_path: str = "./storage/frames"
    datasets_path: str = "./storage/datasets"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # CORS
    cors_origins: Union[List[str], str] = ["http://localhost:5173", "http://localhost:3000"]
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # LLM (for future integration)
    llm_provider: str = "mock"
    llm_api_key: str = ""
    llm_model: str = "gpt-4"
    
    # Research APIs (for future integration)
    arxiv_api_key: str = ""
    semantic_scholar_api_key: str = ""
    
    # Forethought Integration (stub)
    forethought_api_key: str = ""
    forethought_enabled: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
