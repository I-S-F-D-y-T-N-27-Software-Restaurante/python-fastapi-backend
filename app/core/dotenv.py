# core/config.py
import os
from enum import Enum
from typing import Any, Dict

from dotenv import load_dotenv


class ConfigEnum(str, Enum):
    APP_TITLE = "APP_TITLE"
    HOST = "HOST"
    PORT = "PORT"
    DEBUG = "DEBUG"
    DATABASE_URL = "DATABASE_URL"
    SECRET_KEY = "SECRET_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES = "ACCESS_TOKEN_EXPIRE_MINUTES"
    ALLOWED_ORIGINS = ("ALLOWED_ORIGINS",)
    ENVIROMENT = "ENVIROMENT"


class AppConfig:
    _instance = None
    _loaded = False
    _settings: Dict[ConfigEnum, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_env()
        return cls._instance

    @classmethod
    def _load_env(cls):
        if not cls._loaded:
            load_dotenv()
            cls._settings = {
                ConfigEnum.APP_TITLE: os.getenv("APP_TITLE", "python_backend"),
                ConfigEnum.HOST: os.getenv("HOST", "0.0.0.0"),
                ConfigEnum.PORT: int(os.getenv("PORT" or 8000)),
                ConfigEnum.DEBUG: os.getenv("DEBUG", "False"),
                ConfigEnum.DATABASE_URL: os.getenv(
                    "DATABASE_URL", "sqlite:///./data/sqlite.db"
                ),
                ConfigEnum.SECRET_KEY: os.getenv("SECRET_KEY", "your-secret-key"),
                ConfigEnum.ACCESS_TOKEN_EXPIRE_MINUTES: int(
                    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES" or 60)
                ),
                ConfigEnum.ALLOWED_ORIGINS: os.getenv(
                    "ALLOWED_ORIGINS", "http://localhost,http://localhost:3000"
                ),
                ConfigEnum.ENVIROMENT: os.getenv("ENVIROMENT", "development"),
            }
            cls._loaded = True

    def get(self, key: ConfigEnum) -> Any:
        return self._settings[key]


# Singleton instance (use this everywhere)
settings = AppConfig()
