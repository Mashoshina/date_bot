from sqlalchemy import Column, Integer, String
from src.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    gender = Column(String)
    interested_in = Column(String)
    age = Column(Integer)
    description = Column(String)