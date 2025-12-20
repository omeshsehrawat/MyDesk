import datetime
from flask import Flask
from flask_mail import Mail
import registration_database
import todo_database
from email_scheduler import send_email
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

def send_pending_tasks():
    today = datetime.date.today()
    users = registration_database.get_all_users()

    with app.app_context():
        for user in users:
            tasks = todo_database.get_tasks_by_user(user["id"])

            pending = [
                f"-{t['task']}  (Deadline: {t['deadline']})"
                for t in tasks
                if t["status"] == "pending"
                and datetime.datetime.strptime(t["deadline"], "%Y-%m-%d").date() >= today
            ]

            if pending:
                body = "Pending Tasks Reminder\n\n"+"\n".join(pending)
                send_email(
                    "Pending Tasks Reminder",
                    body,
                    [user["email"]]
                )

if __name__ == "__main__":
    send_pending_tasks()