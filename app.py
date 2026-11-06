from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    jsonify,
    make_response
)

from flask_mail import Mail, Message

from ai_assistant import get_ai_answer
from ai_actions import detect_action
import asyncio
from playwright.async_api import async_playwright
import asyncio
import os
import qrcode
import time
import urllib.parse
import pandas as pd
import mysql.connector



app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

app.config["MAIL_USERNAME"] = "lawandsamiksha05@gmail.com"
app.config["MAIL_PASSWORD"] = "cdyu llcl hgtv ddia"

app.config["MAIL_DEFAULT_SENDER"] = "lawandsamiksha05@gmail.com"

mail = Mail(app)


app.secret_key = "student_certificate_secret"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="student_certificate_system"
)

cursor = db.cursor()

if db.is_connected():
    print("✅ MySQL Connected Successfully!")


# ---------------- Login Page ----------------

@app.route("/")
def home():
    return render_template("login.html")


# ---------------- Check Login ----------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    cursor.execute(
        "SELECT * FROM admin WHERE username=%s AND password=%s",
        (username, password)
    )

    admin = cursor.fetchone()

    if admin:
        session["admin"] = username
        return redirect("/dashboard")
    else:
        return render_template(
        "login.html",
        error="Invalid Username or Password!"
    )

# ---------------- Dashboard ----------------

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/")

    # Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Total Certificates
    cursor.execute("SELECT COUNT(*) FROM certificates")
    total_certificates = cursor.fetchone()[0]

    # Pending Certificates
    cursor.execute(
        "SELECT COUNT(*) FROM certificates WHERE status='Pending'"
    )
    pending = cursor.fetchone()[0]

    # Generated Certificates
    cursor.execute(
        "SELECT COUNT(*) FROM certificates WHERE status='Generated'"
    )
    generated = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_certificates=total_certificates,
        pending=pending,
        generated=generated
    )


# ---------------- Logout ----------------

@app.route("/logout")
def logout():

    session.pop("admin", None)
    return redirect("/")

@app.route("/students")
def students():

    if "admin" not in session:
        return redirect("/")

    search = request.args.get("search")

    print("Search =", search)   # Debug

    if search:

        value = "%" + search + "%"

        cursor.execute("""
            SELECT * FROM students
            WHERE enrollment_no LIKE %s
            OR student_name LIKE %s
            OR department LIKE %s
        """, (value, value, value))

    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    print(students)   # Debug

    return render_template(
        "students.html",
        students=students,
        search=search
    )
@app.route("/add_student")
def add_student():

    if "admin" not in session:
        return redirect("/")
    

    return render_template("add_student.html")


@app.route("/save_student", methods=["POST"])
def save_student():

    enrollment_no = request.form["enrollment_no"]
    student_name = request.form["student_name"]
    department = request.form["department"]
    year = request.form["year"]
    mobile = request.form["mobile"]
    email = request.form["email"]

    sql = """
    INSERT INTO students
    (enrollment_no, student_name, department, year,
     mobile, email)

    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (
        enrollment_no,
        student_name,
        department,
        year,
        mobile,
        email
    ))

    db.commit() 
    add_history(
    "Student Added",
    f"Student {student_name} was added."
)

    return redirect("/students")

def add_history(action, details=""):

    db = None
    cursor = None

    try:

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="student_certificate_system"
        )

        cursor = db.cursor()

        admin_name = session.get("admin", "Admin")

        cursor.execute("""
            INSERT INTO activity_history
            (
                admin_name,
                action,
                details
            )
            VALUES (%s, %s, %s)
        """, (
            admin_name,
            action,
            details
        ))

        db.commit()

    except Exception as e:

        print("History Error:", e)

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()

@app.route("/history")
def history():

    if "admin" not in session:
        return redirect("/")

    db = None
    cursor = None

    try:

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="student_certificate_system"
        )

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                admin_name,
                action,
                details,
                action_date
            FROM activity_history
            ORDER BY action_date DESC
        """)

        history_data = cursor.fetchall()

        return render_template(
            "history.html",
            history=history_data
        )

    except Exception as e:

        print("History Page Error:", e)

        return render_template(
            "history.html",
            history=[],
            error=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()
            
@app.route("/edit_student/<int:id>")
def edit_student(id):

    if "admin" not in session:
        return redirect("/")

    cursor.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (id,)
    )

    student = cursor.fetchone()

    return render_template(
        "edit_student.html",
        student=student
    )
