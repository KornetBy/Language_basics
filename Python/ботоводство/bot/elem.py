import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5681742144:AAERT6W3vBBY2D8zyig5BVtnYiuDmfrdSj4'  # вставьте свой токен в кавычках

# настройка журналирования
logging.basicConfig(level=logging.INFO)

# создание экземпляра бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот!")

# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)