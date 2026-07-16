from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency provider that yields a database session per request 
    and guarantees closure after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()