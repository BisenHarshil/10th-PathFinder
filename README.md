# 🚀 PathFinder

### Explore. Discover. Decide.

**PathFinder** is a modern career guidance platform designed to help students explore career options, discover important exams and competitions, and understand which career paths may match their interests.

Built as a school innovation project for **PM SHRI Kendriya Vidyalaya Andrews Ganj**, PathFinder combines a clean futuristic interface with a Flask + MySQL backend.

---

## ✨ Features

### 🎯 Career Explorer

Explore different career paths through structured information including:

* Career descriptions
* Required subjects
* Essential skills
* Related streams
* Entrance examinations
* Colleges and institutions
* Career recommendations

### 🧠 Career Quiz

Students can take an interest-based quiz and receive career matches based on their responses.

The system:

1. Presents career-oriented questions
2. Records student responses
3. Calculates career scores
4. Ranks matching careers
5. Displays match percentages

### 📊 Student Dashboard

Each student gets a personalized dashboard containing:

* Recent quiz results
* Career matches
* Saved careers
* Saved opportunities
* Quick navigation

### 🔖 Bookmarks

Students can save:

* Careers
* Competitions
* Opportunities

Saved items can be accessed later from the bookmarks section.

### 🏆 Opportunities & Competitions

Students can discover upcoming competitions and opportunities filtered according to:

* Class
* Interest
* Deadline

### 📚 Important Exams

The platform provides information about important examinations related to different career paths.

### 🛠️ Admin Dashboard

Administrators can manage the platform's content through a dedicated control panel.

Admin features include:

* Dashboard statistics
* Career management
* Quiz question management
* Competition management
* Content administration

---

# 🧩 Technology Stack

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| 🐍 Python        | Backend programming       |
| 🌐 Flask         | Web framework             |
| 🗄️ MySQL        | Database                  |
| 🎨 HTML5         | Page structure            |
| 💎 CSS3          | UI & animations           |
| ⚡ JavaScript     | Interactive features      |
| 🔐 Werkzeug      | Password hashing          |
| 🔑 Python-dotenv | Environment configuration |

---

# 🏗️ Project Architecture

```text
PathFinder/
│
├── app.py
├── schema.sql
├── seed_data.py
├── requirements.txt
├── .env.example
├── README.md
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── quiz.html
│   ├── results.html
│   ├── history.html
│   ├── careers.html
│   ├── career_detail.html
│   ├── competitions.html
│   ├── exams.html
│   ├── bookmarks.html
│   │
│   └── admin/
│       ├── dashboard.html
│       ├── careers.html
│       └── questions.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── app.js
    │
    └── images/
        └── kv-logo.png
```

---

# ⚙️ How It Works

```text
                ┌──────────────────┐
                │      Student     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   PathFinder UI  │
                └────────┬─────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Careers          Quiz       Opportunities
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                ┌──────────────────┐
                │   Flask Backend  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   MySQL Database │
                └──────────────────┘
```

---

# 🧠 Quiz Recommendation System

PathFinder uses a weighted scoring system to generate career matches.

Each quiz option can have different weights for different careers.

For example:

```text
Question
   ↓
Student selects option
   ↓
Option → Career Weight
   ↓
Score calculation
   ↓
Career ranking
   ↓
Top career matches
```

The system then converts the highest career score into a percentage-based match.

> **Important:** The quiz is designed as a guidance tool, not as a definitive assessment of a student's future.

---

# 🔐 Security

PathFinder includes basic security practices such as:

* Password hashing
* Session-based authentication
* Login protection
* Admin-only routes
* Environment variables for database credentials
* Role-based access control
* Protected student dashboards

Sensitive configuration should be stored in `.env` rather than directly inside the source code.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd PathFinder
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file in the project directory.

Example:

```env
SECRET_KEY=your-secret-key

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=pathfinder
```

---

# 🗄️ Database Setup

Make sure MySQL is running.

Open MySQL Workbench and execute:

```sql
CREATE DATABASE pathfinder;
```

Then run the project's database schema:

```text
schema.sql
```

After creating the database, seed the initial data:

```bash
python seed_data.py
```

This populates the database with the initial careers, questions, exams, competitions and related data.

---

# ▶️ Running the Application

Start the Flask development server:

```bash
python app.py
```

You should see Flask running locally.

Open the local address shown in the terminal in your browser.

---

# 👨‍💻 Developer

### Harshil Bisen

**Class 10 | PM SHRI Kendriya Vidyalaya Andrews Ganj**

PathFinder was developed as a student-led technology project combining:

* Python
* Flask
* MySQL
* HTML
* CSS
* JavaScript
* Database design
* Authentication
* Web development
* Git & GitHub

The project was built with the goal of creating a practical platform that can help students explore possible career directions in one place.

---

# 🎯 Project Goals

PathFinder aims to make career exploration:

**Accessible → Structured → Interactive → Student-friendly**

Instead of searching across multiple websites, students can use one platform to explore:

```text
CAREERS
   +
QUIZ
   +
EXAMS
   +
COMPETITIONS
   +
BOOKMARKS
   +
PERSONAL DASHBOARD
```

---

# 🔮 Future Improvements

Possible future versions could include:

* 🤖 AI-powered career assistant
* 📈 Advanced student analytics
* 🧭 Personalized career roadmaps
* 🎓 More detailed college information
* 📅 Exam deadline reminders
* 🔔 Opportunity notifications
* 📱 Progressive Web App support
* 🌐 Multi-school deployment
* 🧠 More advanced recommendation algorithms
* 📊 Admin analytics and reports

---

# 📌 Project Status

**🚧 Active Development**

The core platform, authentication, database integration, career explorer, quiz system, bookmarks, opportunities and admin functionality are being developed as part of the project.

---

# 📜 License

This project is created for educational and school-project purposes.

© 2026 Harshil Bisen. All rights reserved.

---

## ⭐ Support

If you find the project interesting, consider giving the repository a ⭐ on GitHub.

### PathFinder

**Explore. Discover. Decide.**
