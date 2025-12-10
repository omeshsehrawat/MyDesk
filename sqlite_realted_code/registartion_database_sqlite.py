import sqlite3


def create_users_table():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       email TEXT UNIQUE,
                       username TEXT UNIQUE,
                       password TEXT
            )
        ''')
    conn.commit()
    conn.close()

def add_user(email, username, password):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                    (email, username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect("user.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    db = sqlite3.connect("user.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("SELECT id, email, username, password FROM users")
    rows = cursor.fetchall()

    users = [dict(row) for row in rows]

    cursor.close()
    db.close()

    return users