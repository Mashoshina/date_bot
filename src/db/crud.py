from sqlalchemy.orm import Session
from . import models

def create_user(db: Session, telegram_id: int, user_data: dict):
    db_user = models.User(
        telegram_id=telegram_id,
        name=user_data['name'],
        gender=user_data['gender'],
        interested_in=user_data['interested_in'],
        age=user_data['age'],
        description=user_data['description']
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()