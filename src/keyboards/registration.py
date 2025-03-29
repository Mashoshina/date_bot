from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def generate_gender_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    btn_male = KeyboardButton("Мужчина")
    btn_female = KeyboardButton("Женщина")
    markup.add(btn_male, btn_female)
    return markup

def generate_interested_in_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    btn_male = KeyboardButton("Мужчины")
    btn_female = KeyboardButton("Женщины")
    markup.add(btn_male, btn_female)
    return markup

def generate_update_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    btn_update = KeyboardButton("Да, обновить анкету")
    btn_continue = KeyboardButton("Нет, оставить как есть")
    markup.add(btn_update, btn_continue)
    return markup