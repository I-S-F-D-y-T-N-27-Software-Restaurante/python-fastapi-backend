from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DEBUG, STRCNX

if STRCNX is None:
    raise ValueError("Database connection is not configured.")

is_verbose = DEBUG == 1
engine = create_engine(STRCNX, echo=is_verbose)

SessionLocal = sessionmaker(bind=engine, autoflush=True)
