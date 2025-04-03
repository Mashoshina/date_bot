from src.db.database import engine, Base
from src.core.logging import logger

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    logger.info("Database created successfully!")