from telebot import TeleBot
from src.db.create_db import init_db
from src.handlers.start_handler import register_start_handlers
from src.handlers.registration_handler import register_registration_handler
from src.handlers.profile_handler import register_profile_handler
from src.handlers.main_handler import register_main_handler
from src.handlers.view_profiles_handler import register_dating_handlers
from src.handlers.mutual_handler import register_mutual_handler
from config import BOT_TOKEN

def create_bot():
    bot = TeleBot(BOT_TOKEN)
    register_start_handlers(bot)
    register_registration_handler(bot)
    register_main_handler(bot)
    register_profile_handler(bot)
    register_dating_handlers(bot)
    register_mutual_handler(bot)
    return bot

if __name__ == "__main__":
    init_db()
    bot = create_bot()
    bot.polling(none_stop=True)