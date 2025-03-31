from src.keyboards.profile_keyboard import generate_profile_keyboard
from src.db import crud
from src.db.database import get_db

def register_profile_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "my_profile")
    def show_profile(call):
        db = next(get_db())
        user = crud.get_user(db, call.message.chat.id)

        if user:
            profile = f"""
                Ваша анкета:
                Имя: {user.name}
                Пол: {user.gender}
                Возраст: {user.age}
                О себе: {user.description}
            """
            bot.edit_message_text(
                profile, 
                call.message.chat.id,
                call.message.message_id,
                reply_markup=generate_profile_keyboard()
            )