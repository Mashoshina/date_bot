from src.db import crud
from src.db.database import get_db

def register_profile_handler(bot):
    @bot.message_handler(func=lambda msg: msg.text in ["Создать анкету"])
    def show_profile(message):
        chat_id = message.chat.id
        db = next(get_db())
        user = crud.get_user(db, chat_id)

        if user:
            profile = f"""
                Ваша анкета:
                Имя: {user.name}
                Пол: {user.gender}
                Ищу: {user.interested_in}
                Возраст: {user.age}
                О себе: {user.description}
            """
            bot.send_message(chat_id, profile)
        else:
            bot.send_message(chat_id, "У вас нет анкеты. Нажмите 'Создать анкету'")