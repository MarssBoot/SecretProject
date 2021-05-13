import datetime

from calendardb import ensure_connection
import matplotlib.pyplot as plt
from cal_by_day import get_sum


@ensure_connection
def init_cal(conn,  force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS calories')

    c.execute('''
       CREATE TABLE IF NOT EXISTS calories(
           user_id      INTEGER NOT NULL,
           calories     INTEGER NOT NULL,
           datec        DATE PRIMARY KEY
       )
       ''')
    conn.commit()


@ensure_connection
def add_day_cal(conn, user_id: int, calories: int, datec: datetime):
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO calories (user_id, calories, datec) VALUES (?, ?, ?)', (user_id, calories, datec))
    conn.commit()


@ensure_connection
def list_calories(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT calories, datec FROM calories WHERE user_id = ?', (user_id,))
    return c.fetchall()


def make_graph(user_id: int):
    data = list_calories(user_id=user_id)
    dates = []
    calories = []
    for i in range(0, len(data)):
        calories.append(data[i][0])
        dates.append(data[i][1])
    plt.plot(dates, calories, 'g')
    plt.savefig(f'Images\{user_id}calories.png')


if __name__ == "__main__":
    init_cal()
    add_day_cal(user_id=438558915, calories=1650, datec=datetime.date(2021, 5, 11))
    add_day_cal(user_id=438558915, calories=1500, datec=datetime.date(2021, 5, 10))
    add_day_cal(user_id=438558915, calories=1500, datec=datetime.date(2021, 5, 9))
    add_day_cal(user_id=438558915, calories=1700, datec=datetime.date(2021, 5, 8))