from app import db
from werkzeug.security import generate_password_hash

conn = db()
cur = conn.cursor()

# Admin
cur.execute("""
INSERT INTO users(name,email,password_hash,class_level,role)
VALUES(%s,%s,%s,%s,'admin')
ON CONFLICT (email) DO UPDATE SET role='admin'
""", ("PathFinder Admin","admin@pathfinder.local",generate_password_hash("admin123"),"12"))

streams = [
    ("Science","Explore engineering, medicine, research and technology."),
    ("Commerce","Business, finance, economics and management."),
    ("Humanities","Law, psychology, social sciences, languages and public service."),
    ("Creative","Design, media, communication and creative technology.")
]
for x in streams:
    cur.execute("INSERT INTO streams(name,description) VALUES(%s,%s) ON CONFLICT (name) DO NOTHING", x)

cur.execute("SELECT name,id FROM streams")
stream_map = {name: sid for name, sid in cur.fetchall()}

careers = [
("Software Developer","software-developer","Build apps, websites and software products.","Computer Science, Mathematics, Physics","Programming, logic, problem solving, teamwork","</>",1,"Science"),
("Data Scientist","data-scientist","Use data, statistics and code to solve real problems.","Mathematics, Computer Science, Statistics","Python, statistics, analysis, communication","◉",1,"Science"),
("Doctor","doctor","Study medicine and help diagnose and treat patients.","Physics, Chemistry, Biology","Empathy, biology, decision making, communication","✚",1,"Science"),
("Mechanical Engineer","mechanical-engineer","Design machines, products and mechanical systems.","Physics, Mathematics","CAD, mechanics, design, problem solving","⚙",1,"Science"),
("Chartered Accountant","chartered-accountant","Work with accounting, audit, tax and financial decisions.","Accountancy, Economics, Mathematics","Numeracy, analysis, attention to detail","₹",1,"Commerce"),
("Business Analyst","business-analyst","Connect business needs with data and technology.","Economics, Mathematics, Computer Applications","Analysis, communication, research","▦",0,"Commerce"),
("Lawyer","lawyer","Study law, build arguments and help people navigate legal systems.","Political Science, English, History","Reasoning, research, speaking, writing","§",1,"Humanities"),
("Psychologist","psychologist","Study human behaviour and support wellbeing through evidence-based practice.","Psychology, Biology, Statistics","Listening, research, communication, empathy","◌",1,"Humanities"),
("Teacher","teacher","Help students learn, grow and develop confidence.","Relevant subject, Education","Communication, patience, leadership","★",0,"Humanities"),
("UI/UX Designer","ui-ux-designer","Design useful and engaging digital experiences.","Design, Computer Applications","Visual thinking, user research, prototyping","✦",1,"Creative"),
]
for c in careers:
    cur.execute("""
    INSERT INTO careers(name,slug,short_description,subjects,skills,icon,featured,stream_id)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (slug) DO NOTHING
    """, (*c[:-1], stream_map[c[-1]]))

cur.execute("SELECT id,name FROM careers")
career_map = {name: cid for cid,name in cur.fetchall()}

exams = [
("JEE Main","Joint Entrance Examination Main", "2027-01-01","Engineering entrance exam for participating institutions.","https://jeemain.nta.nic.in/"),
("NEET UG","National Eligibility cum Entrance Test", "2027-05-01","Undergraduate medical entrance examination.","https://neet.nta.nic.in/"),
("CUET UG","Common University Entrance Test", "2027-05-01","Entrance route for undergraduate programmes at participating universities.","https://cuet.nta.nic.in/"),
("CLAT","Common Law Admission Test", "2026-12-01","Entrance examination for participating National Law Universities.","https://consortiumofnlus.ac.in/"),
]
for e in exams:
    cur.execute("INSERT INTO exams(name,full_name,exam_date,description,website) VALUES(%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", e)
cur.execute("SELECT id,name FROM exams")
exam_map = {name: eid for eid,name in cur.fetchall()}

links = {
"Software Developer":["JEE Main","CUET UG"],
"Mechanical Engineer":["JEE Main"],
"Doctor":["NEET UG"],
"Data Scientist":["JEE Main","CUET UG"],
"Lawyer":["CLAT"],
"Teacher":["CUET UG"],
}
for cname, enames in links.items():
    for ename in enames:
        cur.execute("INSERT INTO career_exams(career_id,exam_id) VALUES(%s,%s) ON CONFLICT DO NOTHING", (career_map[cname],exam_map[ename]))

