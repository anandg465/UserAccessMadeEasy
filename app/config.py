from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ORACLE_API_BASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
