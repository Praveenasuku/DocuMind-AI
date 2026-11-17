
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings


# 1. Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)


# 2. Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# 3. Create base class
class Base(DeclarativeBase):
    pass


# 4. Database dependency
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
