from aiogram import Bot, Dispatcher, executor, types

bot = Bot('5795089416:AAGvY6p8jdPg4EDoHxbUEMcSR1xIWpXofDg')
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("I tebe Halo")
    file = open("fiord.jpg", "rb")
    await message.answer_photo(file, "Give a photo!")


@dp.message_handler(commands=["inline"])
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Site", url="https://google.com"))
    markup.add(types.InlineKeyboardButton("Hello", callback_data="hello"))
    await message.reply("Hello", reply_markup=markup)


@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)


@dp.message_handler(commands=["reply"])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton("Site"))
    markup.add(types.KeyboardButton("WebSite"))
    await message.answer("Hello", reply_markup=markup)


executor.start_polling(dp)
