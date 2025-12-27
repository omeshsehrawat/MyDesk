# 📌 MyDesk – Daily Use Web Application

MyDesk is a full-stack **Daily Use Web Application** designed to help users manage **tasks (TODOs)**, **expenses**, and **reports**, with **email notifications** and **scheduled reminders**.  
The application is deployed on **Railway** and uses **SendGrid** for reliable email delivery.

---

## 🚀 Features

### 🔐 Authentication
- User registration & login
- Secure password hashing
- Session-based authentication

### ✅ TODO Management
- Add, update, delete tasks
- Deadline-based task storage
- Daily task filtering
- Email notification on task creation

### 💰 Expense Tracker
- Add & delete expenses
- Date-wise expense tracking
- Daily expense overview

### 📊 Reports
- Generate reports using date ranges
- Filter data by user and category

### 📧 Email Notifications
- Registration confirmation email
- Task creation email
- Scheduled pending task reminders (twice daily)

---

## 🛠 Tech Stack

### Backend
- Python
- Flask
- Gunicorn

### Database
- Supabase (PostgreSQL)

### Email Service
- SendGrid API

### Scheduler
- APScheduler

### Deployment
- Railway

---

## 📩 Why SendGrid?

| SMTP (Gmail) | SendGrid |
|-------------|----------|
| Blocked on cloud platforms | Cloud-friendly |
| Causes worker timeout | Non-blocking API |
| Port restrictions | HTTPS-based |
| Not production safe | Production ready |

SendGrid ensures **reliable email delivery** without crashing Gunicorn workers on Railway.

---

## ⚙️ Environment Variables

Set the following variables in **Railway → Variables**:

```env
SECRET_KEY=your_secret_key

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=verified_sender_email@example.com
