from telebot import TeleBot
from src.db.create_db import init_db
from src.handlers.start_handler import register_start_handlers
from src.handlers.registration import register_registration_handler
from config import BOT_TOKEN

def create_bot():
    bot = TeleBot(BOT_TOKEN)
    register_start_handlers(bot)
    register_registration_handler(bot)
    return bot

if __name__ == "__main__":
    init_db()
    bot = create_bot()
    bot.polling(none_stop=True)