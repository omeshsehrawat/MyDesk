from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import todo_database
import datetime
import registartion_database

mail = None
flask_app = None

# Email helpers
def send_email(subject, body, recipients):
    global flask_app
    with flask_app.app_context():
        msg = Message(subject=subject, recipients=recipients, body=body)
        mail.send(msg)

def send_new_task_email(task, deadline, recipients):
    send_email(
        "✅ New Task Added",
        f"You added a new task: \'{task}\' with deadline {deadline}\\n\\nPlease complete it on time.",
        recipients
    )
    
def send_registration_email(to_email, username, password=None):
    msg = Message(subject="Welcome to Daily Use App",
                  recipients=[to_email])
    body = f"Hello {username},\n\nWelcom to Daily Use App!"

    if password:
        body += f"\nYour password is: {password}"

    msg.body = body
    mail.send(msg)

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
    users = registartion_database.get_all_users()
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

