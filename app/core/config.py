from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Intent Management System"

    # Database settings
    DATABASE_URL: str = "sqlite:///./rasa_framework.db"

    class Config:
        case_sensitive = True


settings = Settings()
