import sqlite3
import datetime
import matplotlib.pyplot as plt


def ensure_connection(func):

    def inner(*args, **kwargs):
        with sqlite3.connect('fitcontrol.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_calendar(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS calendar')

    c.execute('''
    CREATE TABLE IF NOT EXISTS calendar(
        id           INTEGER PRIMARY KEY,
        user_id      INTEGER NOT NULL,
        weight       NUMERIC NOT NULL,
        datew        DATE 
    )
    ''')
    conn.commit()


@ensure_connection
def add_weight(conn, user_id: int, weight: float, datew: datetime):
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO calendar (user_id, weight, datew) VALUES (?, ?, ?)', (user_id, weight, datew))
    conn.commit()


@ensure_connection
def list_weight(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT datew, weight FROM calendar WHERE user_id = ?', (user_id,))
    return c.fetchall()


@ensure_connection
def is_exist(conn, user_id: int):
    c = conn.cursor()
    info = c.execute('SELECT * FROM calendar WHERE user_id=?', (user_id, ))
    return info.fetchone()


@ensure_connection
def delete(conn, user_id: int):
    c = conn.cursor()
    c.execute('DELETE FROM calendar WHERE id = (SELECT MAX(id) FROM calendar WHERE user_id = ?)', (user_id, ))
    conn.commit()


@ensure_connection
def del_by_date(conn, user_id: int, datew: datetime):
    c = conn.cursor()
    c.execute('DELETE FROM calendar WHERE user_id = ? AND datew = ?', (user_id, datew,))
    conn.commit()


def make_image(user_id: int):
    data = list_weight(user_id=user_id)
    dates = []
    weight = []
    for i in range(0, len(data)):
        dates.append(data[i][0])
        weight.append(data[i][1])
    plt.plot(dates, weight, 'g')
    plt.savefig(f'Images\{user_id}.png')


if __name__ == "__main__":
    init_calendar()
