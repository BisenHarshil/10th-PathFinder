import os
from functools import wraps
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from mysql.connector import Error, pooling
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "pathfinder"),
    "ssl_verify_cert": False,
    "ssl_verify_identity": False
}

DB_POOL = pooling.MySQLConnectionPool(
    pool_name="pathfinder_pool",
    pool_size=5,
    pool_reset_session=True,
    **DB_CONFIG
)

def db():
    return DB_POOL.get_connection()

def query(sql, params=(), one=False, commit=False):
    conn = db()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute(sql, params)

        if commit:
            conn.commit()
            return cur.lastrowid

        return cur.fetchone() if one else cur.fetchall()

    finally:
        cur.close()
        conn.close()

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return query("SELECT id, name, email, class_level, role FROM users WHERE id=%s", (uid,), one=True)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Please login to continue.", "info")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user or user["role"] != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("home"))
        return fn(*args, **kwargs)
    return wrapper

@app.context_processor
def inject_globals():
    return {"current_user": current_user(), "today": date.today()}

@app.route("/")
def home():
    careers = query("SELECT * FROM careers ORDER BY featured DESC, name LIMIT 6")
    competitions = query("""
        SELECT * FROM competitions
        WHERE deadline >= CURDATE()
        ORDER BY deadline ASC LIMIT 3
    """)
    return render_template("home.html", careers=careers, competitions=competitions)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        class_level = request.form["class_level"]
        if len(password) < 6:
            flash("Password should be at least 6 characters.", "danger")
            return redirect(url_for("register"))
        if query("SELECT id FROM users WHERE email=%s", (email,), one=True):
            flash("An account with this email already exists.", "warning")
            return redirect(url_for("login"))
        uid = query("""
            INSERT INTO users(name,email,password_hash,class_level,role)
            VALUES(%s,%s,%s,%s,'student')
        """, (name, email, generate_password_hash(password), class_level), commit=True)
        session["user_id"] = uid
        flash("Welcome to PathFinder!", "success")
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = query("SELECT * FROM users WHERE email=%s", (email,), one=True)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    latest = query("""
        SELECT qa.id, qa.created_at, ar.career_id, ar.match_percent, c.name
        FROM quiz_attempts qa
        JOIN attempt_results ar ON ar.attempt_id=qa.id
        JOIN careers c ON c.id=ar.career_id
        WHERE qa.user_id=%s
        ORDER BY qa.created_at DESC, ar.match_percent DESC
        LIMIT 3
    """, (user["id"],))
    bookmarks = query("""
        SELECT b.id, c.name, c.slug FROM bookmarks b
        JOIN careers c ON c.id=b.career_id
        WHERE b.user_id=%s
        ORDER BY b.created_at DESC LIMIT 4
    """, (user["id"],))
    return render_template("dashboard.html", latest=latest, bookmarks=bookmarks)

@app.route("/quiz")
@login_required
def quiz():
    questions = query("SELECT * FROM quiz_questions WHERE active=1 ORDER BY id")
    for q in questions:
        q["options"] = query("SELECT * FROM quiz_options WHERE question_id=%s ORDER BY id", (q["id"],))
    return render_template("quiz.html", questions=questions)

@app.route("/quiz/submit", methods=["POST"])
@login_required
def quiz_submit():
    user = current_user()
    questions = query("SELECT id FROM quiz_questions WHERE active=1 ORDER BY id")
    answers = []
    scores = {}
    for q in questions:
        oid = request.form.get(f"q_{q['id']}")
        if not oid:
            continue
        answers.append((q["id"], int(oid)))
        weights = query("""
            SELECT career_id, weight FROM option_career_weights
            WHERE option_id=%s
        """, (oid,))
        for w in weights:
            scores[w["career_id"]] = scores.get(w["career_id"], 0) + float(w["weight"])

    if not answers:
        flash("Please answer at least one question.", "warning")
        return redirect(url_for("quiz"))

    attempt_id = query(
        "INSERT INTO quiz_attempts(user_id) VALUES(%s)", (user["id"],), commit=True
    )
    conn = db()
    cur = conn.cursor()
    try:
        for qid, oid in answers:
            cur.execute(
                "INSERT INTO quiz_answers(attempt_id,question_id,option_id) VALUES(%s,%s,%s)",
                (attempt_id, qid, oid)
            )
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        max_score = max(scores.values()) if scores else 1
        for cid, score in ranked:
            pct = round((score / max_score) * 100)
            cur.execute(
                "INSERT INTO attempt_results(attempt_id,career_id,score,match_percent) VALUES(%s,%s,%s,%s)",
                (attempt_id, cid, score, pct)
            )
        conn.commit()
    finally:
        cur.close()
        conn.close()
    return redirect(url_for("results", attempt_id=attempt_id))

