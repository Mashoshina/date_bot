from src.keyboards.registration import generate_gender_keyboard
from src.keyboards.registration import generate_interested_in_keyboard
from src.keyboards.registration import generate_update_keyboard
from src.models.user import User
from src.db import crud
from src.db.database import get_db

user_data = {}

def register_registration_handler(bot):
    @bot.message_handler(func=lambda msg: msg.text in ["Создать анкету"])
    def start_registration(message):
        chat_id = message.chat.id
        db = next(get_db())

        if crud.check_user_exists(db, chat_id):
            markup = generate_update_keyboard()
            bot.send_message(chat_id, "У вас уже есть анкета! Хотите обновить её?", reply_markup=markup)
            bot.register_next_step_handler(message, handle_existing_profile)
        else:
            user_data[chat_id] = User()
            bot.send_message(chat_id, "Создаём анкету! Как тебя зовут?")
            bot.register_next_step_handler(message, process_name_step)
    
    def handle_existing_profile(message):
        chat_id = message.chat.id
        if message.text == "Да, обновить анкету":
            user_data[chat_id] = User()
            bot.send_message(chat_id, "Хорошо! Давай обновим твою анкету. Как тебя зовут?")
            bot.register_next_step_handler(message, process_name_step)
        else:
            bot.send_message(chat_id, "Оставляем текущую анкету без изменений.")

    def process_name_step(message):
        chat_id = message.chat.id
        name = message.text
        user_data[chat_id].name = name

        markup = generate_gender_keyboard()

        bot.send_message(chat_id, "Какой у тебя пол?", reply_markup=markup)
        bot.register_next_step_handler(message, process_gender_step)

    def process_gender_step(message):
        chat_id = message.chat.id
        gender = message.text

        user_data[chat_id].gender = gender

        markup = generate_interested_in_keyboard()

        bot.send_message(chat_id, "Какой пол тебя интересует?", reply_markup=markup)
        bot.register_next_step_handler(message, process_interested_in_step)

    def process_interested_in_step(message):
        chat_id = message.chat.id
        interested_in = message.text
        
        user_data[chat_id].interested_in = interested_in
        bot.send_message(chat_id, "Сколько тебе лет? (Введи число):")
        bot.register_next_step_handler(message, process_age_step) 

    def process_age_step(message):
        chat_id = message.chat.id
        try:
            age = int(message.text)
            if age < 18 or age > 80:
                bot.send_message(chat_id, "Пожалуйств, введите реальный возраст (18-80)")
                return bot.register_next_step_handler(message, process_age_step)
            user_data[chat_id].age = age
            bot.send_message(chat_id, "Расскажи немного о себе:")
            bot.register_next_step_handler(message, process_description_step)
        except ValueError:
            bot.send_message(chat_id, "Пожалуйста, введите число ")
    
    def process_description_step(message):
        chat_id = message.chat.id
        description = message.text
        user_data[chat_id].description = description

        db = next(get_db())
        user_dict = {
            'name': user_data[chat_id].name,
            'gender': user_data[chat_id].gender,
            'interested_in': user_data[chat_id].interested_in,
            'age': user_data[chat_id].age,
            'description': user_data[chat_id].description
        }

        try:
            if crud.check_user_exists(db, chat_id):
                crud.update_user(db, chat_id, user_dict)
                bot.send_message(chat_id, "Анкета успешно обновлена")
            else:
                crud.create_user(db, chat_id, user_dict)
                bot.send_message(chat_id, "Анкета успешно создана")
        except Exception as e:
            bot.send_message(chat_id, "Произошла ошибка, сообщите о ней @dead_boy_91")
            print(f"Не получилось сохранить пользователя: {e}")
        finally:
            if chat_id in user_data:
                del user_data[chat_id]