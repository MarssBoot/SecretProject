#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import math
import os
import logging

import aioschedule
import text
import asyncio
from datetime import datetime
from calendardb import init_calendar, add_weight, is_exist, datetime, make_image, delete, del_by_date
from uprajn import init_gif, list_upr
from usersbd import init_users, add_user, list_users
from cal_by_day import init_calories, add_call, del_info, get_sum
from caloriesbd import init_cal, add_day_cal, make_graph
from States import Cal_calc, Fat_calc, Calend_state, Prog_tren, Delete_by_date, Calories

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

TOKEN = '1763824494:AAHWmjvc0UtBV_Hbk2feNL7dFn3R5LHYQj8'
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

button_help = "Помощь"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

init_calendar()
init_gif()
init_users()
init_calories()
init_cal()


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("Подождите, эта функция вызывает сильную нагрузку на сервер, подождите 5 минут, а потом вызовите "
                   "ее заново")


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    add_user(user_id=message.from_user.id)
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
                           '/graphic - вывести график с динамикой веса\n' +
                           '/delete_from_calendar - удалить последнее значение из базы данных веса\n' +
                           '/delete_by_date - удалить значения веса из базы данных по введенной дате\n' +
                           '/callories - внести количество калорий, потребленных за один прием пищи\n' +
                           '/get_calories - узнать количество калорий, потрбленных за день\n' +
                           '/get_calories_graphic - вывести график потребленных калорий за несколько дней\n' +
                           '/programma - ваша программа тренировок для похудения\n\n' +
                           "Если вы хотите приостановить работу какой-либо команды, введите 'стоп' на любом "
                           "этапе исполнения команды\n")


@dp.message_handler(commands=['callories_calculate'], state=None)
async def callories_calculate(message: types.Message):
    await Cal_calc.t1.set()
    await bot.send_message(message.chat.id, 'Введите рост в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Cal_calc.t1)
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
        await Cal_calc.t2.set()
        await state.update_data(height=message.text)
        await bot.send_message(message.chat.id, 'Введите вес в килограммах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Cal_calc.t2)
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
        await Cal_calc.t3.set()
        await state.update_data(weight=message.text)
        await bot.send_message(message.chat.id, 'Введите возраст')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Cal_calc.t3)
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
        await Cal_calc.t4.set()
        await state.update_data(age=message.text)
        await bot.send_message(message.chat.id, 'Введите ваш пол(мужской/женский)')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Cal_calc.t4)
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
        else:
            await bot.send_message(message.chat.id,
                                   'Введен некорректный пол. Введите команду /callories_calculate заново')
            await state.finish()
        await state.finish()


@dp.message_handler(commands=['fat_calculate'], state=None)
async def fat_calculate(message: types.Message):
    await Fat_calc.d1.set()
    await bot.send_message(message.chat.id, 'Введите пол (мужчина/женщина)')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Fat_calc.d1)
async def get_something(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    else:
        await Fat_calc.d2.set()
        await state.update_data(sex=message.text)
        sex = message.text
        sex1 = sex.lower()
        if sex1[0] == "м":
            await Fat_calc.d3.set()
            await state.update_data(hips="-1")
            await bot.send_message(message.chat.id, 'Введите обхват талии в сантиметрах')
        elif sex1[0] == "ж":
            await bot.send_message(message.chat.id, 'Введите обхават бедер в сантиметрах')
        else:
            await bot.send_message(message.chat.id, 'Введен некорректный пол. Введите команду /fat_calculate заново')
            await state.finish()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Fat_calc.d2)
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
        await Fat_calc.d3.set()
        await state.update_data(hips=message.text)
        await bot.send_message(message.chat.id, 'Введите обхват талии в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Fat_calc.d3)
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
        await Fat_calc.d4.set()
        await state.update_data(waist=message.text)
        await bot.send_message(message.chat.id, 'Введите рост в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Fat_calc.d4)
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
        await Fat_calc.d5.set()
        await state.update_data(height1=message.text)
        await bot.send_message(message.chat.id, 'Введите обахват шеи в сантиметрах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Fat_calc.d5)
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
    await Calend_state.g1.set()
    user_id = message.from_user.id
    if is_exist(user_id=user_id) is None:
        await bot.send_message(message.chat.id, 'Вас нет в базе данных (╯°□°）╯︵ ┻━┻')
        await bot.send_message(message.chat.id, 'Введите вес в килограммах')
    else:
        await bot.send_message(message.chat.id, 'Вы уже есть в базе данных o((>ω< ))o')

        await bot.send_message(message.chat.id, 'Введите вес в килограммах')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Calend_state.g1)
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
        make_image(user_id=message.from_user.id)
        await bot.send_photo(message.chat.id, open(f"Images\{message.from_user.id}.png", "rb"))
        os.remove(f"Images\{message.from_user.id}.png")
        await state.finish()


@dp.message_handler(commands=['delete_from_calendar'], state=None)
async def deletefc(message: types.Message):
    delete(user_id=message.from_user.id)
    await bot.send_message(message.chat.id, 'Вы успешно удалили последнее внесенное значение в таблицу веса')
    await bot.send_message(message.chat.id, 'Можете внести значение заново с помощью функции /calendar или вывести '
                                            'график с помощью фунции /graphic')


@dp.message_handler(commands=['delete_by_date'], state=None)
async def deletebd(message: types.Message):
    await Delete_by_date.y1.set()
    await bot.send_message(message.chat.id, 'Введите год')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Delete_by_date.y1)
async def get_year(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /delete_by_date заново')
        await state.finish()
    else:
        await Delete_by_date.y2.set()
        await state.update_data(year=message.text)
        await bot.send_message(message.chat.id, 'Введите месяц числом')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Delete_by_date.y2)
async def get_month(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /delete_by_date заново')
        await state.finish()
    else:
        await Delete_by_date.y3.set()
        await state.update_data(month=message.text)
        await bot.send_message(message.chat.id, 'Введите день числом')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Delete_by_date.y3)
async def get_day(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /delete_by_date заново')
        await state.finish()
    else:
        await state.update_data(day=message.text)
        tmp = await state.get_data()
        year = tmp['year']
        month = tmp['month']
        day = tmp['day']
        d = datetime.date(int(year), int(month), int(day))
        del_by_date(user_id=message.from_user.id, datew=d)
        await bot.send_message(message.chat.id, 'Вы успешно удалили данные')
        await state.finish()


@dp.message_handler(commands=['graphic'], state=None)
async def graphic(message: types.Message):
    make_image(user_id=message.from_user.id)
    await bot.send_photo(message.chat.id, open(f"Images\{message.from_user.id}.png", "rb"))
    os.remove(f"Images\{message.from_user.id}.png")


@dp.message_handler(commands=['programma'], state=None)
@dp.throttled(anti_flood, rate=300)
async def programma(message: types.Message):
    await bot.send_message(message.chat.id, 'Отдыхайте и тренируйтесь согласно следующему графику:\n\n День 1-й ('
                                            'тренировка)\n\n День 2-й (отдых)\n\n День 3-й (тренировка)\n\n День 4-й '
                                            '(отдых)\n\n День '
                                            '5-й (тренировка)\n\n День 6-й (отдых)\n\n День 7-й (отдых)\n\n Повторите '
                                            'то же '
                                            'самое!')
    await bot.send_message(message.chat.id, 'Введите день тренировки для этой недели(1, 2 или 3): ')
    await Prog_tren.b1.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Prog_tren.b1)
async def whatday(message: types.Message, state=FSMContext):
    if message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Тебе сказано, "Введите 1, 2 или 3", зачем ты вводишь буквы... '
                                                'сиди...\n' +
                               'И вводи /programma заново')
        await state.finish()
    elif int(message.text) > 3:
        await bot.send_message(message.chat.id, 'Сиди... думай над своим поведением...\n' +
                               'И вводи /programma заново')
        await state.finish()
    else:
        await state.update_data(day=message.text)
        await Prog_tren.b2.set()
        await bot.send_message(message.chat.id, 'Введите номер недели:')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Prog_tren.b2)
