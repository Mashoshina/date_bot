from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_profile_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Редактировать анкету", callback_data="repeat_reg"))
    keyboard.add(InlineKeyboardButton("На главную", callback_data="back"))
    return keyboard