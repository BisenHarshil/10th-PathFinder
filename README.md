# Supabase / PostgreSQL migration notes

This project version changes the backend database driver from MySQL to PostgreSQL for Supabase.

## Setup with Supabase
1. Create a Supabase project.
2. In Supabase, open **SQL Editor**, paste the full contents of `schema.sql`, and run it.
3. Copy your PostgreSQL connection string from **Project Settings → Database**. Prefer the Session pooler connection if your host environment cannot use direct IPv6 connectivity.
4. Set `DATABASE_URL` in your local `.env` and in Render Environment Variables. Use the actual connection string from Supabase; do not commit `.env`.
5. Install packages with `pip install -r requirements.txt`.
6. Run `python seed_data.py` once to insert the sample careers, quiz questions, options, and competitions.
7. Start locally with `python app.py`, test all pages, then commit and push to GitHub so Render can deploy.

The sample admin credentials seeded by `seed_data.py` are `admin@pathfinder.local` / `admin123`. Change/remove this demo account before using the site publicly.

**Important:** This schema creates new tables in Supabase; it does not automatically copy the records from your old Aiven database. Run the seed script to add demo data, or separately migrate any real user records you need to preserve. Never share your database password or full connection string publicly.

---

# PathFinder

### Career Discovery & Opportunity Platform

PathFinder is a modern career-discovery web application designed to help students explore career options based on their interests, strengths, subjects, and preferences.

It provides an interactive career quiz, personalized career recommendations, career information, opportunities, bookmarks, and an administrative control panel — all backed by a MySQL database.

---

## 🚀 Live Project

**Live Website:**
https://one0th-pathfinder.onrender.com/

---

## ✨ Features

### 🎯 Interest-Based Career Quiz

* Interactive multiple-choice career quiz
* Questions stored dynamically in MySQL
* Career-specific scoring using weighted options
* Personalized results based on quiz responses
* Top career recommendations with matching percentages

### 🔎 Career Explorer

Explore careers with information such as:

* Career overview
* Required subjects
* Important skills
* Related exams
* Recommended colleges
* Relevant academic streams

### 📅 Opportunities

Students can discover opportunities such as:

* Olympiads
* Competitions
* Scholarships
* Academic opportunities
* Deadlines
* Interest/class-based information

### 🔖 Bookmarks

* Save interesting careers and opportunities
* Quickly access saved items from the bookmarks section

### 📊 Quiz History

* Previous quiz attempts are stored
* Students can revisit their career recommendation history

### 🛠️ Admin Panel

Administrators can manage:

* Careers
* Quiz questions
* Students
* Competitions
* Platform content

### 🔐 Authentication

* Student registration
* Login/logout
* Password hashing
* Role-based admin access

### ⚡ Performance

* MySQL connection pooling
* Optimized database connection handling
* Deployed production database using Aiven MySQL

---

## 🧠 How PathFinder Works

```text
Student
   ↓
Register / Login
   ↓
Take Career Quiz
   ↓
Answers → Weighted Career Scoring
   ↓
Top Career Matches
   ↓
Explore Careers & Opportunities
   ↓
Bookmark Interesting Options
```

---

## 🏗️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI

### Backend

* Python
* Flask
* Flask routing and session management

### Database

* MySQL
* mysql-connector-python

### Deployment

* Render — Web Application Hosting
* Aiven — Cloud MySQL Database

### Development Tools

* Visual Studio Code
* Git
* GitHub
* MySQL Workbench

---

## 🗄️ Database Structure

PathFinder uses a relational MySQL database containing tables for:

* `users`
* `streams`
* `careers`
* `exams`
* `career_exams`
* `colleges`
* `quiz_questions`
* `quiz_options`
* `option_career_weights`
* `quiz_attempts`
* `quiz_answers`
* `attempt_results`
* `competitions`
* `bookmarks`

The database separates users, career information, quiz content, scoring relationships, opportunities, and saved items into structured entities.

---

## 📁 Project Structure

```text
Path Finder/
│
├── app.py
├── seed_data.py
├── schema.sql
├── requirements.txt
├── .env.example
├── README.md
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── quiz.html
│   ├── results.html
│   ├── careers.html
│   ├── career_detail.html
│   ├── opportunities.html
│   ├── bookmarks.html
│   └── admin/
│
└── static/
    ├── css/
    ├── js/
    └── images/
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/BisenHarshil/10th-PathFinder.git
cd 10th-PathFinder
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=pathfinder
```

Never commit your `.env` file to GitHub.

### 5. Create the database

Run `schema.sql` using MySQL Workbench or the MySQL command line.

### 6. Load sample data

```bash
python seed_data.py
```

### 7. Start the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## ☁️ Production Deployment

PathFinder is deployed using:

**Frontend + Flask Application:** Render

**Cloud Database:** Aiven MySQL

Production database credentials are configured through environment variables rather than being stored in the source code.

The application uses MySQL connection pooling to reduce repeated database connection overhead when communicating with the remote production database.

---

## 🔒 Security Notes

* Database credentials are stored in environment variables.
* `.env` is excluded from version control.
* Passwords are stored using secure password hashing.
* Admin functionality is protected through role-based access.
* Production credentials should never be committed to GitHub.

---

## 🎓 Project Context

**Project:** PathFinder
**Student:** Harshil Bisen
**Class:** 10
**School:** PM SHRI Kendriya Vidyalaya Andrews Ganj
**Technology:** Python + Flask + MySQL
**Deployment:** Render + Aiven

PathFinder was developed as a practical full-stack web application demonstrating backend development, database management, authentication, dynamic scoring, deployment, and responsive web design.

---

## 🌟 Future Improvements

Possible future versions could include:

* AI-assisted career guidance
* More comprehensive career datasets
* Advanced student analytics
* More quizzes and assessment categories
* College/course comparison
* Opportunity notifications
* Improved recommendation algorithms
* Student progress dashboards

---

## 📜 License

This project is created for educational and portfolio purposes.

© 2026 Harshil Bisen. All rights reserved.
