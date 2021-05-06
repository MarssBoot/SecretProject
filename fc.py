#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import math
import logging
# import schedule
# from time import sleep
# from threading import Thread
from database import init_db, add_weight, list_weight, is_exist, datetime, make_image
from States import Form, Form1, Form2

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

TOKEN = '1763824494:AAHWmjvc0UtBV_Hbk2feNL7dFn3R5LHYQj8'
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

button_help = "Помощь"
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

init_db()


# def alarm(message: types.Message):
# return bot.send_message(message.chat.id, "Миша лох")
# Уведы

# def schedule_checker():
# while True:
# schedule.run_pending()
# sleep(1)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Вас приветствует бот Fitcontrol\n' + 'Этот бот создан для помощи людям, следящих за своей '
                                                                 'формой или желающих похудеть/набрать массу')
    await bot.send_message(message.chat.id, message.from_user.id)


@dp.message_handler(commands=['help'], state=None)
async def help(message: types.Message):
    await bot.send_message(message.chat.id, 'Список доступных команд:\n' +
                           '/callories_calculate - рассчитайте каллории для поддержания/набора/сброса веса\n' +
                           '/fat_calculate - рассчитайте процент жира в своём организме\n' +
                           '/calendar - отслеживайте динамику своего веса\n')


@dp.message_handler(commands=['callories_calculate'], state=None)
async def callories_calculate(message: types.Message):
    await Form.t1.set()
    await bot.send_message(message.chat.id, 'Введите рост в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.t1)
async def get_height(message: types.Message, state=FSMContext):
    await Form.t2.set()
    await state.update_data(height=message.text)
    await bot.send_message(message.chat.id, 'Введите вес в килограммах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.t2)
async def get_weight(message: types.Message, state=FSMContext):
    await Form.t3.set()
    await state.update_data(weight=message.text)
    await bot.send_message(message.chat.id, 'Введите возраст')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.t3)
async def get_age(message: types.Message, state=FSMContext):
    await Form.t4.set()
    await state.update_data(age=message.text)
    await bot.send_message(message.chat.id, 'Введите ваш пол(мужской/женский)')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.t4)
async def get_sex(message: types.Message, state=FSMContext):
    await state.update_data(sex=message.text)
    tmp = await state.get_data()
    weight = tmp['weight']
    height = tmp['height']
    age = tmp['age']
    sex = tmp['sex']
    sex1 = sex.lower()
    cal_man = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 5
    cal_man_lower = cal_man * 0.9
    cal_man_bigger = cal_man * 1.1
    cal_women = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) - 161
    cal_women_lower = cal_women * 0.9
    cal_women_bigger = cal_women * 1.1
    if sex1[0] == 'м':
        await bot.send_message(message.chat.id,
                               'Кол-во каллорий, необходимых для поддержания массы: ' + str(int(cal_man)) + '\n\n' +
                               'Кол-во каллорий, необходимых для сброса веса: ' + str(int(cal_man_lower)) + '\n\n' +
                               'Кол-во каллорий, необходимых для набора массы: ' + str(int(cal_man_bigger)))
    elif sex1[0] == 'ж':
        await bot.send_message(message.chat.id,
                               'Кол-во каллорий, необходимых для поддержания массы: ' + str(int(cal_women)) + '\n\n' +
                               'Кол-во каллорий, необходимых для сброса веса: ' + str(int(cal_women_lower)) + '\n\n' +
                               'Кол-во каллорий, необходимых для набора массы: ' + str(int(cal_women_bigger)))
    await state.finish()


@dp.message_handler(commands=['fat_calculate'], state=None)
async def fat_calculate(message: types.Message):
    await Form1.d1.set()
    await bot.send_message(message.chat.id, 'Введите пол (мужчина/женщина)')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form1.d1)
async def get_something(message: types.Message, state=FSMContext):
    await Form1.d2.set()
    await state.update_data(sex=message.text)
    sex = message.text
    sex1 = sex.lower()
    if sex1 == "м":
        await Form1.d3.set()
        await state.update_data(hips="-1")
        await bot.send_message(message.chat.id, 'Введите обхват талии в сантиметрах')
    else:
        await bot.send_message(message.chat.id, 'Введите обхават бедер в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form1.d2)
async def get_waist(message: types.Message, state=FSMContext):
    await Form1.d3.set()
    await state.update_data(hips=message.text)
    await bot.send_message(message.chat.id, 'Введите обхват талии в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form1.d3)
async def get_height1(message: types.Message, state=FSMContext):
    await Form1.d4.set()
    await state.update_data(waist=message.text)
    await bot.send_message(message.chat.id, 'Введите рост в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form1.d4)
async def get_neck(message: types.Message, state=FSMContext):
    await Form1.d5.set()
    await state.update_data(height1=message.text)
    await bot.send_message(message.chat.id, 'Введите обахват шеи в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form1.d5)
async def get_end(message: types.Message, state=FSMContext):
    await state.update_data(neck=message.text)
    tmp = await state.get_data()
    sex = tmp['sex']
    hips = tmp['hips']
    height1 = tmp['height1']
    waist = tmp['waist']
    neck = tmp['neck']
    if hips == "-1":
        await bot.send_message(message.chat.id, "Процент жира в огранизме: " + str(round(495 / (
                    1.0324 - 0.19077 * (math.log10(float(waist) - float(neck))) + 0.15456 * (
                math.log10(float(height1)))) - 450, 1)) + "%")
    else:
        await bot.send_message(message.chat.id, "Процент жира в огранизме: " + str(round(495 / (
                    1.29579 - 0.35004 * (math.log10(float(waist) + float(hips) - float(neck))) + 0.22100 * (
                math.log10(float(height1)))) - 450, 1)) + "%")


@dp.message_handler(commands=['calendar'], state=None)
async def calendar(message: types.Message):
    await Form2.g1.set()
    user_id = message.from_user.id
    if is_exist(user_id=user_id) is None:
        await bot.send_message(message.chat.id, 'Вас нет в базе данных (╯°□°）╯︵ ┻━┻')
        await bot.send_message(message.chat.id, 'Введите вес в килограммах')
    else:
        await bot.send_message(message.chat.id, 'Вы уже есть в базе данных o((>ω< ))o')

        await bot.send_message(message.chat.id, 'Введите вес в килограммах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form2.g1)
async def get_weight1(message: types.Message, state=FSMContext):
    await Form2.g2.set()
    await state.update_data(weight=message.text)
    weight = message.text
    add_weight(user_id=message.from_user.id, weight=weight, datew=datetime.date.today())
    make_image(user_id=message.from_user.id)
    await bot.send_photo(message.chat.id, open(f"Images\{message.from_user.id}.png", "rb"))



if __name__ == '__main__':
    executor.start_polling(dp)
    # schedule.every().wednesday.at("18:53").do(alarm)
    # Thread(target=schedule_checker).start()






#438558915