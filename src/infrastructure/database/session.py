# src/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.core.config import get_settings

settings = get_settings()

# SQLAlchemy Engine
# echo=False - we control logging through our logging configuration instead
# This prevents SQLAlchemy from creating its own handler and ensures
# all logs go through our custom formatter
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.LOG_SQL_QUERIES,
    future=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()