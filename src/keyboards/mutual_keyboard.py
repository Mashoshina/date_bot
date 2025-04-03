from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_mutual_keyboard(user):
    markup = InlineKeyboardMarkup()
    btn_chat = InlineKeyboardButton(
        "💌 Написать сообщение",
        callback_data=f"start_chat_{user.id}"
    )
    markup.add(btn_chat)
    return markup