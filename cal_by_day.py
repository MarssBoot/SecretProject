from calendardb import ensure_connection


@ensure_connection
def init_calories(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS calories_by_day')

    c.execute('''
    CREATE TABLE IF NOT EXISTS calories_by_day(
        id           INTEGER PRIMARY KEY,
        user_id      INTEGER NOT NULL,
        calories     INTEGER NOT NULL
    )
    ''')
    conn.commit()


@ensure_connection
def add_call(conn, user_id: int, calories: int):
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO calories_by_day (user_id, calories) VALUES (?, ?)', (user_id, calories,))
    conn.commit()


@ensure_connection
def get_sum(conn, user_id: int):
    c = conn.cursor()
    info = c.execute('SELECT calories FROM calories_by_day WHERE user_id = ?', (user_id,)).fetchall()
    sum_cal = 0
    for i in range(0, len(info)):
        sum_cal += info[i][0]
    return sum_cal


@ensure_connection
def del_info(conn):
    c = conn.cursor()
    c.execute('DELETE FROM calories_by_day')
    conn.commit()


if __name__ == "__main__":
    init_calories()
