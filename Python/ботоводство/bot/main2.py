import openpyxl
import aiogram
from aiogram import Bot, Dispatcher, types, filters,executor
from aiogram.types import ParseMode
import logging

# Создание экземпляра бота и диспетчера
API_TOKEN = '5681742144:AAERT6W3vBBY2D8zyig5BVtnYiuDmfrdSj4'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)



# Путь к файлу с данными пользователей
EXCEL_FILE_PATH = "users.xlsx"

# Список доступных месяцев и специальностей
MONTHS = ["июнь", "июль", "август"]
SPECIALTIES = {
    "июнь": ["специальность 1", "специальность 2", "специальность 3"],
    "июль": ["специальность 2", "специальность 3", "специальность 4"],
    "август": ["специальность 1", "специальность 3", "специальность 5"]
}

# Список кодов для повышения уровня приоритета
CODES = ["code1", "code2", "code3"]


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_welcome(message: types.Message):
    await message.reply("Добро пожаловать в студотряд!\n"
                         "Доступные команды: /start, /help, /registration, /delete, /edit, /password, /about")


# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    specialties_info = "\n".join([f"{spec}: {', '.join(SPECIALTIES[spec])}" for spec in MONTHS])
    await message.answer(f"Доступные специальности по месяцам:\n{specialties_info}\n"
                         f"Доступные месяцы: {', '.join(MONTHS)}")


# Обработчик команды /about
@dp.message_handler(commands=['about'])
async def about_handler(message: types.Message):
    # Добавьте информацию о проекте и создателях
    await message.answer("О проекте...")

# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
