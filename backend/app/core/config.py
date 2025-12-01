from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env

class Settings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SMS_PROVIDER_ENABLED: bool = False
    DEBUG: bool = True

    class Config:
        env_file = ".env"   # 明确可以不用，load_dotenv已自动加载

settings = Settings()