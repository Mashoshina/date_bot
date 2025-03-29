import telebot
import sqlite3

import requests.delete
import telebot.types
import telebot.types.InputMediaPhoto
import unicodedata.lookup


proc_id = 0

i = 0
i_ph = 0

a_l = 2
ankets = []
matches = []
likes = []
list = []
mass_anks = []



# def init_db():
#     conn = sqlite3.connect('shadowlove.db')
#     curs = conn.cursor()
#     curs.execute('''CREATE TABLE IF NOT EXISTS users (
#                     user_id INTEGER PRIMARY KEY,
#                     username TEXT,
#                     sex INT
#                     find_sex INT
#                     city TEXT,
#                     age TEXT,
#                     bio TEXT,
#                     photo1 TEXT DEFAULT NULL,
#                     photo2 TEXT DEFAULT NULL,
#                     photo3 TEXT DEFAULT NULL)''')
#     curs.execute('''CREATE TABLE IF NOT EXISTS likes (
#                         id INTEGER PRIMARY KEY,
#                         like INT)''')
#     curs.execute('''CREATE TABLE IF NOT EXISTS matches (
#                             id INTEGER PRIMARY KEY,
#                             match INT)''')
#     curs.execute('''CREATE TABLE IF NOT EXISTS very_bad (
#                         reported_id INTEGER PRIMARY KEY)''')
#     conn.commit()
#    conn.close()


@bot.message_handler(commands=['start'])

def start_message(message):
    us_id = message.from_user.id
    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()
    curs.execute("SELECT user_id FROM users WHERE user_id = ?", (us_id,))
    t_f = curs.fetchone()
    if t_f:
        bot.send_message(message.chat.id,
                         "Кажется, вы уже были у нас")
        show_profile(message)
    else:
        bot.send_message(message.chat.id, "Добро пожаловать в бот для знакомств Shadow Love! Если ты представитель какой-либо субкультуры или просто яркая, необычная личность, считаешь себя \"не таким, как все\" и хочешь найти похожих на себя друзей или любовь всей жизни - ты по адресу! Давай для начала создадим твою анкету.",)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        girl = telebot.types.KeyboardButton("Девушка")
        boy = telebot.types.KeyboardButton("Парень")
        keyboard.add(girl, boy)
        bot.send_message(message.chat.id, "Какого ты пола?" , reply_markup=keyboard)
        bot.register_next_step_handler(message, get_sex)

def get_sex(message):
    us_id = message.from_user.id
    username = message.from_user.first_name

    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()
    if message.text == "Девушка":
        curs.execute("""INSERT OR REPLACE INTO users (user_id, username, sex) VALUES (?, ?, ?)""", (us_id, username, 1))
    elif message.text == "Парень":
        curs.execute("""INSERT OR REPLACE INTO users (user_id, username, sex) VALUES (?, ?, ?)""",(us_id, username, 2))
    else:
        bot.send_message(message.chat.id, "Выбери вариант из кнопок ниже")
        bot.register_next_step_handler(message, get_sex)
    conn.commit()
    conn.close()

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    girl = telebot.types.KeyboardButton("Девушки")
    boy = telebot.types.KeyboardButton("Парни")
    alls = telebot.types.KeyboardButton("Все")
    keyboard.add(girl, boy, alls)
    bot.send_message(message.chat.id, "Какой пол тебе интересен?", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_find_sex)

def get_find_sex(message):
    us_id = message.from_user.id

    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()
    if message.text == "Девушки":
        curs.execute("UPDATE users SET find_sex = ? WHERE user_id = ?", (1, us_id))
    elif message.text == "Парни":
        curs.execute("UPDATE users SET find_sex = ? WHERE user_id = ?", (2, us_id))
    elif message.text == "Все":
        curs.execute("UPDATE users SET find_sex = ? WHERE user_id = ?", (3, us_id))
    else:
        bot.send_message(message.chat.id, "Выбери вариант из кнопок ниже")
        bot.register_next_step_handler(message, get_find_sex)
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "Напиши свой город")
    bot.register_next_step_handler(message, get_city)

#получить город для анкеты
def get_city(message):
    city = message.text
    us_id = message.from_user.id

    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()
    curs.execute("UPDATE users SET city = ? WHERE user_id = ?""", (city, us_id))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "Теперь укажи свой возраст")
    bot.register_next_step_handler(message, get_age)

