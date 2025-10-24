import os
from dotenv import load_dotenv

load_dotenv()

STRCNX = os.getenv("STRCNX")
ENGINE = os.getenv("ENGINE")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT") or 8080)
DEBUG = int(os.getenv("DEBUG") or 0)
ENV = os.getenv("ENV")


origins_env = os.getenv("ALLOWED_ORIGINS", "")
ORIGINS = [origin.strip() for origin in origins_env.split(",") if origin.strip()]

SECRET_KEY = os.getenv("SECRET_KEY", default="1234").encode("utf-8")

SQLALCHEMY_DATABSE_URI = STRCNX