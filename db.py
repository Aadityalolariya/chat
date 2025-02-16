from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import CONNECTION_STRING


# Create Database Engine
engine = create_engine(CONNECTION_STRING, echo=True)

# Create a Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class for Models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
