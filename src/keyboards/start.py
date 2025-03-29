from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def generate_start_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    create_profile = KeyboardButton("Создать анкету")
    markup.add(create_profile)
    return markup