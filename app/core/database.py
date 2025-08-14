# Load DB URL from environment (e.g., "sqlite:///./data/sqlite.db")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .dotenv import ConfigEnum, settings

engine = create_engine(settings.get(ConfigEnum.DATABASE_URL))

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