@app.route("/update_student", methods=["POST"])
def update_student():

    student_id = request.form["student_id"]
    enrollment_no = request.form["enrollment_no"]
    student_name = request.form["student_name"]
    department = request.form["department"]
    year = request.form["year"]
    email = request.form["email"]
    mobile = request.form["mobile"]

    sql = """
    UPDATE students

    SET

    enrollment_no=%s,
    student_name=%s,
    department=%s,
    year=%s,
    email=%s,
    mobile=%s

    WHERE student_id=%s
    """

    cursor.execute(sql,
    (
        enrollment_no,
        student_name,
        department,
        year,
        email,
        mobile,
        student_id
    ))

    db.commit() 

    add_history(
    "Student Updated",
    f"Student {student_name} was updated."
)

    return redirect("/students")

@app.route("/delete_student/<int:id>")
def delete_student(id):

    if "admin" not in session:
        return redirect("/")

    db = None
    cursor = None

    try:

        # ==========================
        # DATABASE CONNECTION
        # ==========================

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="student_certificate_system"
        )

        cursor = db.cursor(dictionary=True)

        # ==========================
        # GET STUDENT NAME
        # ==========================

        cursor.execute("""
            SELECT student_name
            FROM students
            WHERE student_id = %s
        """, (id,))

        student = cursor.fetchone()

        if not student:
            return redirect("/students")

        student_name = student["student_name"]

        # ==========================
        # DELETE STUDENT
        # ==========================

        cursor.execute("""
            DELETE FROM students
            WHERE student_id = %s
        """, (id,))

        db.commit()

        # ==========================
        # ADD HISTORY
        # ==========================

        add_history(
            "Student Deleted",
            f"Student {student_name} was deleted."
        )

        return redirect("/students")

    except Exception as e:

        if db:
            db.rollback()

        print("Delete Student Error:", e)

        return redirect("/students")

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()

@app.route('/search_student', methods=['GET'])
def search_student():

    if "admin" not in session:
        return redirect("/")

    db = None
    cursor = None

    try:

        # ==========================
        # DATABASE CONNECTION
        # ==========================

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="student_certificate_system"
        )

        cursor = db.cursor(dictionary=True)

        # ==========================
        # SEARCH VALUE
        # ==========================

        search = request.args.get('search', '').strip()

        # ==========================
        # SEARCH STUDENTS
        # ==========================

        if search:

            query = """
                SELECT *
                FROM students
                WHERE enrollment_no LIKE %s
                   OR student_name LIKE %s
                   OR department LIKE %s
                   OR year LIKE %s
                   OR mobile LIKE %s
                ORDER BY student_id DESC
            """

            keyword = "%" + search + "%"

            cursor.execute(
                query,
                (
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    keyword
                )
            )

        else:

            cursor.execute("""
                SELECT *
                FROM students
                ORDER BY student_id DESC
            """)

        students = cursor.fetchall()

        return render_template(
            'search_student.html',
            students=students,
            search=search
        )

    except Exception as e:

        print("Search Student Error:", e)

        return render_template(
            'search_student.html',
            students=[],
            search=search,
            error="Unable to search students."
        )

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()
# ---------------- Certificates ----------------

@app.route("/certificates")
def certificates():

    if "admin" not in session:
        return redirect("/")

    cursor.execute("""
        SELECT
            certificates.certificate_id,
            students.student_name,
            certificates.certificate_type,
            certificates.issue_date,
            certificates.status
        FROM certificates
        JOIN students
        ON certificates.student_id = students.student_id
    """)

    certificates = cursor.fetchall()

    return render_template(
        "certificates.html",
        certificates=certificates
    )

@app.route("/add_certificate")
def add_certificate():

    if "admin" not in session:
        return redirect("/")

    cursor.execute(
        "SELECT student_id, enrollment_no, student_name FROM students"
    )

    students = cursor.fetchall()

    return render_template(
        "add_certificate.html",
        students=students
    )

