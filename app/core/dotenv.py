import os
from enum import Enum

from dotenv import load_dotenv


class ConfigKey(str, Enum):
    APP_TITLE = "APP_TITLE"
    HOST = "HOST"
    PORT = "PORT"
    DEBUG = "DEBUG"
    DATABASE_URL = "DATABASE_URL"
    SECRET_KEY = "SECRET_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES = "ACCESS_TOKEN_EXPIRE_MINUTES"
    ALLOWED_ORIGINS = "ALLOWED_ORIGINS"


def dotenv_setup():
    load_dotenv()
    return {
        ConfigKey.APP_TITLE: os.getenv("APP_TITLE") or "backend",
        ConfigKey.HOST: os.getenv("HOST") or "0.0.0.0",
        ConfigKey.PORT: int(os.getenv("PORT") or 8000),
        ConfigKey.DEBUG: os.getenv("DEBUG") == "True",
        ConfigKey.DATABASE_URL: os.getenv("DATABASE_URL") or "uri",
        ConfigKey.SECRET_KEY: os.getenv("SECRET_KEY") or "your-secret-key",
        ConfigKey.ACCESS_TOKEN_EXPIRE_MINUTES: int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60
        ),
        ConfigKey.ALLOWED_ORIGINS: os.getenv("ALLOWED_ORIGINS")
        or "http://localhost,http://localhost:3000",
    }
