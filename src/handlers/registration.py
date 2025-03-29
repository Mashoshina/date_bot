from src.keyboards.registration import generate_gender_keyboard, generate_interested_in_keyboard

user_data = {}

def register_registration_handler(bot):
    @bot.message_handler(func=lambda msg: msg.text in ["Создать анкету"])
    def start_registration(message):
        chat_id = message.chat.id
        user_data[chat_id] = TempUser()

        bot.send_message(chat_id, "Давай для начала создадим тебе анкету. Как тебя зовут?")
        bot.register_next_step_handler(message, process_name_step)

    def process_name_step(message):
        chat_id = message.chat.id
        name = message.text
        user_data[chat_id]['name'] = name

        markup = generate_gender_keyboard()

        bot.send_message(chat_id, "Какой у тебя пол?", reply_markup=markup)
        bot.register_next_step_handler(message, process_gender_step)

    def process_gender_step(message):
        chat_id = message.chat.id
        gender = message.text

        user_data[chat_id]['gender'] = gender

        markup = generate_interested_in_keyboard()

        bot.send_message(chat_id, "Какой пол тебя интересует?", reply_markup=markup)
        bot.register_next_step_handler(message, process_interested_in_step)

    def process_interested_in_step(message):
        chat_id = message.chat.id
        interested_in = message.text
        
        user_data[chat_id]['interested_in'] = interested_in
        bot.send_message(chat_id, "Сколько тебе лет? (Введи число):")
        bot.register_next_step_handler(message, process_age_step) 

    def process_age_step(message):
        chat_id = message.chat.id
        try:
            age = int(message.text)
            if age < 18 or age > 80:
                bot.send_message(chat_id, "Пожалуйств, введите реальный возраст (18-80)")
                return bot.register_next_step_handler(message, process_age_step)
            user_data[chat_id]['age'] = age
            bot.send_message(chat_id, "Расскажи немного о себе:")
            bot.register_next_step_handler(message, process_description_step)
        except ValueError:
            bot.send_message(chat_id, "Пожалуйста, введите число ")
    
    def process_description_step(message):
        chat_id = message.chat.id
        description = message.text
        user_data[chat_id]['description'] = description

        profile = f"""
            Ваша анкета:
            Имя: {user_data[chat_id]['name']}
            Пол: {user_data[chat_id]['gender']}
            Ищу: {user_data[chat_id]['interested_in']}
            Возраст: {user_data[chat_id]['age']}
            О себе: {user_data[chat_id]['description']}
        """


        bot.send_message(chat_id, profile)