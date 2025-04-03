from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    gender = Column(String)
    interested_in = Column(String)
    age = Column(Integer)
    city = Column(String)
    photo_path = Column(String)
    description = Column(String)

    reactions_given = relationship("Reaction", foreign_keys="Reaction.user_id", back_populates="user")
    reactions_received = relationship("Reaction", foreign_keys="Reaction.target_user_id", back_populates="target_user")