import os

from dotenv import load_dotenv

load_dotenv()

STRCNX = os.getenv("STRCNX")
# STRCNX = f'{ENGINE}://{USERDB}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

ENGINE = os.getenv("ENGINE")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT") or 8080)
ENV = os.getenv("ENV")


SQLALCHEMY_DATABSE_URI = STRCNX
