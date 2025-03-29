from src.keyboards.start import generate_start_keyboard

def register_start_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_message(message):
        text = "Добро пожаловать в бот для знакомств Shadow Love!"
        markup = generate_start_keyboard()
        bot.send_message(message.chat.id, text, reply_markup=markup)