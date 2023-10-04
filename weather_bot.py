import telebot
import requests
import json

bot = telebot.TeleBot('5795089416:AAGvY6p8jdPg4EDoHxbUEMcSR1xIWpXofDg')
API = "8595573b9165e526597c8e9ae92e4c8b"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello, enter city name")


@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message, f"The weather in {city} is: {data['main']['temp']} degrees")
    else:
        bot.reply_to(message, "Incorrect city name")


bot.polling(none_stop=True)