#получить возраст для анкеты
def get_age(message):
    us_id = message.from_user.id

    try:
        age = int(message.text)

        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        curs.execute("UPDATE users SET age = ? WHERE user_id = ?", (age, us_id))
        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, "Расскажи немного о себе")
        bot.register_next_step_handler(message, get_bio)

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введи корректный возраст")
        bot.register_next_step_handler(message, get_age)

#получить раздел о себе для анкеты
def get_bio(message):
    us_id = message.from_user.id

    bio = message.text

    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()

    curs.execute("UPDATE users SET bio = ? WHERE user_id = ?", (bio, us_id))

    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "Отправь фото для анкеты или /next чтобы продолжить")
    bot.register_next_step_handler(message, get_photos)

#получить фото для анкеты
def get_photos(message):
    us_id = message.from_user.id

    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()
    curs.execute("SELECT photo1, photo2, photo3 FROM users WHERE user_id = ?", (us_id,))
    photos = curs.fetchone()
    ph1, ph2, ph3 = photos

    if message.text and message.text == "/next":
        bot.send_message(message.chat.id, "Анкета успешно создана! Проверь, всё ли верно?")
        show_profile(message)

    elif message.photo:
        photo_id = message.photo[-1].file_id
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        curs.execute("SELECT photo1, photo2, photo3 FROM users WHERE user_id = ?", (us_id,))
        photos = curs.fetchone()
        ph1, ph2, ph3 = photos

        if not ph1:
            curs.execute("UPDATE users SET photo1 = ? WHERE user_id = ? ", (photo_id, us_id))
            conn.commit()
        elif not ph2:
            curs.execute("UPDATE users SET photo2 = ? WHERE user_id = ? ", (photo_id, us_id))
            conn.commit()
        elif not ph3:
            curs.execute("UPDATE users SET photo3 = ? WHERE user_id = ? ", (photo_id, us_id))
            conn.commit()
        #else:
        #    bot.send_message(message.chat.id, "Анкета успешно создана! Проверь, всё ли верно?")
        #    show_profile(message)
        curs.execute("SELECT photo3 FROM users WHERE user_id = ?", (us_id,))
        photos = curs.fetchone()
        conn.close()
        ph3 = photos
        if not ph3:
            bot.send_message(message.chat.id, "Фото добавлено! Можешь отправить ещё или продолжить, введя команду /next")
            bot.register_next_step_handler(message, get_photos)
        else:
            bot.send_message(message.chat.id, "Анкета успешно создана! Проверь, всё ли верно?")
            show_profile(message)
    else:
        bot.send_message(message.chat.id, "Отправь фото, пожалуйста.")
        bot.register_next_step_handler(message, get_photos)

#показать профиль пользователя
def show_profile(message):
    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()
    us_id = message.from_user.id

    curs.execute("SELECT username, city, age, bio, photo1, photo2, photo3 FROM users WHERE user_id = ?", (us_id,))
    profile = curs.fetchone()
    conn.close()

    if profile:
        check_keyb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        edit = telebot.types.KeyboardButton("✏️ Редактировать анкету")
        delet = telebot.types.KeyboardButton("🗑️ Удалить анкету")
        look = telebot.types.KeyboardButton("🔍 Смотреть анкеты")
        backk = telebot.types.KeyboardButton("Назад")
        check_keyb.add(edit, delet, look, backk)

        username, city, age, bio, photo1, photo2, photo3 = profile
        caption = f"Вот ваша анкета:\n👤 {username}\n📍 Город: {city}\n🎂 Возраст: {age}\n📝 О себе: {bio}"

        media_group = []
        if photo1:
            media_group.append(InputMediaPhoto(photo1, caption=caption))
        if photo2:
            media_group.append(InputMediaPhoto(photo2))
        if photo3:
            media_group.append(InputMediaPhoto(photo3))

        bot.send_message(message.chat.id, "Вот ваша анкета", reply_markup=check_keyb)
        if media_group:
            bot.send_media_group(message.chat.id, media_group)
        else:
            bot.send_message(message.chat.id, caption)

        bot.register_next_step_handler(message, start_work)
    else:
        bot.send_message(message.chat.id, "Ошибка! Анкета не найдена.")