@app.route("/save_certificate", methods=["POST"])
def save_certificate():

    student_id = request.form["student_id"]
    certificate_type = request.form["certificate_type"]
    issue_date = request.form["issue_date"]
    status = request.form["status"]
    remarks = request.form["remarks"]   # <-- Add this line

    cursor.execute("""
        INSERT INTO certificates
        (student_id, certificate_type, issue_date, status, remarks)

        VALUES (%s,%s,%s,%s,%s)
    """,
    (
        student_id,
        certificate_type,
        issue_date,
        status,
        remarks
    ))

    db.commit()
    certificate_id = cursor.lastrowid

    return redirect("/certificates")
@app.route("/edit_certificate/<int:id>")
def edit_certificate(id):

    if "admin" not in session:
        return redirect("/")

    cursor.execute("""
        SELECT *
        FROM certificates
        WHERE certificate_id=%s
    """, (id,))

    certificate = cursor.fetchone()

    cursor.execute("""
        SELECT student_id, student_name, enrollment_no
        FROM students
    """)

    students = cursor.fetchall()

    return render_template(
        "edit_certificate.html",
        certificate=certificate,
        students=students
    )

@app.route("/update_certificate", methods=["POST"])
def update_certificate():

    certificate_id = request.form["certificate_id"]
    student_id = request.form["student_id"]
    certificate_type = request.form["certificate_type"]
    issue_date = request.form["issue_date"]
    status = request.form["status"]
    remarks = request.form["remarks"]

    cursor.execute("""
        UPDATE certificates

        SET
            student_id=%s,
            certificate_type=%s,
            issue_date=%s,
            status=%s,
            remarks=%s

        WHERE certificate_id=%s
    """,
    (
        student_id,
        certificate_type,
        issue_date,
        status,
        remarks,
        certificate_id
    ))

    db.commit()

    return redirect("/certificates")
@app.route("/delete_certificate/<int:id>")
def delete_certificate(id):

    if "admin" not in session:
        return redirect("/")

    cursor.execute(
        "DELETE FROM certificates WHERE certificate_id=%s",
        (id,)
    )

    db.commit()

    return redirect("/certificates")


@app.route("/generate_certificate/<int:id>")
def generate_certificate(id):

    if "admin" not in session:
        return redirect("/")

    cursor.execute("""
        SELECT
            students.student_name,
            students.email,
            students.mobile
        FROM certificates
        JOIN students
            ON certificates.student_id = students.student_id
        WHERE certificates.certificate_id = %s
    """, (id,))

    student = cursor.fetchone()

    if student is None:
        return "Student not found"

    student_name = student[0]
    student_email = student[1]
    student_mobile = student[2]

    # Generate PDF
    pdf = asyncio.run(create_pdf(id))

    # Save PDF temporarily
    file_path = f"certificate_{id}.pdf"

    with open(file_path, "wb") as f:
        f.write(pdf)

    print("Certificate saved at:", os.path.abspath(file_path))

    # Send Email
    print("Starting email sending...")
    print("Student email:", repr(student_email))

    email_sent = send_certificate_email(
        student_email,
        student_name,
        file_path
    )

    print("EMAIL FUNCTION RESULT:", email_sent)

    # Update certificate status
    cursor.execute("""
        UPDATE certificates
        SET status = 'Generated'
        WHERE certificate_id = %s
    """, (id,))

    db.commit()

    # Add activity history
    add_history(
        "Certificate Generated",
        f"Certificate generated for {student_name}."
    )

    # Return PDF Download
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f'attachment; filename="certificate_{id}.pdf"'
    )

    return response

