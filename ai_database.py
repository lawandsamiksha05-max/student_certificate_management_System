# =========================================================
# ai_database.py
# Student Certificate System - Database AI
# =========================================================

import mysql.connector


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="student_certificate_system"
    )


# =========================================================
# FETCH FUNCTIONS
# =========================================================

def fetch_all(query, params=()):

    db = None
    cursor = None

    try:

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(query, params)

        return cursor.fetchall()

    except Exception as e:

        print("Database Error:", e)
        return []

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()



def fetch_one(query, params=()):

    db = None
    cursor = None

    try:

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(query, params)

        return cursor.fetchone()

    except Exception as e:

        print("Database Error:", e)
        return None


    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()



# =========================================================
# STUDENT COUNT
# =========================================================

def get_student_count():

    result = fetch_one("""
        SELECT COUNT(*) AS total
        FROM students
    """)

    return result["total"] if result else 0



# =========================================================
# CERTIFICATE COUNT
# =========================================================

def get_certificate_count():

    result = fetch_one("""
        SELECT COUNT(*) AS total
        FROM certificates
    """)

    return result["total"] if result else 0



# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student(name):

    return fetch_all("""
        SELECT
            student_id,
            enrollment_no,
            student_name,
            department,
            year,
            mobile,
            email
        FROM students

        WHERE student_name LIKE %s
        OR enrollment_no LIKE %s
        OR department LIKE %s

        ORDER BY student_name

    """,(
        f"%{name}%",
        f"%{name}%",
        f"%{name}%"
    ))



# =========================================================
# ALL STUDENTS
# =========================================================

def get_all_students():

    return fetch_all("""
        SELECT
            student_id,
            enrollment_no,
            student_name,
            department,
            year,
            mobile,
            email

        FROM students

        ORDER BY student_name

    """)



# =========================================================
# RECENT STUDENTS
# =========================================================

def get_recent_students(limit=10):

    return fetch_all("""
        SELECT
            student_id,
            enrollment_no,
            student_name,
            department,
            year,
            mobile,
            email

        FROM students

        ORDER BY student_id DESC

        LIMIT %s

    """,(limit,))



# =========================================================
# SEARCH CERTIFICATE
# =========================================================

def search_certificate(value):

    return fetch_all("""

        SELECT

            c.certificate_id,
            s.student_name,
            s.enrollment_no,
            s.department,

            c.certificate_type,
            c.issue_date,
            c.status,
            c.remarks


        FROM certificates c


        JOIN students s

        ON c.student_id=s.student_id



        WHERE s.student_name LIKE %s

        OR s.enrollment_no LIKE %s

        OR c.certificate_type LIKE %s

        OR c.status LIKE %s


        ORDER BY c.certificate_id DESC


    """,(
        f"%{value}%",
        f"%{value}%",
        f"%{value}%",
        f"%{value}%"
    ))



# =========================================================
# RECENT CERTIFICATES
# =========================================================

def get_recent_certificates(limit=10):

    return fetch_all("""

        SELECT

        c.certificate_id,
        s.student_name,
        s.enrollment_no,
        c.certificate_type,
        c.issue_date,
        c.status


        FROM certificates c


        JOIN students s

        ON c.student_id=s.student_id


        ORDER BY c.certificate_id DESC


        LIMIT %s


    """,(limit,))



# =========================================================
# GENERATED CERTIFICATES
# =========================================================

def get_generated_certificates():

    return fetch_all("""

        SELECT

        c.certificate_id,
        s.student_name,
        s.enrollment_no,
        c.certificate_type,
        c.issue_date,
        c.status


        FROM certificates c


        JOIN students s

        ON c.student_id=s.student_id


        WHERE c.status='Generated'


        ORDER BY c.certificate_id DESC


    """)



# =========================================================
# PENDING CERTIFICATES
# =========================================================

def get_pending_certificates():

    return fetch_all("""

        SELECT

        c.certificate_id,
        s.student_name,
        s.enrollment_no,
        c.certificate_type,
        c.issue_date,
        c.status


        FROM certificates c


        JOIN students s

        ON c.student_id=s.student_id


        WHERE c.status='Pending'


        ORDER BY c.certificate_id DESC


    """)



# =========================================================
# CERTIFICATE STATUS COUNT
# =========================================================

def get_certificate_status_count(status):

    result = fetch_one("""

        SELECT COUNT(*) AS total

        FROM certificates

        WHERE status=%s

    """,(status,))


    return result["total"] if result else 0



# =========================================================
# CERTIFICATE TYPE REPORT
# =========================================================

def get_certificate_type_count():

    return fetch_all("""

        SELECT

        certificate_type,

        COUNT(*) AS total


        FROM certificates


        GROUP BY certificate_type


        ORDER BY total DESC


    """)



# =========================================================
# DEPARTMENT REPORT
# =========================================================

def get_department_report():

    return fetch_all("""

        SELECT

        department,

        COUNT(*) AS total


        FROM students


        GROUP BY department


        ORDER BY total DESC


    """)



# =========================================================
# STUDENT BY ENROLLMENT
# =========================================================

def get_student_by_enrollment(enrollment_no):

    return fetch_one("""

        SELECT

        student_id,
        enrollment_no,
        student_name,
        department,
        year,
        mobile,
        email


        FROM students


        WHERE enrollment_no=%s


    """,(enrollment_no,))



# =========================================================
# STUDENT CERTIFICATE HISTORY
# =========================================================

def get_student_certificates(student_name):

    return fetch_all("""

        SELECT

        c.certificate_id,

        s.student_name,

        s.department,

        c.certificate_type,

        c.issue_date,

        c.status


        FROM certificates c


        JOIN students s

        ON c.student_id=s.student_id


        WHERE s.student_name LIKE %s


        ORDER BY c.certificate_id DESC


    """,(f"%{student_name}%",))



# =========================================================
# DASHBOARD SUMMARY
# =========================================================

def get_dashboard_summary():

    return {

        "students": get_student_count(),

        "certificates": get_certificate_count(),

        "pending": get_certificate_status_count("Pending"),

        "generated": get_certificate_status_count("Generated")

    }



# =========================================================
# TODAY CERTIFICATES
# =========================================================

def get_today_certificates():

    return fetch_all("""

        SELECT

        s.student_name,

        c.certificate_type,

        c.issue_date


        FROM certificates c


        JOIN students s

        ON c.student_id=s.student_id


        WHERE DATE(c.issue_date)=CURDATE()


    """)



# =========================================================
# DATABASE TEST
# =========================================================

def test_database():

    try:

        db=get_connection()

        if db.is_connected():

            db.close()

            return True


    except Exception as e:

        print(e)


    return False
def get_students_by_department(department):

    return fetch_all("""
        SELECT
            student_name,
            enrollment_no,
            department,
            year,
            mobile,
            email

        FROM students

        WHERE department LIKE %s

        ORDER BY student_name

    """,(f"%{department}%",))