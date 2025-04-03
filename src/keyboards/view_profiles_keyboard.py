from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_date_keyboard(user):
    markup = InlineKeyboardMarkup()
    like_btn = InlineKeyboardButton("❤️ Лайк", callback_data=f"like_{user}")
    dislike_btn = InlineKeyboardButton("👎 Дизлайк", callback_data=f"dislike_{user}")
    markup.add(like_btn, dislike_btn)
    return markup