from aiogram import Bot, Dispatcher, types, executor
import string
import random
from first import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

@dp.message_handler(commands=['description'])
async def desc_command(message: types.message):
    await message.answer('Данный бот умеет')
    
@dp.message_handler() #ASCII
async def send_random_letter(message: types.Message):
    await message.reply(random.choice(string.ascii_letters))


if __name__ == "__main__":
    executor.start_polling(dp) 