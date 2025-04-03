from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.logging import logger

SQLALCHEMY_DATABASE_URL = "sqlite:///src/db/app.db"

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=False
    )
    logger.info("Database engine successfully created")
except Exception as e:
    logger.error(f"Error createing database engine: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("Session factory configured")

Base = declarative_base()
logger.info("Base declarative class created")

def get_db():
    db = SessionLocal()
    try:
        logger.debug("Database session started")
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
    finally:
        db.close()
        logger.debug("Database session closed")