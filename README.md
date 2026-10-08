
---

## 🗄️ Database Structure

| Table | Purpose |
|---|---|
| `users` | Student & admin accounts |
| `streams` | Academic streams (Science, Commerce, etc.) |
| `careers` | Career profiles |
| `exams` | Entrance exams |
| `career_exams` | Career ↔ exam mapping |
| `colleges` | Colleges per career |
| `quiz_questions` | Quiz questions |
| `quiz_options` | Answer options |
| `option_career_weights` | Scoring weights per option |
| `quiz_attempts` | A student's quiz session |
| `quiz_answers` | Answers given in an attempt |
| `attempt_results` | Career match results per attempt |
| `competitions` | Olympiads/scholarships |
| `bookmarks` | Saved careers & competitions |

---

## 📁 Project Structure
Path Finder/
├── app.py
├── seed_data.py
├── schema.sql
├── requirements.txt
├── Procfile
├── .env.example
├── README.md
├── templates/
│ ├── base.html
│ ├── home.html
│ ├── login.html / register.html
│ ├── quiz.html / results.html / history.html
│ ├── careers.html / career_detail.html
│ ├── competitions.html / exams.html
│ ├── bookmarks.html / dashboard.html
│ └── admin/
└── static/
├── css/
├── js/
└── images/


---

## ⚙️ Local Setup

**1. Clone the repo**
```bash
git clone https://github.com/BisenHarshil/10th-PathFinder.git
cd 10th-PathFinder
```

**2. Create & activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file based on `.env.example`:
```env
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
```
Use your Supabase **Transaction pooler** connection string if running on a host that only supports IPv4 (e.g. Render's free tier).

Never commit `.env` to GitHub.

**5. Create the database tables**

In Supabase → SQL Editor, paste and run the full contents of `schema.sql`.

**6. Load sample data**
```bash
python seed_data.py
```
This seeds an admin account: `admin@pathfinder.local` / `admin123` — change or remove this before any public use.

**7. Run the app**
```bash
python app.py
```
Visit `http://127.0.0.1:5000`

---

## ☁️ Production Deployment

- **App hosting:** Render (Flask app, served via `gunicorn`)
- **Database:** Supabase PostgreSQL
- **Start command:** `gunicorn app:app`
- Credentials are set via Render's Environment Variables, never committed to source

---

## 🔒 Security Notes

- Credentials live in environment variables, not in code
- `.env` is excluded via `.gitignore`
- Passwords are hashed with Werkzeug's `generate_password_hash`
- Admin routes are protected by role checks
- Production secrets should never be pushed to GitHub

---

## 🎓 Project Context

**Project:** PathFinder
**Student:** Harshil Bisen
**Class:** 10
**School:** PM SHRI Kendriya Vidyalaya Andrews Ganj
**Stack:** Python + Flask + PostgreSQL (Supabase)
**Deployment:** Render

Built as a full-stack project demonstrating backend development, database design, authentication, weighted scoring logic, deployment, and responsive UI design.

---

## 🌟 Future Improvements

- AI-assisted career guidance
- Larger, richer career dataset
- Student analytics dashboard
- Additional quiz categories
- College/course comparison tools
- Opportunity deadline notifications
- Smarter recommendation algorithm

---

## 📜 License

Created for educational and portfolio purposes.
© 2026 Harshil Bisen. All rights reserved.
