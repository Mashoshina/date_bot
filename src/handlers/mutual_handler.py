from src.core.logging import logger
from src.db import crud
from src.db.database import get_db
from src.keyboards.main_keyboard import get_main_keyboard
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def register_mutual_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "mutual_likes")
    def handle_mutual_likes(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        try:
            db = next(get_db())
            user = crud.get_user(db, call.from_user.id)
            mutual_likes = crud.get_mutual_likes(db, user.id)

            if not mutual_likes:
                return bot.send_message(
                    call.message.chat.id, 
                    "😔 У вас пока нет взаимных симпатий", 
                    reply_markup=get_main_keyboard()
                )

            bot_data = {
                'mutual_likes': mutual_likes,
                'current_index': 0,
                'chat_id': call.message.chat.id
            }
            bot.current_user_data = bot_data
            
            send_user_with_navigation(bot, bot_data)

        except Exception as e:
            logger.error(f"Error: {e}")
            bot.send_message(call.message.chat.id, "⚠️ Произошла ошибка при поиске симпатий")


def send_user_with_navigation(bot, bot_data):
    mutual_likes = bot_data['mutual_likes']
    current_index = bot_data['current_index']
    chat_id = bot_data['chat_id']

    if current_index >= len(mutual_likes):
        bot.send_message(chat_id, "Вы просмотрели всех пользователей", 
                        reply_markup=get_main_keyboard())
        return

    liked_user = mutual_likes[current_index]
    send_user_profile(bot, chat_id, liked_user, current_index < len(mutual_likes) - 1)


def send_user_profile(bot, chat_id, user, has_next=True):
    if not user:
        bot.send_message(chat_id, "Информация о пользователе недоступна")
        return

    profile_text = format_user_profile(user)
    
    markup = InlineKeyboardMarkup()
    if has_next:
        markup.add(InlineKeyboardButton("Следующий", callback_data="next_mutual_user"))
    else:
        markup = get_main_keyboard()

    with open(user.photo_path, 'rb') as photo:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=profile_text,
            reply_markup=markup,
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data == "next_mutual_user")
    def handle_next_user(call):
        try:
            if not hasattr(bot, 'current_user_data'):
                return bot.send_message(call.message.chat.id, "Сессия просмотра завершена", 
                                    reply_markup=get_main_keyboard())

            bot_data = bot.current_user_data
            bot_data['current_index'] += 1
            
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass
                
            send_user_with_navigation(bot, bot_data)
            
        except Exception as e:
            logger.error(f"Error in next user handler: {e}")
            bot.send_message(call.message.chat.id, "⚠️ Произошла ошибка")


def format_user_profile(user):
    return f"""
Взаимная симпатия:

    Имя: {user.name}
    Город: {user.city}
    Пол: {user.gender}
    Возраст: {user.age}
    О себе: {user.description}
    Ссылка: @{user.telegram_name}
"""