@app.route("/certificate_pdf/<int:id>")
def certificate_pdf(id):

    cursor.execute("""
        SELECT
            students.student_name,
            students.enrollment_no,
            students.department,
            certificates.certificate_type,
            certificates.issue_date,
            certificates.certificate_id
        FROM certificates
        JOIN students
        ON certificates.student_id = students.student_id
        WHERE certificates.certificate_id=%s
    """, (id,))


    certificate = cursor.fetchone()


    if certificate is None:
        return "Certificate not found"


    certificate_type = certificate[3]


    # Get student name
    student_name = certificate[0]


    print("Student Name:", student_name)



    if certificate_type == "Internship Certificate":

      html = render_template(
        "internship_certificate.html",
        student_name=student_name
    )


    elif certificate_type == "Bonafide Certificate":

      html = render_template(
        "bonafide_certificate.html",
        college_name="SVERI College of Engineering",
        college_address="Pandharpur, Maharashtra",

        student_name=certificate[0],
        enrollment_no=certificate[1],
        department=certificate[2],

        course="Diploma Computer Engineering",
        academic_year="2026-27"
    )
    elif certificate_type == "College Leaving Certificate":

      html = render_template(
        "leaving_certificate.html",

        college_name="SVERI College of Engineering",
        college_address="Pandharpur, Maharashtra",

        student_name=certificate[0],
        enrollment_no=certificate[1],
        department=certificate[2],

        course="Diploma Computer Engineering",

        dob="2005-05-10",
        admission_year="2022",
        leaving_date="2026-08-04",

        issue_date=certificate[4]
    )
    elif certificate_type == "Scholarship Certificate":

      html = render_template(
        "scholarship_certificate.html",
        college_name="SVERI College of Engineering",
        college_address="Pandharpur, Maharashtra",

        student_name=certificate[0],
        enrollment_no=str(certificate[1]).replace(".0", ""),
        department=certificate[2],

        scholarship_id=certificate[5],
        issue_date=certificate[4]
    )
    else:

       html = render_template(
        "certificate_template.html",
        certificate=certificate
    )


    return html



# ---------- PDF GENERATION ----------

async def create_pdf(id):

    async with async_playwright() as p:

        browser = await p.chromium.launch()

        page = await browser.new_page()

        await page.goto(
            f"http://127.0.0.1:5000/certificate_pdf/{id}",
            wait_until="networkidle"
        )

        pdf = await page.pdf(
            format="A4",
            print_background=True
        )

        await browser.close()

        return pdf
# ---------- END ----------

@app.route("/verify_certificate/<int:id>")
def verify_certificate(id):

    cursor.execute("""
        SELECT
            students.student_name,
            students.enrollment_no,
            students.department,
            certificates.certificate_type,
            certificates.issue_date,
            certificates.status

        FROM certificates

        JOIN students
        ON certificates.student_id = students.student_id

        WHERE certificates.certificate_id=%s

    """,(id,))


    certificate = cursor.fetchone()


    if certificate:

        return render_template(
            "verify_certificate.html",
            certificate=certificate
        )

    else:

        return "Invalid Certificate"
    add_history(
    "Certificate Verified",
    f"Certificate verified for {student_name}."
)

def send_certificate_email(email, student_name, pdf_file):
    try:

        print("MAIL USERNAME =", app.config.get("MAIL_USERNAME"))
        print("MAIL PASSWORD =", app.config.get("MAIL_PASSWORD"))

        if not os.path.exists(pdf_file):
            print("Email Error: Certificate PDF file not found")
            return False

        msg = Message(
            subject="Your Certificate",
            recipients=[email]
        )

        msg.body = f"""
       Hello {student_name},

       Congratulations!

      Your certificate has been generated.

      Please find your certificate attached.

      Thank you.
      """

        with open(pdf_file, "rb") as f:
            msg.attach(
                "certificate.pdf",
                "application/pdf",
                f.read()
            )

        mail.send(msg)

        print("✅ Email sent successfully to:", email)

        return True

    except Exception as e:
        print("❌ Email Error:", str(e))
        return False
    # Attach PDF manually using screen coordinates
@app.route("/reports")
def reports():

    if "admin" not in session:
        return redirect("/")

    return render_template("reports.html")

@app.route("/student_report")
def student_report():

    if "admin" not in session:
        return redirect("/")

    cursor.execute("""
        SELECT
            enrollment_no,
            student_name,
            department,
            year,
            mobile,
            email
        FROM students
        ORDER BY student_name
    """)

    students = cursor.fetchall()

    return render_template(
        "student_report.html",
        students=students
    )

