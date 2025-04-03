from src.keyboards.registration_keyboard import generate_gender_keyboard
from src.keyboards.registration_keyboard import generate_interested_in_keyboard
from src.keyboards.registration_keyboard import generate_update_keyboard
from src.keyboards.main_keyboard import get_main_keyboard
from src.models.user import User
from src.db import crud
from src.db.database import get_db
from src.core.logging import logger

user_data = {}

def register_registration_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "start_reg")
    def start_registration(call):
        db = next(get_db())

        if crud.check_user_exists(db, call.from_user.id):
            bot.edit_message_text(
                "У вас уже есть анкета! Хотите обновить её?", 
                call.message.chat.id, 
                call.message.message_id,
                reply_markup=generate_update_keyboard()
            )
        else:
            user_data[call.from_user.id] = User()
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Создаём анкету! Как тебя зовут?")
            bot.register_next_step_handler(call.message,  process_name_step)

    @bot.callback_query_handler(func=lambda call: call.data in ["confirm_yes", "repeat_reg"])
    def handle_update_existing_profile(call):
        user_data[call.from_user] = User()
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Хорошо! Давай обновим твою анкету. Как тебя зовут?")
        bot.register_next_step_handler(call.message, process_name_step)

    def process_name_step(message):
        user_data[message.from_user.id].name = message.text
        if message.from_user.username:
            user_data[message.from_user.id].telegram_name = message.from_user.username
        bot.send_message(message.chat.id, "Из какого ты города?")
        bot.register_next_step_handler(message, process_city_step)

    def process_city_step(message):
        user_data[message.from_user.id].city = message.text
        bot.send_message(message.chat.id, "Отправь мне своё фото")
        bot.register_next_step_handler(message, process_photo_step)

    
    def process_photo_step(message):
        try:
            if message.content_type != 'photo':
                msg = bot.send_message(message.chat.id, "Это не фото. Пожалуйста, отправь фото.")
                return bot.register_next_step_handler(msg, process_photo_step)
            
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            photo_path = f"src/images/{message.from_user.id}.jpg"
            with open(photo_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            user_data[message.from_user.id].photo_path = photo_path
            
        except Exception as e:
            logger.error(f"Error photo step {e}")

        bot.send_message(
            message.chat.id, 
            "Какой у тебя пол?", 
            reply_markup=generate_gender_keyboard()
        )

    @bot.callback_query_handler(func=lambda call: call.data in ["male_gender", "female_gender"])
    def process_gender_step(call):
        if call.data == "male_gender":
            user_data[call.from_user.id].gender = "Мужчина"
        else:
            user_data[call.from_user.id].gender = "Женщина"

        bot.edit_message_text(
            "Какой пол тебя интересует?", 
            call.message.chat.id, 
            call.message.message_id,
            reply_markup=generate_interested_in_keyboard()
        )

    @bot.callback_query_handler(func=lambda call: call.data in ["male_inter", "female_inter"])
    def process_interested_in_step(call):
        if call.data == "male_inter":
            user_data[call.from_user.id].interested_in = "Мужчины"
        else:
            user_data[call.from_user.id].interested_in = "Женщины"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Сколько тебе лет? (Введи число):")
        bot.register_next_step_handler(call.message, process_age_step) 

    def process_age_step(message):
        try:
            age = int(message.text)
            if age < 18 or age > 80:
                bot.send_message(message.chat.id, "Пожалуйств, введите реальный возраст (18-80)")
                return bot.register_next_step_handler(message, process_age_step)
            user_data[message.from_user.id].age = age
            bot.send_message(message.chat.id, "Расскажи немного о себе:")
            bot.register_next_step_handler(message, process_description_step)
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите число ")


    
    def process_description_step(message):
        user_data[message.from_user.id].description = message.text
        db = next(get_db())
        user_dict = {
            'telegram_name': user_data[message.from_user.id].telegram_name,
            'name': user_data[message.from_user.id].name,
            'gender': user_data[message.from_user.id].gender,
            'interested_in': user_data[message.from_user.id].interested_in,
            'age': user_data[message.from_user.id].age,
            'city': user_data[message.from_user.id].city,
            'photo_path': user_data[message.from_user.id].photo_path,
            'description': user_data[message.from_user.id].description
        }

        try:
            if crud.check_user_exists(db, message.from_user.id):
                crud.update_user(db, message.from_user.id, user_dict)
                bot.send_message(
                    message.chat.id, 
                    "Анкета успешно обновлена", 
                    reply_markup=get_main_keyboard()
                )
            else:
                crud.create_user(db, message.from_user.id, user_dict)
                bot.send_message(
                    message.chat.id, 
                    "Анкета успешно создана", 
                    reply_markup=get_main_keyboard()
                )
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка, сообщите о ней @dead_boy_91")
            logger.error(f"Не получилось сохранить пользователя: {e}")
        finally:
            if message.from_user.id in user_data:
                del user_data[message.from_user.id]
            logger.debug("Registration cache cleared")