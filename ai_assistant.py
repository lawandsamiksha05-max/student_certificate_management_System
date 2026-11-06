# =========================================================
# ai_assistant.py
# =========================================================

import re

from ai_actions import detect_action

from ai_database import (
    get_student_count,
    get_certificate_count,
    search_student,
    get_recent_students,
    get_recent_certificates,
    search_certificate,
    get_generated_certificates,
    get_pending_certificates,
    get_all_students,
    get_department_report,
    get_today_certificates,
    get_dashboard_summary,
    get_students_by_department
)

from project_knowledge import get_project_answer


# =========================================================
# Extract Student Name
# =========================================================

def extract_name(question):

    question = question.lower().strip()

    patterns = [
        r"find student (.+)",
        r"search student (.+)",
        r"show student (.+)",
        r"student details (.+)",
        r"details of student (.+)",
        r"information of student (.+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, question)

        if match:
            return match.group(1).strip()

    return None



# =========================================================
# Format Students
# =========================================================

def format_students(students):

    if not students:
        return "I couldn't find that student."

    answer = "### Student Information\n\n"

    for student in students:

        answer += f"Name: {student.get('student_name','N/A')}\n"

        if student.get("email"):
            answer += f"Email: {student.get('email')}\n"

        if student.get("mobile"):
            answer += f"Mobile: {student.get('mobile')}\n"

        if student.get("department"):
            answer += f"Department: {student.get('department')}\n"

        if student.get("year"):
            answer += f"Year: {student.get('year')}\n"

        answer += "\n"

    return answer



# =========================================================
# Format Certificates
# =========================================================

def format_certificates(certificates):

    if not certificates:
        return "No certificates found."

    answer = "### Certificates\n\n"

    for certificate in certificates:

        if certificate.get("student_name"):
            answer += f"Student: {certificate['student_name']}\n"

        if certificate.get("certificate_type"):
            answer += f"Type: {certificate['certificate_type']}\n"

        if certificate.get("issue_date"):
            answer += f"Issue Date: {certificate['issue_date']}\n"

        if certificate.get("status"):
            answer += f"Status: {certificate['status']}\n"

        answer += "\n"

    return answer



# =========================================================
# Programming Answers
# =========================================================

def programming_answer(question, topic):

    answers = {

        "python_help":
        """
### Python

Python is a programming language used for:

• Web Development
• Automation
• AI
• Machine Learning
• Data Science
""",

        "flask_help":
        """
### Flask

Flask is a Python framework used to create web applications.

Example:

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"
""",

        "html_help":
        """
### HTML

HTML creates webpage structure.
""",

        "css_help":
        """
### CSS

CSS is used for webpage designing.
""",

        "javascript_help":
        """
### JavaScript

JavaScript makes websites interactive.
""",

        "database_help":
        """
### MySQL

SQL Commands:

SELECT
INSERT
UPDATE
DELETE
JOIN
COUNT
""",

        "ai_help":
        """
### Artificial Intelligence

AI includes:

• Machine Learning
• Deep Learning
• NLP
• Computer Vision
• Generative AI
"""
    }

    return answers.get(topic)



# =========================================================
# Main AI Function
# =========================================================

def get_ai_answer(question):

    if not question:
        return "Please type a question."


    question = question.strip()

    action = detect_action(question)



    # Greeting

    if action == "greeting":

        return """
Hello 👋

I am your AI Certificate Assistant.

I can help with:

• Students
• Certificates
• Reports
• Database
• Python
• Flask
• AI
"""


    # Identity

    if action == "identity":

        return """
I am AI Certificate Assistant.

I help manage Student Certificate System.
"""


    # Thanks

    if action == "thanks":

        return "You're welcome 😊"



    # Student Count

    if action == "student_count":

        count = get_student_count()

        return f"There are {count} students registered."



    # Certificate Count

    if action == "certificate_count":

        count = get_certificate_count()

        return f"There are {count} certificates."



    # Search Student

    if action == "student_search":

        name = extract_name(question)

        students = search_student(name)

        return format_students(students)



    # Search Certificate

    if action == "certificate_search":

        name = extract_name(question)

        certificates = search_certificate(name)

        return format_certificates(certificates)



    # Recent Students

    if action == "recent_students":

        return format_students(
            get_recent_students()
        )



    # Recent Certificates

    if action == "recent_certificates":

        return format_certificates(
            get_recent_certificates()
        )



    # Generated Certificates

    if action == "generated_certificates":

        return format_certificates(
            get_generated_certificates()
        )



    # Pending Certificates

    if action == "pending_certificates":

        return format_certificates(
            get_pending_certificates()
        )



    # All Students

    if action == "all_students":

        return format_students(
            get_all_students()
        )



    # Department Students

    if action == "department_students":

        departments = [
            "Computer Engineering",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering",
            "Electronic Engineering",
            "Information Technology",
            "AI Engineering"
        ]


        found = None


        for dept in departments:

            if dept.lower() in question.lower():

                found = dept
                break



        if not found:

            return "Please specify department name."



        students = get_students_by_department(found)

        return format_students(students)



    # Department Report

    if action == "department_report":

        data = get_department_report()

        answer = "### Department Report\n\n"


        for d in data:

            answer += f"""
Department: {d['department']}

Students: {d['total']}

----------------

"""

        return answer



    # Dashboard

    if action == "dashboard_summary":

        data = get_dashboard_summary()

        return f"""
### Dashboard Summary

Students:
{data['students']}

Certificates:
{data['certificates']}

Pending:
{data['pending']}

Generated:
{data['generated']}
"""



    # Today Activity

    if action == "today_activity":

        data = get_today_certificates()

        return format_certificates(data)



    # Technology Used

    if action == "technology_used":

        return """
### Technologies Used

Backend:
Python Flask

Database:
MySQL

Frontend:
HTML CSS JavaScript Bootstrap

Automation:
Playwright QRCode Flask-Mail
"""



    # Future Scope

    if action == "future_scope":

        return """
### Future Scope

1. Voice AI
2. Face Recognition
3. Mobile Application
4. Cloud Deployment
5. AI Analytics
"""



    # Programming

    result = programming_answer(question, action)

    if result:
        return result



    # Project Knowledge

    result = get_project_answer(question)

    if result:
        return result



    return """
I don't have an answer yet.

Try:

• How many students?
• Show all students
• Department report
• Dashboard summary
• Pending certificates
• Explain Python
• Explain Flask
"""