colleges = {
"Software Developer":["IIT Bombay — Mumbai","IIT Delhi — New Delhi","IIIT Hyderabad — Hyderabad"],
"Data Scientist":["IIT Madras — Chennai","IIT Bombay — Mumbai","IIT Delhi — New Delhi"],
"Doctor":["AIIMS New Delhi — New Delhi","JIPMER — Puducherry","MAMC — New Delhi"],
"Mechanical Engineer":["IIT Kanpur — Kanpur","IIT Bombay — Mumbai","IIT Delhi — New Delhi"],
"Lawyer":["NLSIU — Bengaluru","NLU Delhi — New Delhi","NALSAR — Hyderabad"],
"Teacher":["University of Delhi — New Delhi","Jamia Millia Islamia — New Delhi"],
}
for cname, names in colleges.items():
    for n in names:
        if " — " in n:
            nm, loc = n.split(" — ",1)
        else:
            nm, loc = n, ""
        cur.execute("INSERT INTO colleges(career_id,name,location) SELECT %s,%s,%s WHERE NOT EXISTS (SELECT 1 FROM colleges WHERE career_id=%s AND name=%s)",
                    (career_map[cname],nm,loc,career_map[cname],nm))

questions = [
("Which activity sounds most interesting to you?",[
("Building an app or solving a coding problem.",["Software Developer","Data Scientist"],[5,4]),
("Understanding how the human body works.",["Doctor","Psychologist"],[5,4]),
("Planning a business or handling money.",["Chartered Accountant","Business Analyst"],[5,4]),
("Arguing a case or discussing social issues.",["Lawyer","Teacher"],[5,3])]),
("What kind of problem do you enjoy?",[
("A logical puzzle with a clear solution.",["Software Developer","Data Scientist","Mechanical Engineer"],[4,5,3]),
("A people-focused problem.",["Doctor","Psychologist","Teacher"],[4,5,4]),
("A money or business decision.",["Chartered Accountant","Business Analyst"],[5,5]),
("A debate involving rules and fairness.",["Lawyer","Teacher"],[5,3])]),
("Which school area would you happily spend extra time learning?",[
("Maths and Computer Science.",["Software Developer","Data Scientist","Mechanical Engineer"],[4,5,4]),
("Biology and Chemistry.",["Doctor","Psychologist"],[5,4]),
("Accountancy and Economics.",["Chartered Accountant","Business Analyst"],[5,5]),
("English, History or Political Science.",["Lawyer","Teacher"],[5,4])]),
("Which strength describes you best?",[
("I like creating things with technology.",["Software Developer","UI/UX Designer"],[5,4]),
("I notice patterns in information.",["Data Scientist","Business Analyst"],[5,4]),
("I like helping and understanding people.",["Doctor","Psychologist","Teacher"],[4,5,4]),
("I communicate ideas confidently.",["Lawyer","Teacher","UI/UX Designer"],[5,4,3])]),
]
for qtext, opts in questions:
    cur.execute("SELECT id FROM quiz_questions WHERE question_text=%s", (qtext,))
    row=cur.fetchone()
    if row: qid=row[0]
    else:
        cur.execute("INSERT INTO quiz_questions(question_text) VALUES(%s) RETURNING id",(qtext,))
        qid=cur.fetchone()[0]
    for text, careers_for_opt, weights in opts:
        cur.execute("SELECT id FROM quiz_options WHERE question_id=%s AND option_text=%s",(qid,text))
        row=cur.fetchone()
        if row: oid=row[0]
        else:
            cur.execute("INSERT INTO quiz_options(question_id,option_text) VALUES(%s,%s) RETURNING id",(qid,text))
            oid=cur.fetchone()[0]
        for cname, weight in zip(careers_for_opt,weights):
            cur.execute("""
                INSERT INTO option_career_weights(option_id,career_id,weight)
                VALUES(%s,%s,%s)
                ON CONFLICT (option_id,career_id) DO UPDATE SET weight=EXCLUDED.weight
            """,(oid,career_map[cname],weight))

competitions = [
("SOF International Mathematics Olympiad","Olympiad","6-12","Mathematics","2026-11-15","School-level mathematics olympiad opportunity.","https://sofworld.org/imo"),
("SOF National Science Olympiad","Olympiad","1-12","Science","2026-11-20","Science olympiad for school students.","https://sofworld.org/nso"),
("KVPY / INSPIRE-style Science Opportunities","Scholarship","9-12","Science","2026-12-10","Example science opportunity slot for the PathFinder demo database.","https://online-inspire.gov.in/"),
("CBSE Expression Series","Competition","6-12","All","2026-10-15","Creative writing and expression opportunity; verify the current notice before applying.","https://www.cbse.gov.in/"),
]
for c in competitions:
    cur.execute("""
    INSERT INTO competitions(name,type,class_level,interest,deadline,description,website)
    VALUES(%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING
    """,c)

conn.commit()
cur.close()
conn.close()
print("PathFinder sample data loaded.")
print("Admin login: admin@pathfinder.local / admin123")