@bot.message_handler(content_types=['text'])

def start_work(message):
    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()
    us_id = message.from_user.id

    # Просмотр профиля юзера
    if message.text == "👤 Мой профиль":
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        show_profile(message)

    # Просмотр анкеты юзера
    elif message.text == "✏️ Редактировать анкету":
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        sex_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        girl = telebot.types.KeyboardButton("Девушка")
        boy = telebot.types.KeyboardButton("Парень")
        sex_keyboard.add(girl, boy)
        bot.send_message(message.chat.id, "Какого ты пола?", reply_markup=sex_keyboard)
        bot.register_next_step_handler(message, get_sex)

    # Удаление анкеты юзера
    elif message.text == "🗑️ Удалить анкету":
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        curs.execute("DELETE FROM users WHERE user_id = ?", (us_id,))
        bot.send_message(message.chat.id, "Твоя анкета удалена, с нетерпением ждем тебя снова")

        curs.execute("SELECT id FROM likes WHERE id = ?", (us_id,))
        del_1 = [row[0] for row in curs.fetchall()]
        if del_1:
            curs.execute("DELETE FROM likes WHERE id =?", (us_id,))
            conn.commit()

        curs.execute("SELECT id FROM likes WHERE like = ?", (us_id,))
        del_1 = [row[0] for row in curs.fetchall()]
        if del_1:
            curs.execute("DELETE FROM likes WHERE like =?", (us_id,))
            conn.commit()


        curs.execute("SELECT id FROM matches WHERE id = ?", (us_id,))
        del_1 = [row[0] for row in curs.fetchall()]
        if del_1:
            curs.execute("DELETE FROM matches WHERE id =?", (us_id,))
            conn.commit()

        curs.execute("SELECT id FROM matches WHERE match = ?", (us_id,))
        del_1 = [row[0] for row in curs.fetchall()]
        if del_1:
            curs.execute("DELETE FROM matches WHERE match =?", (us_id,))
            conn.commit()

        conn.close()

        bot.stop_bot()

    # Просмотр анкет
    elif message.text == "🔍 Смотреть анкеты":
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        curs.execute("SELECT sex, find_sex, city FROM users WHERE user_id = ?", (us_id,))
        find = curs.fetchone()
        sex, find_sex, city = find

        if find_sex != 3:
            curs.execute("SELECT user_id FROM users WHERE user_id != ? AND sex = ? AND find_sex = ? AND city = ?", (us_id, find_sex, sex, city))
            global mass_anks
            mass_anks = [row[0] for row in curs.fetchall()]
            ankets = [row[0] for row in curs.fetchall()]
        else:
            curs.execute("SELECT user_id FROM users WHERE (find_sex = ? OR find_sex = 3) AND user_id != ? AND city = ?", (sex, us_id, city))
            mass_anks = [row[0] for row in curs.fetchall()]
            ankets = [row[0] for row in curs.fetchall()]
        show_ankets(message, mass_anks)

        # Посмотреть лайки других юзеров
    elif message.text == "💖 Лайки":
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        curs.execute("SELECT id FROM likes WHERE like = ?", (us_id,))
        global likes
        mass_anks = [row[0] for row in curs.fetchall()]
        likes = [row[0] for row in curs.fetchall()]
        show_ankets(message, mass_anks)

        # Посмотреть свои метчи
    elif message.text == "💞 Метчи":
        global i
        i = 0
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        curs.execute("SELECT match FROM matches WHERE id = ?", (us_id,))
        global matches
        matches = [row[0] for row in curs.fetchall()]
        conn.close()

        show_matches(message)

        # Обработка лайков
    elif message.text == "❤️":
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        curs.execute("SELECT like FROM likes WHERE id = ?", (us_id,))
        like_n = [row[0] for row in curs.fetchall()]  # кого лайкал n
        curs.execute("SELECT like FROM likes WHERE id = ?", (proc_id,))
        like_m = [row[0] for row in curs.fetchall()]  # кого лайкал m
        if proc_id not in like_n and us_id not in like_m:
            curs.execute("""INSERT OR REPLACE INTO likes (id, like) VALUES (?, ?)""",(us_id, proc_id))
            conn.commit()
        elif proc_id not in like_n and us_id in like_m:
            curs.execute("SELECT match FROM matches WHERE id = ?", (us_id,))
            match_n = [row[0] for row in curs.fetchall()]  # метчи n
            curs.execute("SELECT match FROM matches WHERE id = ?", (proc_id,))
            match_m = [row[0] for row in curs.fetchall()]  # метчи m
            if us_id not in match_m and proc_id not in match_n:
                curs.execute("""INSERT OR REPLACE INTO matches (id, match) VALUES (?, ?)""",(us_id, proc_id))
                conn.commit()
                curs.execute("""INSERT OR REPLACE INTO matches (id, match) VALUES (?, ?)""",(proc_id, us_id))
                conn.commit()
                curs.execute("DELETE FROM likes WHERE id = ? AND like = ?", (proc_id, us_id))
        conn.close()
        show_ankets(message, mass_anks)

        # Обработка дизлайков
    elif message.text == "👎":
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        curs.execute("SELECT like FROM likes WHERE id = ?", (us_id,))
        like_n = [row[0] for row in curs.fetchall()]  # кого лайкал n
        curs.execute("SELECT like FROM likes WHERE id = ?", (proc_id,))
        like_m = [row[0] for row in curs.fetchall()]  # кого лайкал m
        if proc_id not in like_n and us_id in like_m:
            curs.execute("DELETE FROM likes WHERE id = ? AND like = ?", (proc_id, us_id))
            conn.commit()
        conn.close()

        show_ankets(message, mass_anks)

        # Обработка жалоб
    elif message.text == "🚫":
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        curs.execute("""INSERT OR REPLACE INTO very_bad (id) VALUES (?)""", (proc_id))

        curs.execute("SELECT like FROM likes WHERE id = ?", (us_id))
        like_n = [row[0] for row in curs.fetchall()]  # кого лайкал n
        curs.execute("SELECT like FROM likes WHERE id = ?", (proc_id))
        like_m = [row[0] for row in curs.fetchall()]  # кого лайкал m
        # если m лайкал n И n не лайкал m - удаляем n из лайков m
        if us_id in like_m and proc_id not in like_n:
            curs.execute("DELETE FROM likes WHERE id = ? AND WHERE like = ?", (proc_id, us_id))
            conn.commit()
        # иначе ничего делать не надо
        conn.close()


        show_ankets(message, mass_anks)

    # Обработка кнопки назад
    elif message.text == "Назад":
        conn = sqlite3.connect('\date_bot\shadowlove.db')
        curs = conn.cursor()
        us_id = message.from_user.id

        main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        my_profile = telebot.types.KeyboardButton("👤 Мой профиль")
        likes = telebot.types.KeyboardButton("💖 Лайки")
        matches_bt = telebot.types.KeyboardButton("💞 Метчи")
        look = telebot.types.KeyboardButton("🔍 Смотреть анкеты")
        main_menu.add(my_profile, likes, matches_bt, look)

        bot.send_message(message.chat.id, "Выбери действие на кнопке ниже⬇️", reply_markup=main_menu)
        bot.register_next_step_handler(message, start_work)


    # Пред мэтч
    elif message.text == "🔙":
        i -= 1
        show_matches(message)

    # След мэтч
    elif message.text == "🔜":
        i += 1
        show_matches(message)

    # Удал мэтч
    elif message.text == "❌️ Удалить мэтч":
        matches.pop(i)
        curs.execute("DELETE FROM matches WHERE id = ? AND WHERE match = ?", (us_id, proc_id))
        curs.execute("DELETE FROM matches WHERE id = ? AND WHERE match = ?", (proc_id, us_id))
        conn.commit()
        conn.close()
        show_matches(message)

    else:
        main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        my_profile = telebot.types.KeyboardButton("👤 Мой профиль")
        likes_bt = telebot.types.KeyboardButton("💖 Лайки")
        matches_bt = telebot.types.KeyboardButton("💞 Метчи")
        look = telebot.types.KeyboardButton("🔍 Смотреть анкеты")
        main_menu.add(my_profile, likes_bt, matches_bt, look)
        bot.send_message(message.chat.id, "Выбери действие на кнопке ниже⬇️", reply_markup=main_menu)
        bot.register_next_step_handler(message, start_work)



