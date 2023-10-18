import openpyxl
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# Инициализация бота и хранилища состояний
bot = Bot(token='5681742144:AAERT6W3vBBY2D8zyig5BVtnYiuDmfrdSj4')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Класс, описывающий состояния пользователя
class Registration(StatesGroup):
    surname = State()  # Фамилия
    name = State()  # Имя
    patronymic = State()  # Отчество
    birthdate = State()  # Дата рождения
    group = State()  # Номер группы
    phone = State()  # Номер телефона
    hostel = State()  # Необходимость общежития
    months = State()  # Месяцы работы
    specialties = State()  # Специальности на каждый месяц работы
    priority = State()  # Приоритеты специальностей


# Открытие таблицы и выбор листа
#wb = openpyxl.load_workbook('data.xlsx')
#ws = wb['Sheet1']


# Обработчик команды /start
@dp.message_handler(Command('start'))
async def start_cmd_handler(message: types.Message):
    # Приветственное сообщение
    await message.answer('Добро пожаловать в бот для вступления в студотряд! Введите /help для просмотра доступных команд.')


# Обработчик команды /help
@dp.message_handler(Command('help'))
async def help_cmd_handler(message: types.Message):
    # Описание доступных команд
    await message.answer('Доступные команды:\n'
                         '/help - помощь\n'
                         '/registration - регистрация\n'
                         '/delete - удаление заявки\n'
                         '/edit - редактирование заявки\n'
                         '/password - ввод кода для повышения приоритета\n'
                         '/about - информация о проекте и создателях\n')


# Обработчик команды /registration
@dp.message_handler(Command('registration'))
async def registration_cmd_handler(message: types.Message):
    # Сообщение о начале регистрации и запрос фамилии
    await message.answer('Введите вашу фамилию:')
    await Registration.surname.set()


# Обработчик ответа на запрос фамилии
@dp.message_handler(state=Registration.surname)
async def surname_handler(message: types.Message, state: FSMContext):
    # Сохранение фамилии в состоянии пользователя и запрос имени
    async with state.proxy() as data:
        data['surname'] = message.text
    await message.answer('Введите ваше имя:')
    await Registration.name.set()



# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)