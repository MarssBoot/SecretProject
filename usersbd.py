from calendardb import ensure_connection


@ensure_connection
def init_users(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS users')

    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id      INTEGER PRIMARY KEY
    )
    ''')
    conn.commit()


@ensure_connection
def add_user(conn, user_id: int):
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users (user_id) VALUES  (?)', (user_id,))
    conn.commit()


@ensure_connection
def list_users(conn):
    c = conn.cursor()
    info = c.execute('SELECT * FROM users')
    return info.fetchall()


if __name__ == "__main__":
    init_users()