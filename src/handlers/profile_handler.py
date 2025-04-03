from src.keyboards.profile_keyboard import generate_profile_keyboard
from src.db import crud
from src.db.database import get_db

def register_profile_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['my_profile'])
    def show_profile(call):
        db = next(get_db())
        user = crud.get_user(db, call.from_user.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        if user:
            profile = f"""
                Ваша анкета:
                Имя: {user.name}
                Город: {user.city}
                Пол: {user.gender}
                Возраст: {user.age}
                О себе: {user.description}
            """
        with open(user.photo_path, 'rb') as photo_file:
            bot.send_photo(
                call.message.chat.id, 
                photo_file, 
                caption=profile, 
                reply_markup=generate_profile_keyboard()
            )