async def whatweek(message: types.Message, state=FSMContext):
    if message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Тебе сказано, "Введите номер недели", зачем ты вводишь буквы... '
                                                'сиди...\n' +
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
        week = tmp['week']
        paths = []
        for i in range(len(list_upr(dayofweek=day, week=week))):
            paths.append(list_upr(dayofweek=day, week=week)[i][0])
        for i in range(5):
            await bot.send_animation(message.chat.id, open(f'{paths[i]}', 'rb'))
            await bot.send_message(message.chat.id, text.Text_of_upr.upr[int(day) - 1][int(week) - 1][i])
        await state.finish()


@dp.message_handler(commands=['callories'], state=None)
async def callories(message: types.Message):
    await bot.send_message(message.chat.id, 'Внесите количество каллорий')
    await Calories.c1.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Calories.c1)
async def get_cal(message: types.Message, state=FSMContext):
    test = message.text.find("/")
    if test != -1:
        await bot.send_message(message.chat.id, 'Введите команду заново')
        await state.finish()
    elif message.text.lower() == "стоп":
        await bot.send_message(message.chat.id, 'Вы приостановили работу команды')
        await state.finish()
    elif message.text.isdigit() is False:
        await bot.send_message(message.chat.id, 'Сиди... и вводи /callories заново')
    else:
        add_call(user_id=message.from_user.id, calories=int(message.text))
        await bot.send_message(message.chat.id, f'Вы внесли {message.text} калорий')
        await state.finish()


@dp.message_handler(commands=['get_calories'], state=None)
async def get_list_cal(message: types.Message):
    await bot.send_message(message.chat.id, f'Количество потребленных вами сегодня калорий: '
                                            f'{get_sum(user_id=message.from_user.id)}')


@dp.message_handler(commands=['get_calories_graphic'], state=None)
async def cal_graphic(message: types.Message):
    add_day_cal(user_id=message.from_user.id, calories=get_sum(user_id=message.from_user.id), datec=datetime.date.today())
    make_graph(user_id=message.from_user.id)
    await bot.send_photo(message.chat.id, open(f"Images\{message.from_user.id}calories.png", "rb"))
    os.remove(f"Images\{message.from_user.id}calories.png")


async def scheduler():
    aioschedule.every().day.at("23:55").do(add_day_calories)
    aioschedule.every().day.at("00:00").do(del_cal)
    aioschedule.every().sunday.at("09:30").do(mass_sunday)
    aioschedule.every().monday.at("8:30").do(alert_tren)
    aioschedule.every().wednesday.at("8:30").do(alert_tren)
    aioschedule.every().friday.at("8:30").do(alert_tren)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


async def del_cal():
    del_info()


async def add_day_calories():
    users = list_users()
    d = datetime.date.today()
    for i in range(0, len(users)):
        add_day_cal(user_id=users[i][0], calories=get_sum(user_id=users[i][0]), datec=d)


async def mass_sunday():
    users = list_users()
    for i in range(0, len(users)):
        await bot.send_message(users[i][0], 'Не забудьте сегодня взвеситься и записать свой вес с помощью команды '
                                            '/calendar')


async def alert_tren():
    users = list_users()
    for i in range(0, len(users)):
        await bot.send_message(users[i][0], 'Доброе утро, не забудь, что сегодня день занятий. Получить упражнения ты '
                                            'можешь с помощью команды /programma')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

