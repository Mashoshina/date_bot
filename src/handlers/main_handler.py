from src.keyboards.main_keyboard import get_main_keyboard

def register_main_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data in ["main", "back"])
    def show_main_menu(call):
        bot.edit_message_text(
            "Главное меню:", 
            call.message.chat.id, 
            call.message.message_id,
            reply_markup=get_main_keyboard()
        )