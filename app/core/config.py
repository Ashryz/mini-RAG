from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    APP_NAME: str 
    APP_VERSION: str 
    FILE_ALLOWED_EXTENSIONS: list[str]
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int
    MONGODB_URL: str
    MONGODB_DB_NAME: str

    class Config:
        env_file = "app/.env"
        env_file_encoding = "utf-8"



@lru_cache()
def get_settings() -> Settings:
    return Settings()
