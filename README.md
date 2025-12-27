# 📘 MyDesk – Daily Use Web Application

MyDesk is a full-stack web application designed to help users manage their **daily productivity, academics, and tasks** from a single platform.  
This project focuses on **real-world deployment challenges, scalability, and system migration**.

---

## 🚀 Features

### 📝 Task Management
- Add, update, and delete daily TODO tasks
- Set deadlines and task status (pending / completed)
- Date-wise task filtering

### 📧 Email Notifications
- New task creation email
- User registration email
- Automated pending task reminders (scheduled)

### 📊 Academic Tools
#### 🎓 SGPA & CGPA Calculator
- User selects **number of subjects**
- Enters **credits and grades**
- System first calculates **SGPA**
- Then asks for **previous SGPA values**
- Computes **final CGPA accurately**

### 💰 Expense Tracker
- Add daily expenses
- Date-wise expense tracking
- Summary reports

---

## 🔁 Project Evolution (Key Migrations)

### 🔹 Deployment
- Initially deployed on **Render**
- Faced worker timeouts & SMTP restrictions
- Migrated to **Railway** for stable production deployment

### 🔹 Email System
- Started with **SMTP (Gmail)**
- Failed in cloud environment due to blocked ports
- Refactored entire email service using **SendGrid API**
- Implemented verified sender & API-based mailing

### 🔹 Database
- Initially used **SQLite**
- Migrated to **Supabase (PostgreSQL)** for:
  - Cloud persistence
  - Multi-user scalability
  - Better reliability

---

## 🛠 Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | Flask, Gunicorn |
| Database | Supabase (PostgreSQL) |
| Email Service | SendGrid API |
| Scheduler | APScheduler |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Railway |

---

## 🧠 Key Learnings
- SMTP is **not production-safe** for cloud deployment
- Importance of **non-blocking email services**
- Debugging production logs & worker crashes
- Real DevOps experience: build → break → fix → improve
- API-based email authentication & sender verification

---

## 📌 Project Status
✅ Live & Deployed  
✅ Email system working in production  
✅ Database migrated to cloud  
✅ Academic calculator integrated  

---

## 📎 Author
**Omesh Sehrawat**  
