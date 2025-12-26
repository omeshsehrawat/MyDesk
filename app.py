from flask import Flask, render_template, request, jsonify, session
from flask_mail import Mail
import todo_database
import expense_database
import email_scheduler
import registration_database
from accessing_data import Accessing_Table_Data
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

access_data = Accessing_Table_Data()

# ---------------- MAIL CONFIG ---------------- #
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)
email_scheduler.mail = mail
email_scheduler.start_scheduler(app)

# ---------------- AUTH ---------------- #

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

        success = registration_database.add_user(
            email, username, hashed_password
        )

        if success:
            email_scheduler.send_registration_email(
                email, username, password
            )
            return jsonify({"success": True,
                            "message": "Registration Successful"})
        else:
            return jsonify({
                "success": False,
                "message": "Email or username already exists"
            })


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # print("LOGIN EMAIL:", email)
    
    else:
        email = request.args.get('email')
        password = request.args.get('password')

    user = registration_database.get_user_by_email(email)

    # print("SUPABASE USER:", user)

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]

        return jsonify({
            "success": True,
            "username": user["username"],
            "email": user["email"]
        })

    return jsonify({
        "success": False,
        "message": "Invalid email or password"
    })


@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html')

# ---------------- HOME ---------------- #

@app.route('/home')
def home():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    return render_template('home.html')

# ---------------- TODO ---------------- #

@app.route('/todo')
def todo():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    return render_template('todo.html')


@app.route("/tasks")
def get_tasks():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    tasks = access_data.access_today_data(
        "todo", session["user_id"]
    )
    return jsonify(tasks)


@app.route("/add_task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    new_task = todo_database.add_task(
        data["task"],
        data["myDate"],
        session["user_id"]
    )

    email_scheduler.send_new_task_email(
        data["task"],
        data["myDate"],
        [session["email"]]
    )

    return jsonify({
        "message": "Task Added",
        "task": new_task
        })


@app.route("/delete/<int:sr_no>", methods=["DELETE"])
def delete_task(sr_no):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    todo_database.delete_tasks(sr_no, session["user_id"])
    return jsonify({"message": "Deleted"})


@app.route("/update/<int:sr_no>", methods=["PUT"])
def update_task(sr_no):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    todo_database.update_task_status(
        sr_no,
        data["status"],
        session["user_id"]
    )

    return jsonify({"message": "Updated"})

# ---------------- EXPENSE ---------------- #

@app.route("/expense")
def expense():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    return render_template('expense.html')


@app.route("/expenditure")
def get_expenditure():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = access_data.access_today_data(
        "expense", session["user_id"]
    )
    return jsonify(data)


@app.route("/add_expense", methods=["POST"])
def add_expense():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    expense_database.add_expense(
        data["item"],
        data["amount"],
        data["date"],
        session["user_id"]
    )

    return jsonify({"message": "Expense Added"})


@app.route("/delete_expense/<int:sr_no>", methods=["DELETE"])
def delete_expense(sr_no):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    expense_database.delete_expense(
        sr_no, session["user_id"]
    )
    return jsonify({"message": "Deleted"})

# ---------------- CGPA ------------------ #
@app.route('/cgpa')
def cgpa():
    return render_template('cgpa.html')

# ---------------- REPORT ---------------- #

@app.route('/report')
def report():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    return render_template('report.html')


@app.route("/get_report", methods=["POST"])
def get_report():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    report_data = access_data.access_data(
        data["option"],
        data["startDate"],
        data["endDate"],
        session["user_id"]
    )

    return jsonify(report_data)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
