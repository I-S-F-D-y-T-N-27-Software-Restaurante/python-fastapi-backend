from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import STRCNX

if STRCNX is None:
    raise ValueError("Database connection is not configured.")

engine = create_engine(STRCNX, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=True)
