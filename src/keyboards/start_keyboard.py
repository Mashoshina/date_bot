from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_start_keyboard():
    markup = InlineKeyboardMarkup()
    create_profile = InlineKeyboardButton("Создать анкету", callback_data="start_reg")
    markup.add(create_profile)
    return markup