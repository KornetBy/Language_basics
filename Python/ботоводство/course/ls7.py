from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from first import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Бот был успешно запущен')


@dp.message_handler(commands=['start'])
async def start_cammand(message: types.Message): 
    await message.answer('<em>Привет, добро пожаловать в наш бот!</em>',parse_mode = "HTML")

@dp.message_handler(commands=['give'])
async def start_cammand(message: types.Message): 
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEH6ZBj-43JO4-o3IPeNaMgGTYgduN-GwACphYAApxXEUpbd-VcuKli9y4E" )



if __name__ == "__main__":
    executor.start_polling(dp, on_startup= on_startup)
