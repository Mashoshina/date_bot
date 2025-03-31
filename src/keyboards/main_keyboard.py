from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("👤 Моя анкета", callback_data="my_profile"))
    keyboard.add(InlineKeyboardButton("🔍 Поиск", callback_data="search"))
    return keyboard

def get_back_to_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("◀️ В главное меню", callback_data="main_menu"))
    return keyboard