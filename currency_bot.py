import telebot
from telebot import types
from currency_converter import CurrencyConverter


bot = telebot.TeleBot('5795089416:AAGvY6p8jdPg4EDoHxbUEMcSR1xIWpXofDg')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hi! Enter sum")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Invalid value. Enter sum")
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="USD/EUR")
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="EUR/USD")
        btn3 = types.InlineKeyboardButton("USD/GBP", callback_data="USD/GBP")
        btn4 = types.InlineKeyboardButton("Else", callback_data="else")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Select currency for convert", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Sum must be greater than 0")
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != "else":
        values = call.data.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"Result {round(res, 2)}. You can enter sum again")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Enter currency pair")
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"Result {round(res, 2)}. You can enter sum again")
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, "Something was wrong. Enter correct values")
        bot.register_next_step_handler(message, summa)


bot.polling(none_stop=True)
