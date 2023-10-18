from aiogram import Bot, Dispatcher, types, executor

bot = Bot("5681742144:AAERT6W3vBBY2D8zyig5BVtnYiuDmfrdSj4")
dp= Dispatcher(bot)

HELP_COMMANDS = """
/help - список команд
"""

@dp.message_handler(commands= ['help'])
async def help_command(message: types.Message):
    await message.reply(text = HELP_COMMANDS)

@dp.message_handler(commands= ['start'])
async def help_command(message: types.Message):
    await message.answer(text = 'Добро пожаловать')
    await message.delete()


if __name__ == "__main__":
    executor.start_polling(dp)