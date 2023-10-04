import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import config

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Open web", web_app=WebAppInfo(url="https://itproger.com/telegram.html")))
    await message.answer("Hello!", reply_markup=markup)


@dp.message_handler(content_types=["web_app_data"])
async def web_app(message: types.Message):
    res = json.loads(message.web_app_data.data)
    await message.answer(f"Name: {res['name']}. Email: {res['email']}. Phone: {res['phone']}")


@dp.message_handler(commands=["payment"])
async def payment(message: types.Message):
    await bot.send_invoice(message.chat.id, "Buy product", "Product", "invoice", config.PAYMENT_TOKEN, "USD",
                           [types.LabeledPrice("Buy product", 5 * 100)])


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def success(message: types.Message):
    await message.answer(f"Success: {message.successful_payment.order_info}")

executor.start_polling(dp)