# Просмотр анкет (лайки, по городу)
def show_ankets(message, massive):
    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()
    us_id = message.from_user.id


    main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    my_profile = telebot.types.KeyboardButton("👤 Мой профиль")
    likes_bt = telebot.types.KeyboardButton("💖 Лайки")
    matches_bt = telebot.types.KeyboardButton("💞 Метчи")
    look = telebot.types.KeyboardButton("🔍 Смотреть анкеты")
    main_menu.add(my_profile, likes_bt, matches_bt, look)

    if len(massive) != 0:
        global proc_id
        proc_id = massive[0]
        massive.pop(0)
        curs.execute("SELECT username, city, age, bio, photo1, photo2, photo3 FROM users WHERE user_id = ?", (proc_id,))
        profile = curs.fetchone()
        username, city, age, bio, photo1, photo2, photo3 = profile
        caption = f"👤 {username}\n📍 Город: {city}\n🎂 Возраст: {age}\n📝 О себе: {bio}"

        media_group = []
        if photo1:
            media_group.append(InputMediaPhoto(photo1, caption=caption))
        if photo2:
            media_group.append(InputMediaPhoto(photo2))
        if photo3:
            media_group.append(InputMediaPhoto(photo3))

        like_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        like = telebot.types.KeyboardButton("❤️")
        dislike = telebot.types.KeyboardButton("👎")
        report = telebot.types.KeyboardButton("🚫")
        backk = telebot.types.KeyboardButton("Назад")
        like_menu.add(like, dislike, report, backk)

        bot.send_message(message.chat.id, "...", reply_markup=like_menu)
        if media_group:
            bot.send_media_group(message.chat.id, media_group)
            bot.register_next_step_handler(message, start_work)
        else:
            bot.send_message(message.chat.id, caption)
            bot.register_next_step_handler(message, start_work)
    else:
        bot.send_message(message.chat.id, "Ничего больше нет :(", reply_markup=main_menu)
        bot.register_next_step_handler(message, start_work)

