import os
import datetime
import todo_database
import registration_database
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

# mail = None
flask_app = None

# Email helpers while using SMTP
# def send_email(subject, body, recipients):
#     global flask_app
#     with flask_app.app_context():
#         msg = Message(subject=subject, recipients=recipients, body=body)
#         mail.send(msg)

# CORE SEND EMAIL SENDGRID
def send_email(subject, body, recipients):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=recipients,
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print("SendGrid Error:", e)

def send_new_task_email(task, deadline, recipients):
    message = (
        f"You added a new task: '{task}' \n"
        f"Deadline: {deadline} \n"
        "Please complete it on time"
    )
    send_email(
        "✅ New Task Added",
        message,
        recipients
    )

def send_registration_email(to_email, username, password=None):
    body = f"Hello {username}, \n\nWelcome to MyDesk App"
    if password:
        body += f"\n\nYour Password is: {password}"

    send_email(
        "Welcome to Daily Use App",
        body,
        [to_email]
    )

def send_pending_tasks_email(user):
    today = datetime.date.today()

    tasks = todo_database.get_tasks_by_user(user['id'])

    pending = [
        f"- {t['task']} (Deadline: {t['deadline']})" 
        for t in tasks
        if t['status'] == "pending" and datetime.datetime.strptime(t['deadline'], "%Y-%m-%d").date() >= today
    ]

    if pending:
        body = "Here are your pending tasks:\n\n" + "\n".join(pending)
        send_email("⏰ Pending Tasks Reminder", body, [user['email']])

def send_all_users_pending():
    users = registration_database.get_all_users()
    for user in users:
        send_new_task_email(user)

def start_scheduler(app):
    global flask_app
    flask_app = app 

    scheduler = BackgroundScheduler()

    reminder_hours = [8, 20]

    for hour in reminder_hours:
        scheduler.add_job(
            send_all_users_pending, 'cron',
            hour = hour, minute=0
        )
    
    scheduler.start()
    return scheduler

