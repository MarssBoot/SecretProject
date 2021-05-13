from aiogram.dispatcher.filters.state import StatesGroup, State


class Cal_calc(StatesGroup):
    t1 = State()
    t2 = State()
    t3 = State()
    t4 = State()


class Fat_calc(StatesGroup):
    d1 = State()
    d2 = State()
    d3 = State()
    d4 = State()
    d5 = State()


class Calend_state(StatesGroup):
    g1 = State()
    g2 = State()
    g3 = State()


class Prog_tren(StatesGroup):
    b1 = State()
    b2 = State()
    b3 = State()


class Delete_by_date(StatesGroup):
    y1 = State()
    y2 = State()
    y3 = State()


class Calories(StatesGroup):
    c1 = State()