@app.route("/certificate_report")
def certificate_report():

    if "admin" not in session:
        return redirect("/")

    cursor.execute("""
        SELECT
            certificates.certificate_id,
            students.student_name,
            certificates.certificate_type,
            certificates.issue_date,
            certificates.status
        FROM certificates
        JOIN students
        ON certificates.student_id = students.student_id
        ORDER BY certificates.certificate_id DESC
    """)

    certificates = cursor.fetchall()

    return render_template(
        "certificate_report.html",
        certificates=certificates
    )

@app.route("/department_report")
def department_report():

    if "admin" not in session:
        return redirect("/")

    cursor.execute("""
        SELECT
            department,
            COUNT(*) AS total_students
        FROM students
        GROUP BY department
        ORDER BY department
    """)

    departments = cursor.fetchall()

    return render_template(
        "department_report.html",
        departments=departments
    )
@app.route('/date-wise-report', methods=['GET', 'POST'])
def date_wise_report():

    certificates = []

    if request.method == 'POST':

        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')

        if from_date and to_date:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root123",
                database="student_certificate_system"
            )

            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    c.certificate_id,
                    s.student_name,
                    c.certificate_type,
                    c.issue_date,
                    c.status
                FROM certificates c
                JOIN students s ON c.student_id = s.student_id
                WHERE DATE(c.issue_date) BETWEEN %s AND %s
                ORDER BY c.issue_date ASC
            """

            cursor.execute(query, (from_date, to_date))

            certificates = cursor.fetchall()

            cursor.close()
            conn.close()

    return render_template(
        'date_wise_report.html',
        certificates=certificates
    )
@app.route("/status_report", methods=["GET", "POST"])
def status_report():

    if "admin" not in session:
        return redirect("/")

    status = "Generated"

    if request.method == "POST":
        status = request.form["status"]

    cursor.execute("""
        SELECT
            c.certificate_id,
            s.student_name,
            c.certificate_type,
            c.issue_date,
            c.status
        FROM certificates c
        INNER JOIN students s
            ON c.student_id = s.student_id
        WHERE c.status = %s
        ORDER BY c.issue_date DESC
    """, (status,))

    reports = cursor.fetchall()

    return render_template(
        "status_report.html",
        reports=reports
    )
@app.route("/top_certificate_report")
def top_certificate_report():

    if "admin" not in session:
        return redirect("/")

    cursor.execute("""
        SELECT
            certificate_type,
            COUNT(*) AS total
        FROM certificates
        GROUP BY certificate_type
        ORDER BY total DESC
    """)

    reports = cursor.fetchall()

    return render_template(
        "top_certificate_report.html",
        reports=reports
    )



# ==============================
# AI ASSISTANT ROUTES
# ==============================


@app.route("/settings")
def settings():

    if "admin" not in session:
        return redirect("/")

    cursor.execute("SELECT * FROM system_settings LIMIT 1")

    data = cursor.fetchone()

    return render_template(
        "settings.html",
        data=data
    )
@app.route("/save_settings", methods=["POST"])
def save_settings():

    if "admin" not in session:
        return redirect("/")

    college_name = request.form["college_name"]
    principal_name = request.form["principal_name"]
    address = request.form["address"]
    phone = request.form["phone"]
    email = request.form["email"]
    certificate_prefix = request.form["certificate_prefix"]
    theme = request.form["theme"]

    email_notification = "Yes" if "email_notification" in request.form else "No"
    whatsapp_notification = "Yes" if "whatsapp_notification" in request.form else "No"

    cursor.execute("""
        UPDATE settings
        SET
            college_name=%s,
            principal_name=%s,
            address=%s,
            phone=%s,
            email=%s,
            certificate_prefix=%s,
            theme=%s,
            email_notification=%s,
            whatsapp_notification=%s
        WHERE id=1
    """,
    (
        college_name,
        principal_name,
        address,
        phone,
        email,
        certificate_prefix,
        theme,
        email_notification,
        whatsapp_notification
    ))

    db.commit()

    return redirect("/settings")

@app.route("/admin_profile")
def admin_profile():

    cursor.execute("SELECT * FROM admin_profile WHERE id=1")
    data = cursor.fetchone()

    return render_template(
        "admin_profile.html",
        data=data
    )


@app.route("/update_admin", methods=["POST"])
def update_admin():

    admin_name = request.form["admin_name"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    password = request.form["password"]

    cursor.execute("""
        UPDATE admin_profile
        SET
            admin_name=%s,
            email=%s,
            mobile=%s,
            password=%s
        WHERE id=1
    """,(admin_name,email,mobile,password))

    db.commit()

    return redirect("/admin_profile")
@app.route("/excel")
def excel():
    return render_template("upload_excel.html")


@app.route("/upload_excel", methods=["POST"])
def upload_excel():

    file = request.files["excel"]

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    df = pd.read_excel(filepath)

    for _, row in df.iterrows():

        cursor.execute("""
