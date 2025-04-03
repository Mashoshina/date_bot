from src.db import crud
from src.db.database import get_db
from src.keyboards.view_profiles_keyboard import generate_date_keyboard
from src.core.logging import logger

def register_dating_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ['search'])
    def start_dating(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        db = next(get_db())
        current_user = crud.get_user(db, call.from_user.id)
        next_user = crud.get_next_user(db, current_user.id)

        if not next_user:
            return bot.send_message(call.message.chat.id, "Анкеты закончились! 🎉")
        
        send_profile(bot, call.message.chat.id, next_user)

    def send_profile(bot, chat_id, user):
        profile = f"""
            Имя: {user.name}
            Город: {user.city}
            Пол: {user.gender}
            Возраст: {user.age}
            О себе: {user.description}
        """
        bot.send_message(
            chat_id,
            profile,
            reply_markup=generate_date_keyboard(user.telegram_id)
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith(('like_', 'dislike_')))
    def handle_reaction(call):
        try:
            action, target_telegram_id = call.data.split('_')
            current_telegram_id = call.from_user.id
            is_like = (action == 'like')

            db = next(get_db())

            current_user = crud.get_user(db, current_telegram_id)
            target_user = crud.get_user(db, target_telegram_id)
            
            crud.upsert_reaction(
                db,
                user_id=current_user.id,
                target_user_id=target_user.id,
                is_like=is_like
            )
            
            next_user = crud.get_next_user(db, current_user.id)
            if next_user:
                send_profile(bot, call.message.chat.id, next_user)
            else:
                bot.send_message(call.message.chat.id, "Вы просмотрели всех! 🎉")
            
            bot.answer_callback_query(call.id, "👍 Сохранено!")
        except Exception as e:
            logger.error(f"Handle_reaction: {e}")
            bot.answer_callback_query(call.id, "⚠️ Ошибка! Попробуйте позже")