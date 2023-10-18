from aiogram import Bot, Dispatcher, executor, types

TOKEN_API = "5681742144:AAERT6W3vBBY2D8zyig5BVtnYiuDmfrdSj4"

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.message):
    await message.answer(text = message.text)#Написать сообщение

if __name__== '__main__':
    executor.start_polling(dp)