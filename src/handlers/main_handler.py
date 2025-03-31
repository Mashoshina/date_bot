from src.keyboards.main_keyboard import get_main_keyboard

def register_main_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ["main", "back"])
    def show_main_menu(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id, 
            "Выберите одну из опций:", 
            reply_markup=get_main_keyboard()
        )