from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("👤 Моя анкета", callback_data="my_profile"))
    keyboard.add(InlineKeyboardButton("🔍 Смотреть анкеты", callback_data="search"))
    keyboard.add(InlineKeyboardButton("Взаимные лайки", callback_data="reciprocal"))
    keyboard.add(InlineKeyboardButton("Лайки", callback_data="likes"))
    return keyboard

def get_back_to_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("◀️ В главное меню", callback_data="main_menu"))
    return keyboard