INSERT IGNORE INTO students
(enrollment_no, student_name, department, year, email, mobile)
VALUES (%s, %s, %s, %s, %s, %s)
""", (
            str(row["enrollment_no"]),
            str(row["student_name"]),
            str(row["department"]),
            str(row["year"]),
            str(row["email"]) if pd.notna(row["email"]) else "",
            str(row["mobile"]) if pd.notna(row["mobile"]) else ""
        ))

    db.commit()

    return redirect("/students")

# =========================================================
# AI ASSISTANT ROUTES
# =========================================================

@app.route("/ai_assistant")
def ai_assistant():

    if "admin" not in session:
        return redirect("/")

    return render_template("ai_assistant.html")


@app.route("/ask_ai", methods=["POST"])
def ask_ai():

    if "admin" not in session:
        return jsonify({
            "success": False,
            "answer": "Please login first."
        }), 401

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "answer": "Invalid request."
            })

        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "success": False,
                "answer": "Please enter a question."
            })

        # Detect action
        action = detect_action(question)

        print("AI Question:", question)
        print("Detected Action:", action)

        # =================================================
        # OPEN STUDENTS
        # =================================================

        if action in ["open_students", "students"]:

            return jsonify({
                "success": True,
                "answer": "Opening Students page...",
                "action": "open_page",
                "url": "/students"
            })

        # =================================================
        # OPEN CERTIFICATES
        # =================================================

        if action in ["open_certificates", "certificates"]:

            return jsonify({
                "success": True,
                "answer": "Opening Certificates page...",
                "action": "open_page",
                "url": "/certificates"
            })

        # =================================================
        # OPEN REPORTS
        # =================================================

        if action in ["open_reports", "reports"]:

            return jsonify({
                "success": True,
                "answer": "Opening Reports page...",
                "action": "open_page",
                "url": "/reports"
            })

        # =================================================
        # OPEN DASHBOARD
        # =================================================
        if action in ["open_dashboard", "dashboard"]:

            return jsonify({
                "success": True,
                "answer": "Opening Dashboard...",
                "action": "open_page",
                "url": "/dashboard"
            })

        # =================================================
        # OPEN SETTINGS
        # =================================================

        if action == "open_settings":

            return jsonify({
                "success": True,
                "answer": "Opening Settings...",
                "action": "open_page",
                "url": "/settings"
            })

        # =================================================
        # OPEN PROFILE
        # =================================================

        if action == "open_profile":

            return jsonify({
                "success": True,
                "answer": "Opening Admin Profile...",
                "action": "open_page",
                "url": "/admin_profile"
            })

        # =================================================
        # ADD STUDENT
        # =================================================

        if action == "add_student":

            return jsonify({
                "success": True,
                "answer": "Opening Add Student page...",
                "action": "open_page",
                "url": "/add_student"
            })

        # =================================================
        # ADD CERTIFICATE
        # =================================================

        if action == "add_certificate":

            return jsonify({
                "success": True,
                "answer": "Opening Add Certificate page...",
                "action": "open_page",
                "url": "/add_certificate"
            })

        # =================================================
        # EXCEL
        # =================================================

        if action == "excel":

            return jsonify({
                "success": True,
                "answer": "Opening Excel Upload...",
                "action": "open_page",
                "url": "/excel"
            })

        # =================================================
        # NORMAL AI QUESTION
        # =================================================

        answer = get_ai_answer(question)

        return jsonify({
            "success": True,
            "answer": answer,
            "action": "none",
            "url": None
        })

    except Exception as e:

        print("AI ERROR:", e)

        return jsonify({
            "success": False,
            "answer": f"AI Error: {str(e)}"
        }), 500

print("Before app.run()")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)