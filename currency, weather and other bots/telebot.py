import telebot
import webbrowser
import sqlite3

from telebot import types
name = None

bot = telebot.TeleBot('5795089416:AAGvY6p8jdPg4EDoHxbUEMcSR1xIWpXofDg')
API = "8595573b9165e526597c8e9ae92e4c8b"


@bot.message_handler(commands=["users"])
def users(message):
    conn = sqlite3.connect('../teleusers.db')
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), password "
                "varchar(50))")
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, "Hello, enter your name...")
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Enter your password")
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('../teleusers.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, password) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("User list", callback_data="users"))
    bot.send_message(message.chat.id, "User has been registered", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('../teleusers.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    info = ""
    for el in users:
        info += f"Name: {el[1]}, pass: {el[2]}\n"
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)


@bot.message_handler(commands=["hello"])
def hello(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Halo")
    btn2 = types.InlineKeyboardButton("Photo 🚀")
    btn3 = types.KeyboardButton("Id 🐸")
    btn4 = types.KeyboardButton("Go to website 💃")
    markup.row(btn1, btn2)
    markup.add(btn3, btn4)
    bot.send_message(message.chat.id, "Halo!", reply_markup=markup)
    # bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=["website"])
def website(message):
    webbrowser.open("https://google.com")


def on_click(message):
    if message.text == "Go to website":
        webbrowser.open("https://google.com")


@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    go_to_site_button = types.InlineKeyboardButton("Go to Google", url="https://google.com")
    delete_button = types.InlineKeyboardButton("Delete photo", callback_data="delete")
    edit_button = types.InlineKeyboardButton("Edit text", callback_data="edit")
    markup.add(go_to_site_button)
    markup.row(delete_button, edit_button)
    bot.reply_to(message, "Great photo!", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == "edit":
        bot.edit_message_text("Edit text Ololo", callback.message.chat.id, callback.message.message_id)


@bot.message_handler(content_types=["text"])
def info(message):
    if message.text.lower() == "halo":
        bot.send_message(message.chat.id, f'I tebe Halo,<b>{message.from_user.first_name}</b>!', parse_mode='html')
    elif message.text.lower() == "id":
        bot.reply_to(message, f"Your ID: {message.from_user.id}")
    elif message.text.lower() == "photo":
        photo = open("../fiord.jpg", "rb")
        bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'I dont understand you((', parse_mode="html")


bot.polling(none_stop=True)
