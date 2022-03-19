import time

import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('5131645257:AAHyEawmAqAe-kDRi8l5GLZXk2ZAEiCTsFo')

@bot.message_handler(commands=['start'])
def start(message):
    t = time.localtime()
    print(message.text)
    user = (message.from_user.id, message.chat.username, message.text[7:], time.strftime("%H.%M", t))
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?);", user)
    conn.commit()
    bot.send_message(message.chat.id, 'Исәнме дустым, {user}!'.format(user = message.chat.username))
    conn.close()
    phone(message)
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, 'Телефон номерын жибәрергә рөхсәт бирегез', reply_markup=keyboard)

@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        userid = message.from_user.id
        bot.send_message(message.chat.id, 'Әфәрин', reply_markup = types.ReplyKeyboardRemove())
        s = str(message.contact.phone_number)
        s = s.replace('+', '')
        if s[:1] == '7':
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute("select * from users where userid = {user_id}" .format(user_id = userid))
            rest = cur.fetchone()
            rest=rest[2]
            cur.execute("DELETE FROM users WHERE userid = {user_id}" .format(user_id = userid))
            conn.commit()
            conn.close()
            post(message, rest)

def post(message, rest):
    txt = 'https://t.me/' + rest
    print(txt)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text = 'Telegram', url=txt)
    markup.add(button1)
    bot.send_message(message.chat.id, "Түбәндәге ссылкага басыгыз", reply_markup = markup)

if __name__ == "__main__":
    print("Бот запущен")
    bot.polling(none_stop=True, interval=0)

#pyTelegramBotAPI 4.1.1