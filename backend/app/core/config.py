from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SensaBook API"
    API_VERSION: str = "v1"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/sensabook"

    class Config:
        env_file = ".env"

settings = Settings()