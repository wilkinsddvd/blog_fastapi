from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings

# SQLAlchemy engine and session
engine = create_engine(settings.DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency generator for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()