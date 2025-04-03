from sqlalchemy import and_, exists, text
from sqlalchemy.orm import Session
from src.models.user import User
from src.models.reaction import Reaction
from src.core.logging import logger

def check_user_exists(db: Session, telegram_id: int) -> bool:
    return db.query(User).filter(User.telegram_id == telegram_id).first() is not None

def create_user(db: Session, telegram_id: int, user_data: dict):
    db_user = User(
        telegram_id=telegram_id,
        name=user_data['name'],
        gender=user_data['gender'],
        interested_in=user_data['interested_in'],
        age=user_data['age'],
        city=user_data['city'],
        photo_path=user_data['photo_path'],
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
        db_user.city = user_data['city']
        db_user.photo_path = user_data['photo_path']
        db_user.description = user_data['description']
        db.commit()
        db.refresh(db_user)
    return db_user

def get_user(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def get_next_user(db, current_user_id):
    current_user = db.query(User).get(current_user_id)

    if not current_user:
        return None

    viewed_users = db.query(Reaction.target_user_id).filter(
        Reaction.user_id == current_user_id
    ).all()

    viewed_ids = [user[0] for user in viewed_users] if viewed_users else []

    query = db.query(User).filter(
        User.id != current_user_id,
        User.id.notin_(viewed_ids),
        # User.interested_in == current_user.gender,
        # User.gender == current_user.interested_in
    )

    if current_user.city:
        query = query.filter(User.city == current_user.city)

    return query.first()

def upsert_reaction(db, user_id, target_user_id, is_like):
    reaction = db.query(Reaction).filter(
        Reaction.user_id == user_id,
        Reaction.target_user_id == target_user_id
    ).first()
    
    if reaction:
        reaction.is_like = is_like
    else:
        reaction = Reaction(
            user_id=user_id,
            target_user_id=target_user_id,
            is_like=is_like
        )
        db.add(reaction)
    
    db.commit()
    return reaction

def get_mutual_likes(db, current_user_id):
    liked_by_current = db.query(Reaction.target_user_id).filter(
        Reaction.user_id == current_user_id,
        Reaction.is_like == 1
    ).all()
    
    if not liked_by_current:
        return []

    liked_users_ids = [user[0] for user in liked_by_current]

    mutual_users = db.query(User).join(
        Reaction,
        and_(
            Reaction.user_id == User.id,
            Reaction.target_user_id == current_user_id,
            Reaction.is_like == 1
        )
    ).filter(
        User.id.in_(liked_users_ids)
    ).all()

    return mutual_users