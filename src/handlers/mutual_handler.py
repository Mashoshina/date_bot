from src.core.logging import logger
from src.db import crud
from src.db.database import get_db

def register_mutual_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "mutual_likes")
    def handle_mutual_likes(call):
        try:
            db = next(get_db())
            user = crud.get_user(db, call.from_user.id)

            mutual_likes = crud.get_mutual_likes(db, user.id)

            if not mutual_likes:
                return bot.send_message(call.message.chat.id, "😔 У вас пока нет взаимных симпатий")

            for liked_user in mutual_likes:
                send_user_profile(bot, call.message.chat.id, liked_user)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            bot.send_message(call.message.chat.id, "⚠️ Произошла ошибка при поиске симпатий")


def send_user_profile(bot, chat_id, user):
    """Отправляет профиль пользователя с фото"""
    if not user:
        bot.send_message(chat_id, "Информация о пользователе недоступна")
        return

    profile_text = format_user_profile(user)
    
    with open(user.photo_path, 'rb') as photo:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=profile_text,
            parse_mode="Markdown"
        )


def format_user_profile(user):
    return f"""
Взаимная симпатия:

    Имя: {user.name}
    Город: {user.city}
    Пол: {user.gender}
    Возраст: {user.age}
    О себе: {user.description}
"""