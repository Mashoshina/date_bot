from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.db.database import Base

class Reaction(Base):
    __tablename__ = 'reactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    target_user_id = Column(Integer, ForeignKey('users.id'))
    is_like = Column(Boolean)

    user = relationship("User", foreign_keys=[user_id], back_populates="reactions_given")
    target_user = relationship("User", foreign_keys=[target_user_id], back_populates="reactions_received")