@app.route("/results/<int:attempt_id>")
@login_required
def results(attempt_id):
    user = current_user()
    attempt = query(
        "SELECT * FROM quiz_attempts WHERE id=%s AND user_id=%s",
        (attempt_id, user["id"]), one=True
    )
    if not attempt:
        flash("Result not found.", "danger")
        return redirect(url_for("dashboard"))
    results = query("""
        SELECT ar.*, c.name, c.slug, c.short_description, c.icon, s.name AS stream_name
        FROM attempt_results ar
        JOIN careers c ON c.id=ar.career_id
        LEFT JOIN streams s ON s.id=c.stream_id
        WHERE ar.attempt_id=%s
        ORDER BY ar.match_percent DESC
    """, (attempt_id,))
    return render_template("results.html", attempt=attempt, results=results)

@app.route("/history")
@login_required
def history():
    user = current_user()
    attempts = query("""
        SELECT qa.id, qa.created_at,
               GROUP_CONCAT(CONCAT(c.name,' (',ar.match_percent,'%)')
               ORDER BY ar.match_percent DESC SEPARATOR ', ') AS matches
        FROM quiz_attempts qa
        LEFT JOIN attempt_results ar ON ar.attempt_id=qa.id
        LEFT JOIN careers c ON c.id=ar.career_id
        WHERE qa.user_id=%s
        GROUP BY qa.id
        ORDER BY qa.created_at DESC
    """, (user["id"],))
    return render_template("history.html", attempts=attempts)

@app.route("/careers")
def careers():
    q = request.args.get("q", "").strip()
    if q:
        rows = query("""
            SELECT c.*, s.name AS stream_name FROM careers c
            LEFT JOIN streams s ON s.id=c.stream_id
            WHERE c.name LIKE %s OR c.short_description LIKE %s
            ORDER BY c.featured DESC, c.name
        """, (f"%{q}%", f"%{q}%"))
    else:
        rows = query("""
            SELECT c.*, s.name AS stream_name FROM careers c
            LEFT JOIN streams s ON s.id=c.stream_id
            ORDER BY c.featured DESC, c.name
        """)
    return render_template("careers.html", careers=rows, search=q)

@app.route("/career/<slug>")
def career_detail(slug):
    career = query("""
        SELECT c.*, s.name AS stream_name FROM careers c
        LEFT JOIN streams s ON s.id=c.stream_id
        WHERE c.slug=%s
    """, (slug,), one=True)
    if not career:
        return "Career not found", 404
    exams = query("""
        SELECT e.* FROM exams e
        JOIN career_exams ce ON ce.exam_id=e.id
        WHERE ce.career_id=%s ORDER BY e.name
    """, (career["id"],))
    colleges = query("SELECT * FROM colleges WHERE career_id=%s ORDER BY name", (career["id"],))
    return render_template("career_detail.html", career=career, exams=exams, colleges=colleges)

@app.route("/competitions")
@login_required
def competitions():
    user = current_user()
    class_filter = request.args.get("class_level", "")
    interest = request.args.get("interest", "")
    sql = "SELECT * FROM competitions WHERE deadline >= CURDATE()"
    params = []
    if class_filter:
        sql += " AND (class_level=%s OR class_level='All')"
        params.append(class_filter)
    if interest:
        sql += " AND (interest=%s OR interest='All')"
        params.append(interest)
    sql += " ORDER BY deadline ASC"
    rows = query(sql, tuple(params))
    saved = {x["competition_id"] for x in query(
        "SELECT competition_id FROM bookmarks WHERE user_id=%s AND competition_id IS NOT NULL",
        (user["id"],)
    )}
    return render_template("competitions.html", competitions=rows, saved=saved,
                           class_filter=class_filter, interest=interest)

