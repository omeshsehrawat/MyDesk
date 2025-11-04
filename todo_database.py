import sqlite3
from datetime import datetime

def create_table():
    with sqlite3.connect("daily_use_database.db") as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo(
                sr_no INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                date TEXT NOT NULL,
                deadline TEXT NOT NULL,
                status TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)      
            );
        """)
        db.commit()
        cursor.close()

def add_task(task, deadline, user_id, status="pending"):
    with sqlite3.connect("daily_use_database.db") as db:
        cursor = db.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO todo (task, status, date, deadline, user_id) VALUES (?, ?, ?, ?, ?)", (task, status, date, deadline, user_id))
        db.commit()
        cursor.close()

def get_tasks_by_user(user_id):
    with sqlite3.connect("daily_use_database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("SELECT * FROM todo WHERE user_id=?", (user_id,))
        rows = cursor.fetchall()

        tasks = [dict(row) for row in rows]
        db.close()
        return tasks

def delete_tasks(sr_no, user_id):
    with sqlite3.connect("daily_use_database.db") as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM todo WHERE sr_no=? AND user_id=?", (sr_no, user_id))
        db.commit()
        cursor.close()

def update_task_status(sr_no, status, user_id):
    with sqlite3.connect("daily_use_database.db") as db:
        cursor = db.cursor()
        cursor.execute("UPDATE todo SET status=? WHERE sr_no=? AND user_id=?", (status, sr_no, user_id))
        db.commit()
        cursor.close()
