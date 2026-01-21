from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # MongoDB Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "intern_onboarding"
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    
    # Application Configuration
    app_name: str = "Intern Onboarding API"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
