from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


"""
Задание выполнялось на:
Phiton 3.9
aiogram 2.25
"""

user_token = input('Введите ваш токен: ')
bot = Bot(token=user_token)
dp = Dispatcher(bot, storage=MemoryStorage())

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Расчитать")
button2 = KeyboardButton(text='Информация')
kb1.add(button1)
kb1.add(button2)

kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text="start")
kb2.add(button3)

kb3 = ReplyKeyboardMarkup(resize_keyboard=True)
button4 = KeyboardButton(text="Мужской")
button5 = KeyboardButton(text='Женский')
kb3.add(button4)
kb3.add(button5)


class UserState(StatesGroup):
    genders = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=["Информация"])
async def greeting(message):
    text = ('Домашнее задание по теме "Клавиатура кнопок".'
            '\nЦель: научится создавать клавиатуры и кнопки на них в Telegram-bot.'
            '\nЗадача "Меньше текста, больше кликов":'
            '\nСтудент Крылов Эдуард Васильевич.'
            '\nДата работы над заданием: 18.10.2024г.')
    await message.answer(text)


@dp.message_handler(text="Расчитать")
async def set_genders(message):
    await message.answer('Введите ваш пол:', reply_markup=kb3)
    await UserState.genders.set()


@dp.message_handler(state=UserState.genders)
async def set_age(message, state):
    keywb = types.ReplyKeyboardRemove()
    await state.update_data(genders=message.text)
    counting = await state.get_data()
    list_gender = str(counting['genders'])
    if list_gender == 'Мужской':
        await state.update_data(genders=float(5))
    elif list_gender == 'Женский':
        await state.update_data(genders=float(-161))
    else:
        await state.update_data(genders=float(5))
    await message.answer('Введите ваш возраст, лет', reply_markup=keywb)
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост, см.')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес, кг.')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    counting = await state.get_data()
    list_gender = float(counting['genders'])
    rep_weight = str(counting['weight']).replace(",", ".")
    set_weights = float(rep_weight)
    rep_growth = str(counting['growth']).replace(",", ".")
    set_growths = float(rep_growth)
    rep_age = str(counting['age']).replace(",", ".")
    set_ages = float(rep_age)
    calories = float(10 * set_weights + 6.25 * set_growths - 5 * set_ages + list_gender)
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()


@dp.message_handler(text=['start'])
async def start_message(messeage):
    await messeage.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb1)


@dp.message_handler()
async def all_message(message):
    await message.answer('Нажмите кнопку "start", чтобы начать общение.', reply_markup=kb2)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
