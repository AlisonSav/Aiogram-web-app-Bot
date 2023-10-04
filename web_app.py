from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

bot = Bot('5795089416:AAGvY6p8jdPg4EDoHxbUEMcSR1xIWpXofDg')
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Open web", web_app=WebAppInfo(url="https://itproger.com/telegram.html")))
    await message.answer("Hello!", reply_markup=markup)

executor.start_polling(dp)
