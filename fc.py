#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import math
import os.path
import os
import logging
from asyncio import sleep

import text
import asyncio
from datetime import datetime

from database import init_db, add_weight, is_exist, datetime, make_image
from database2 import init_db2, list_upr
from States import Form, Form1, Form2, Form3


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


MAX_FILESIZE_DOWNLOAD = 20000000
MAX_FILESIZE_UPLOAD = 50000000
MAX_MESSAGES_PER_SECOND = 30

TOKEN = '1763824494:AAHWmjvc0UtBV_Hbk2feNL7dFn3R5LHYQj8'
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

button_help = "Помощь"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

init_db()
init_db2()


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Вас приветствует бот Fitcontrol\n' + 'Этот бот создан для помощи людям, следящим за своей '
                                                                 'формой или желающим похудеть/набрать массу\n\n' +
                           'Введите /help, чтобы узнать список доступных команд')


@dp.message_handler(commands=['help'], state=None)
async def help(message: types.Message):
    await bot.send_message(message.chat.id, 'Список доступных команд:\n' +
                           '/callories_calculate - рассчитайте каллории для поддержания/набора/сброса веса\n' +
                           '/fat_calculate - рассчитайте процент жира в своём организме\n' +
                           '/calendar - отслеживайте динамику своего веса\n' +
                           '/programma - ваша программа тренировок для похудения\n\n' +
                           "Если вы хотите приостановить работу какой-либо команды, введите 'стоп' на любом "
                           "этапе исполнения команды\n")


@dp.message_handler(commands=['callories_calculate'], state=None)
async def callories_calculate(message: types.Message):
    await Form.t1.set()
    await bot.send_message(message.chat.id, 'Введите рост в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.t1)
async def get_height(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, "Введите команду заново")
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /callories_calculate заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    else:
        await Form.t2.set()
        await state.update_data(height=message.text)
        await bot.send_message(message.chat.id, 'Введите вес в килограммах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.t2)
async def get_weight(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /callories_calculate заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    else:
        await Form.t3.set()
        await state.update_data(weight=message.text)
        await bot.send_message(message.chat.id, 'Введите возраст')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.t3)
async def get_age(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /callories_calculate заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    else:
        await Form.t4.set()
        await state.update_data(age=message.text)
        await bot.send_message(message.chat.id, 'Введите ваш пол(мужской/женский)')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.t4)
async def get_sex(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    else:
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
                                   'Кол-во каллорий, необходимых для поддержания массы: ' + str(
                                       int(cal_women)) + '\n\n' +
                                   'Кол-во каллорий, необходимых для сброса веса: ' + str(
                                       int(cal_women_lower)) + '\n\n' +
                                   'Кол-во каллорий, необходимых для набора массы: ' + str(int(cal_women_bigger)))
        await state.finish()


@dp.message_handler(commands=['fat_calculate'], state=None)
async def fat_calculate(message: types.Message):
    await Form1.d1.set()
    await bot.send_message(message.chat.id, 'Введите пол (мужчина/женщина)')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form1.d1)
async def get_something(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    else:
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
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /fat_calculate заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    else:
        await Form1.d3.set()
        await state.update_data(hips=message.text)
        await bot.send_message(message.chat.id, 'Введите обхват талии в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form1.d3)
async def get_height1(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /fat_calculate заново')
        await state.finish()
    else:
        await Form1.d4.set()
        await state.update_data(waist=message.text)
        await bot.send_message(message.chat.id, 'Введите рост в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form1.d4)
async def get_neck(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /fat_calculate заново')
        await state.finish()
    else:
        await Form1.d5.set()
        await state.update_data(height1=message.text)
        await bot.send_message(message.chat.id, 'Введите обахват шеи в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form1.d5)
async def get_end(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /fat_calculate заново')
        await state.finish()
    elif test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    else:
        await state.update_data(neck=message.text)
        tmp = await state.get_data()
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
        await state.finish()


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
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    else:
        await state.update_data(weight=message.text)
        weight = message.text
        add_weight(user_id=message.from_user.id, weight=weight, datew=datetime.date.today())
        if os.path.exists(f"Images\{message.from_user.id}.png"):
            os.remove(f"Images\{message.from_user.id}.png")
        make_image(user_id=message.from_user.id)
        await bot.send_photo(message.chat.id, open(f"Images\{message.from_user.id}.png", "rb"))
        os.remove(f"Images\{message.from_user.id}.png")
        await state.finish()


@dp.message_handler(commands=['programma'], state=None)
async def programma(message: types.Message):
    await bot.send_message(message.chat.id, 'Отдыхайте и тренируйтесь согласно следующему графику:\n\n День 1-й ('
                                            'тренировка)\n\n День 2-й (отдых)\n\n День 3-й (тренировка)\n\n День 4-й '
                                            '(отдых)\n\n День '
                                            '5-й (тренировка)\n\n День 6-й (отдых)\n\n День 7-й (отдых)\n\n Повторите '
                                            'то же '
                                            'самое!')
    await bot.send_message(message.chat.id, 'Введите день тренировки для этой недели(1, 2 или 3): ')
    await Form3.b1.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form3.b1)
async def whatday(message: types.Message, state=FSMContext):
    if message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Тебе сказано, "Введите 1, 2 или 3", зачем ты вводишь буквы... сиди...\n' +
                                                'И вводи /programma заново')
        await state.finish()
    elif int(message.text) > 3:
        await bot.send_message(message.chat.id, 'Сиди... думай над своим поведением...\n' +
                                                'И вводи /programma заново')
        await state.finish()
    else:
        await state.update_data(day=message.text)
        await Form3.b2.set()
        await bot.send_message(message.chat.id, 'Введите номер недели:')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form3.b2)
async def whatweek(message: types.Message, state=FSMContext):
    if message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Тебе сказано, "Введите номер недели", зачем ты вводишь буквы... сиди...\n' +
                                                'И вводи /programma заново')
        await state.finish()
    else:
        if int(message.text) % 2 == 1:
            await state.update_data(week=1)
            await bot.send_message(message.chat.id, 'Ваши упражнения на сегодня: ')
        else:
            await state.update_data(week=2)
            await bot.send_message(message.chat.id, 'Ваши упражнения на сегодня: ')
        tmp = await state.get_data()
        day = tmp['day']
        week =tmp['week']
        paths = []
        for i in range(len(list_upr(dayofweek=day, week=week))):
            paths.append(list_upr(dayofweek=day, week=week)[i][0])
        for i in range(5):
            await sleep(2)
            await bot.send_animation(message.chat.id, open(f'{paths[i]}', 'rb'))
            await bot.send_message(message.chat.id, text.Text_of_upr.upr[int(day)-1][int(week)-1][i])
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

