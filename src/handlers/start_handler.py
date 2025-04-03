from src.keyboards.start_keyboard import generate_start_keyboard

def register_start_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(
            message.chat.id, 
            "Добро пожаловать в бот для знакомств Shadow Love!",
            reply_markup=generate_start_keyboard()
        )