# Просмотр метчей
def show_matches(message):
    conn = sqlite3.connect('\date_bot\shadowlove.db')
    curs = conn.cursor()
    us_id = message.from_user.id

    main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    my_profile = telebot.types.KeyboardButton("👤 Мой профиль")
    likes_bt = telebot.types.KeyboardButton("💖 Лайки")
    matches_bt = telebot.types.KeyboardButton("💞 Метчи")
    look = telebot.types.KeyboardButton("🔍 Смотреть анкеты")
    main_menu.add(my_profile, likes_bt, matches_bt, look)


    if matches and i < len(matches):

        global proc_id
        proc_id = matches[i - 1]
        curs.execute("SELECT username, city, age, bio, photo1, photo2, photo3 FROM users WHERE user_id = ?", (proc_id,))
        profile = curs.fetchone()
        username, city, age, bio, photo1, photo2, photo3 = profile
        caption = f"👤 {username}\n📍 Город: {city}\n🎂 Возраст: {age}\n📝 О себе: {bio}\n\n Написать: @{bot.get_chat(proc_id).username}"
        media_group = []
        if photo1:
            media_group.append(InputMediaPhoto(photo1, caption=caption))
        if photo2:
            media_group.append(InputMediaPhoto(photo2))
        if photo3:
            media_group.append(InputMediaPhoto(photo3))

        match_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        prev = telebot.types.KeyboardButton("️🔙")
        _next = telebot.types.KeyboardButton("🔜")
        _del = telebot.types.KeyboardButton("❌️ Удалить мэтч")
        backk = telebot.types.KeyboardButton("Назад")
        if len(matches) != 1:
            if i == 0:
                match_menu.add(_next, _del, backk)
            elif i == len(matches) - 1:
                match_menu.add(prev, _del, backk)
            else:
                match_menu.add(prev, _next, _del, backk)
        else:
            match_menu.add(_del, backk)

        bot.send_message(message.chat.id, "...", reply_markup=match_menu)
        if media_group:
            bot.send_media_group(message.chat.id, media_group)
        else:
            bot.send_message(message.chat.id, caption)
        bot.register_next_step_handler(message, start_work)
    else:
        bot.send_message(message.chat.id, "Ничего больше нет :(", reply_markup=main_menu)
        bot.register_next_step_handler(message, start_work)



if __name__ == '__main__':
    init_db()
    bot.polling(none_stop=True)