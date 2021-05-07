import sqlite3
from database import ensure_connection


@ensure_connection
def init_db2(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS programma')

    c.execute('''
    CREATE TABLE IF NOT EXISTS programma(
        dayofweek    INTEGER NOT NULL,
        week         INTEGER NOT NULL,
        pathof       TEXT PRIMARY KEY
    )
    ''')
    conn.commit()


@ensure_connection
def add_upr(conn, dayofweek: int, week: int, pathof: str):
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO programma (dayofweek, week, pathof) VALUES (?, ?, ?)', (dayofweek, week, pathof))
    conn.commit()


@ensure_connection
def list_upr(conn, dayofweek: int, week: int):
    c = conn.cursor()
    c.execute('SELECT pathof FROM programma WHERE dayofweek = ? AND week = ?', (dayofweek, week,))
    return c.fetchall()


if __name__ == "__main__":
    init_db2()
