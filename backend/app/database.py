"""
TaskFlow Backend - Database Configuration
JIRA Story: TFLOW-2 - [BE] Setup FastAPI project structure

Database connection and session management using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL - file-based for simplicity
SQLALCHEMY_DATABASE_URL = "sqlite:///./taskflow.db"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Database session dependency for FastAPI.
    
    Yields:
        Session: SQLAlchemy database session
        
    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
