from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup()
    profile = InlineKeyboardButton("👤 Моя анкета", callback_data="my_profile")
    search = InlineKeyboardButton("🔍 Смотреть анкеты", callback_data="search")
    reciprocal = InlineKeyboardButton("Взаимные лайки", callback_data="reciprocal")
    likes = InlineKeyboardButton("Лайки", callback_data="likes")
    keyboard.add(profile, search, reciprocal, likes)
    return keyboard

def get_back_to_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("◀️ В главное меню", callback_data="main_menu"))
    return keyboard