from sqlalchemy.orm import Session
from src.models.user import User

def check_user_exists(db: Session, telegram_id: int) -> bool:
    return db.query(User).filter(User.telegram_id == telegram_id).first() is not None

def create_user(db: Session, telegram_id: int, user_data: dict):
    db_user = User(
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

def update_user(db: Session, telegram_id: int, user_data: dict):
    db_user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if db_user:
        db_user.name = user_data['name']
        db_user.gender = user_data['gender']
        db_user.interested_in = user_data['interested_in']
        db_user.age = user_data['age']
        db_user.description = user_data['description']
        db.commit()
        db.refresh(db_user)
    return db_user

def get_user(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()