from flask import Flask, render_template, request, jsonify, session
from flask_mail import Mail
import todo_database
import expense_database
import email_scheduler
import registartion_database_sqlite
from accessing_data import Accessing_Table_Data
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Initialize databases
todo_database.create_table()
expense_database.create_table()
registartion_database_sqlite.create_users_table()

access_data = Accessing_Table_Data()

# Gmai SMTP Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

# Initialize Mail
mail = Mail(app)

# Pass the mail object to scheduler module
email_scheduler.mail = mail

# Start scheduler for daily reminders
email_scheduler.start_scheduler(app)

# ROUTES
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')

    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        hashed_password = generate_password_hash(password)

        success = registartion_database_sqlite.add_user(email, username, hashed_password)
        if success:
            email_scheduler.send_registration_email(email, username, password)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Email or username already exists."})


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
    
    else:
        email = request.args.get('email')
        password = request.args.get('password')

    user = registartion_database_sqlite.get_user_by_email(email)

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid email or password"})

@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/home')
def home():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    return render_template('home.html')

# Todo tasks
@app.route('/todo')
def todo():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    return render_template('todo.html')

@app.route("/tasks", methods=["GET"])
def get_tasks():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    
    tasks = access_data.access_today_data("todo", session["user_id"])
    return jsonify(tasks)

@app.route("/add_task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    task = data.get("task")
    deadline = data.get("myDate")
    
    # Add to DB
    todo_database.add_task(task, deadline, session["user_id"])

    # Send instant email
    email_scheduler.send_new_task_email(task, deadline, [session['email']])

    return jsonify({"message": "Task added successfully!"})

@app.route("/delete/<int:sr_no>", methods=["DELETE"])
def delete_task(sr_no):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    
    todo_database.delete_tasks(sr_no, session["user_id"])
    return jsonify({"message": "Task deleted successfully!"})

@app.route("/update/<int:sr_no>", methods=["PUT"])
def update_task(sr_no):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    status = data.get("status")
    todo_database.update_task_status(sr_no, status, session["user_id"])
    return jsonify({"message": "Task update successfully"})

# Expense Functions
@app.route("/expense")
def expense():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    return render_template('expense.html')

@app.route("/expenditure", methods=["GET"])
def get_expenditure():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    
    expenditure = access_data.access_today_data("expense", session["user_id"])
    return jsonify(expenditure)

@app.route("/add_expense", methods=["POST"])
def add_expense():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    item = data.get("item")
    amount = data.get("amount")
    date = data.get("date")

    expense_database.add_expense(item,amount, date, session["user_id"])

    return jsonify({"message": "Expense added successfully!"})

@app.route("/delete_expense/<int:sr_no>", methods=["DELETE"])
def delete_expense(sr_no):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    
    expense_database.delete_expense(sr_no, session["user_id"])
    return jsonify({"message": "Expense deleted successfully!"})

# CGPA Calculator
@app.route('/cgpa')
def cgpa():
    return render_template('cgpa.html')

# Reports 
@app.route('/report')
def report():
    return render_template('report.html')

@app.route("/get_report", methods=["POST"])
def get_report():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    option = data.get("option")     # "todo" or "expense"
    start_date = data.get("startDate")
    end_date = data.get("endDate")

    # validate
    if not option or not start_date or not end_date:
        return jsonify({"error": "Missing parameters"}), 400

    # fetch from DB using Accessing_Table_Data
    report_data = access_data.access_data(option, start_date, end_date, session["user_id"])

    return jsonify(report_data)

if __name__ == '__main__':
    app.run(debug=True)