from pydantic_settings import BaseSettings,SettingsConfigDict
# from typing import Optional
# from pydantic import PostgresDsn
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",extra = "ignore")
    DATABASE_URL: str
    API_KEY  : str
    JWT_SECRET_KEY: str
settings = Settings()
