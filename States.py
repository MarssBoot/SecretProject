from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    t1 = State()
    t2 = State()
    t3 = State()
    t4 = State()


class Form1(StatesGroup):
    d1 = State()
    d2 = State()
    d3 = State()
    d4 = State()
    d5 = State()


class Form2(StatesGroup):
    g1 = State()
    g2 = State()
    g3 = State()


class Form3(StatesGroup):
    b1 = State()
    b2 = State()
    b3 = State()
