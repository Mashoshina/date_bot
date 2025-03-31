from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_gender_keyboard():
    markup = InlineKeyboardMarkup()
    btn_male = InlineKeyboardButton("Мужчина", callback_data="male_gender")
    btn_female = InlineKeyboardButton("Женщина", callback_data="female_gender")
    markup.add(btn_male, btn_female)
    return markup

def generate_interested_in_keyboard():
    markup = InlineKeyboardMarkup()
    btn_male = InlineKeyboardButton("Мужчины", callback_data="male_inter")
    btn_female = InlineKeyboardButton("Женщины", callback_data="female_inter")
    markup.add(btn_male, btn_female)
    return markup

def generate_update_keyboard():
    markup = InlineKeyboardMarkup()
    btn_update = InlineKeyboardButton("Да, обновить анкету", callback_data="confirm_yes")
    btn_continue = InlineKeyboardButton("Нет, оставить как есть", callback_data="main")
    markup.add(btn_update, btn_continue)
    return markup