@app.route("/exams")
def exams():
    rows = query("SELECT * FROM exams ORDER BY exam_date IS NULL, exam_date, name")
    return render_template("exams.html", exams=rows)

@app.route("/bookmarks")
@login_required
def bookmarks():
    user = current_user()
    careers = query("""
        SELECT b.id, c.name, c.slug, c.icon, b.created_at
        FROM bookmarks b JOIN careers c ON c.id=b.career_id
        WHERE b.user_id=%s
    """, (user["id"],))
    competitions = query("""
        SELECT b.id, x.name, x.deadline, b.created_at
        FROM bookmarks b JOIN competitions x ON x.id=b.competition_id
        WHERE b.user_id=%s
    """, (user["id"],))
    return render_template("bookmarks.html", careers=careers, competitions=competitions)

@app.route("/bookmark/career/<int:career_id>", methods=["POST"])
@login_required
def bookmark_career(career_id):
    uid = current_user()["id"]
    exists = query("SELECT id FROM bookmarks WHERE user_id=%s AND career_id=%s", (uid, career_id), one=True)
    if exists:
        query("DELETE FROM bookmarks WHERE id=%s", (exists["id"],), commit=True)
    else:
        query("INSERT INTO bookmarks(user_id,career_id) VALUES(%s,%s)", (uid,career_id), commit=True)
    return redirect(request.referrer or url_for("careers"))

@app.route("/bookmark/competition/<int:competition_id>", methods=["POST"])
@login_required
def bookmark_competition(competition_id):
    uid = current_user()["id"]
    exists = query("SELECT id FROM bookmarks WHERE user_id=%s AND competition_id=%s", (uid, competition_id), one=True)
    if exists:
        query("DELETE FROM bookmarks WHERE id=%s", (exists["id"],), commit=True)
    else:
        query("INSERT INTO bookmarks(user_id,competition_id) VALUES(%s,%s)", (uid,competition_id), commit=True)
    return redirect(request.referrer or url_for("competitions"))

@app.route("/admin")
@admin_required
def admin():
    stats = {
        "students": query("SELECT COUNT(*) n FROM users WHERE role='student'", one=True)["n"],
        "careers": query("SELECT COUNT(*) n FROM careers", one=True)["n"],
        "questions": query("SELECT COUNT(*) n FROM quiz_questions", one=True)["n"],
        "competitions": query("SELECT COUNT(*) n FROM competitions", one=True)["n"],
    }
    return render_template("admin/dashboard.html", stats=stats)

@app.route("/admin/careers", methods=["GET", "POST"])
@admin_required
def admin_careers():
    if request.method == "POST":
        name = request.form["name"].strip()
        slug = name.lower().replace(" ", "-").replace("/", "-")
        query("""
            INSERT INTO careers(name,slug,short_description,subjects,skills,icon,featured,stream_id)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """, (name, slug, request.form["description"], request.form["subjects"],
              request.form["skills"], request.form.get("icon","◎"),
              1 if request.form.get("featured") else 0, request.form.get("stream_id") or None), commit=True)
        flash("Career added.", "success")
    rows = query("SELECT c.*, s.name AS stream_name FROM careers c LEFT JOIN streams s ON s.id=c.stream_id ORDER BY c.name")
    streams = query("SELECT * FROM streams ORDER BY name")
    return render_template("admin/careers.html", careers=rows, streams=streams)

@app.route("/admin/questions", methods=["GET", "POST"])
@admin_required
def admin_questions():
    if request.method == "POST":
        qid = query("INSERT INTO quiz_questions(question_text) VALUES(%s)", (request.form["question_text"],), commit=True)
        for text in request.form.getlist("option_text"):
            oid = query("INSERT INTO quiz_options(question_id,option_text) VALUES(%s,%s)", (qid,text), commit=True)
        flash("Question added. Add weights in the database for custom scoring.", "success")
    questions = query("SELECT * FROM quiz_questions ORDER BY id DESC")
    return render_template("admin/questions.html", questions=questions)

@app.route("/api/careers")
def api_careers():
    rows = query("SELECT id,name,slug,icon FROM careers ORDER BY name")
    return jsonify(rows)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)