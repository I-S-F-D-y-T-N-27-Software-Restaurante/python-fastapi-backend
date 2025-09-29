import os

from dotenv import load_dotenv

load_dotenv()

STRCNX = os.getenv("STRCNX")

ENGINE = os.getenv("ENGINE")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT") or 8080)
USERDB = os.getenv("USERDB")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

# STRCNX = f'{ENGINE}://{USERDB}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

SQLALCHEMY_DATABSE_URI = STRCNX
