# =========================================================
# project_knowledge.py
# Student Certificate System - AI Knowledge
# =========================================================

import re


# =========================================================
# 100+ QUESTIONS / ANSWERS
# =========================================================

KNOWLEDGE = {

    # -----------------------------------------------------
    # GENERAL
    # -----------------------------------------------------

    "hello": "Hello! 👋 I am your Student Certificate AI Assistant. How can I help you today?",

    "hi": "Hi! 🤖 I am ready to help you with students, certificates, reports, database information and programming questions.",

    "hey": "Hey! 👋 Ask me anything about your Student Certificate System.",

    "who are you": "I am the AI Assistant for your Student Certificate Management System. I can help you with students, certificates, reports, database information and project-related questions.",

    "what can you do": "I can search students, check certificate information, count students and certificates, show pending or generated certificates, explain your project, and answer programming questions.",

    "help": "You can ask me questions such as: How many students are there? Show pending certificates. Find student Sayali. How many certificates were generated? Explain the project.",

    "good morning": "Good morning! ☀️ How can I help you today?",

    "good afternoon": "Good afternoon! 🌤️ What would you like to know?",

    "good evening": "Good evening! 🌆 How can I help you?",

    "thank you": "You're welcome! 😊",

    "thanks": "You're welcome! 🤖",

    "bye": "Goodbye! 👋 Have a great day!",

    "goodbye": "Goodbye! 👋 Come back whenever you need help.",


    # -----------------------------------------------------
    # PROJECT
    # -----------------------------------------------------

    "what is this project": "This is a Student Certificate Management System built to manage students, certificates, verification, reports and certificate generation.",

    "project name": "The project is a Student Certificate Management System with an integrated AI Assistant.",

    "what is student certificate system": "It is a system that allows administrators to manage student records, create certificates, generate PDFs, verify certificates and generate reports.",

    "what is the purpose of this project": "The purpose is to reduce manual certificate management and provide a centralized system for student and certificate records.",

    "what technology is used": "The project uses Python, Flask, MySQL, HTML, CSS, JavaScript and Playwright. It also uses QR codes and email functionality.",

    "which language is used": "Python is the main backend programming language. HTML, CSS and JavaScript are used for the frontend, while MySQL is used for the database.",

    "what is flask": "Flask is a lightweight Python web framework used to create the web application and API routes.",

    "what is mysql": "MySQL is the relational database used to store student, certificate and administrator information.",

    "what is html": "HTML is used to create the structure of the web pages.",

    "what is css": "CSS is used to design and style the user interface.",

    "what is javascript": "JavaScript is used to make the web interface interactive.",

    "what is python": "Python is a high-level programming language used in this project for Flask, database operations, automation and AI logic.",


    # -----------------------------------------------------
    # STUDENTS
    # -----------------------------------------------------

    "student management": "The student management section allows the administrator to add, search, edit and delete student records.",

    "how to add student": "Open the Students section, choose Add Student, enter enrollment number, name, department, year, mobile and email, then save the record.",

    "how to edit student": "Open the Students page, find the student and choose Edit. Update the information and save it.",

    "how to delete student": "Open the Students page, select the student and use the Delete option.",

    "student information": "Student information includes enrollment number, student name, department, year, mobile number and email.",

    "student details": "You can ask me for a student's details by saying something like 'Find student Sayali'.",

    "student enrollment": "The enrollment number uniquely identifies a student in the system.",

    "student department": "The department field stores the student's academic department.",

    "student year": "The year field stores the student's academic year.",

    "student email": "The email field stores the student's email address and can be used for certificate communication.",

    "student mobile": "The mobile field stores the student's phone number.",


    # -----------------------------------------------------
    # CERTIFICATES
    # -----------------------------------------------------

    "certificate management": "The certificate management section allows administrators to create, edit, delete, generate and verify certificates.",

    "how to add certificate": "Open the Certificates section, choose Add Certificate, select a student, choose the certificate type, enter the issue date and status, then save it.",

    "how to edit certificate": "Open the Certificates page and choose Edit for the certificate you want to modify.",

    "how to delete certificate": "Open the Certificates page and use the Delete option for the certificate.",

    "certificate types": "The system can support certificate types such as Internship Certificate, Bonafide Certificate, College Leaving Certificate and Scholarship Certificate.",

    "internship certificate": "An Internship Certificate confirms that a student completed an internship or training program.",

    "bonafide certificate": "A Bonafide Certificate confirms that a student is officially associated with the educational institution.",

    "college leaving certificate": "A College Leaving Certificate records that a student has left the institution.",

    "scholarship certificate": "A Scholarship Certificate can be used to provide official information related to a student's scholarship.",

    "certificate status": "Certificates can have statuses such as Pending and Generated.",

    "pending certificate": "A Pending certificate is a certificate record that has not yet been generated.",

    "generated certificate": "A Generated certificate has been successfully created as a certificate document.",

    "certificate pdf": "The system uses Playwright to render the certificate HTML and generate a PDF.",

    "certificate generation": "Certificate generation retrieves student and certificate information, renders the appropriate certificate template and creates a PDF.",


    # -----------------------------------------------------
    # QR / VERIFICATION
    # -----------------------------------------------------

    "what is qr code": "A QR code provides a quick way to access certificate verification information.",

    "why qr code": "The QR code helps users verify whether a certificate exists in the system.",

    "certificate verification": "Certificate verification allows a user to enter or scan certificate information and check the certificate record.",

    "how to verify certificate": "Open the verification page and enter the certificate ID, or use the certificate QR code when available.",

    "is certificate verification online": "The verification page is part of the Flask web application and can check certificate information stored in MySQL.",


    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    "database": "The project uses MySQL database named student_certificate_system.",

    "database name": "The database name used by the project is student_certificate_system.",

    "student table": "The students table stores student records such as enrollment number, name, department, year, mobile and email.",

    "certificate table": "The certificates table stores certificate information such as student ID, certificate type, issue date, status and remarks.",

    "admin table": "The admin table stores administrator login information used by the login system.",

    "what is primary key": "A primary key uniquely identifies each record in a database table.",

    "what is foreign key": "A foreign key connects a record in one table with a related record in another table.",

    "student certificate relationship": "The certificates table uses student_id to connect a certificate with a student in the students table.",

    "what is sql": "SQL stands for Structured Query Language. It is used to create, read, update and delete database records.",

    "select query": "A SELECT query retrieves data from a database table.",

    "insert query": "An INSERT query adds a new record to a database table.",

    "update query": "An UPDATE query modifies an existing database record.",

    "delete query": "A DELETE query removes a database record.",

    "join query": "A JOIN combines related records from multiple database tables.",


    # -----------------------------------------------------
    # REPORTS
    # -----------------------------------------------------

    "reports": "The system contains reports for students, certificates, departments, dates, statuses and certificate types.",

    "student report": "The Student Report displays student information including enrollment number, name, department, year, mobile and email.",

    "certificate report": "The Certificate Report displays certificate ID, student name, certificate type, issue date and status.",

    "department report": "The Department Report groups students by department and shows the number of students in each department.",

    "date report": "The Date Report displays certificate records ordered by issue date.",

    "status report": "The Status Report can display certificates according to their status, such as Generated or Pending.",

    "top certificate report": "The Top Certificate Report groups certificates by certificate type and shows how many of each type exist.",


    # -----------------------------------------------------
    # EMAIL
    # -----------------------------------------------------

    "email": "The project uses Flask-Mail to send generated certificates through email.",

    "how email works": "After certificate generation, the system can attach the generated PDF and send it to the student's email address.",

    "certificate email": "The generated certificate PDF can be attached to an email and sent to the student's registered email address.",


    # -----------------------------------------------------
    # AI ASSISTANT
    # -----------------------------------------------------

    "ai assistant": "The AI Assistant is an intelligent interface that allows administrators to ask questions about the Student Certificate Management System.",

    "how ai assistant works": "The assistant receives the question, detects its intent, retrieves database information when required, and generates a readable answer.",

    "what questions can i ask": "You can ask about students, certificates, pending certificates, generated certificates, reports, database information, project features and programming topics.",

    "is ai connected to database": "Yes. The AI Assistant can use the MySQL database functions to answer questions about actual students and certificates.",

    "can ai search students": "Yes. You can ask me to find a student by name, enrollment number or department.",

    "can ai search certificates": "Yes. You can ask me to search certificates by student, certificate type or status.",


    # -----------------------------------------------------
    # PYTHON
    # -----------------------------------------------------

    "python variables": "A Python variable stores a value. Example: name = 'Student'.",

    "python list": "A Python list is an ordered, mutable collection. Example: students = ['A', 'B', 'C'].",

    "python tuple": "A tuple is an ordered collection that cannot normally be changed after creation.",

    "python dictionary": "A dictionary stores data as key-value pairs. Example: student = {'name': 'Sayali', 'year': 3}.",

    "python loop": "Python loops repeat a block of code. Common loops are for and while.",

    "python function": "A Python function is a reusable block of code defined using the def keyword.",

    "python class": "A Python class is a blueprint for creating objects and combining data with related methods.",

    "python oop": "Object-oriented programming organizes software around classes and objects.",

    "python exception": "Exception handling allows a program to handle runtime errors using try, except, else and finally.",


    # -----------------------------------------------------
    # FLASK
    # -----------------------------------------------------

    "flask route": "A Flask route connects a URL to a Python function using the @app.route decorator.",

    "flask template": "Flask uses templates to generate HTML pages dynamically.",

    "flask session": "A Flask session can store information between requests, such as the logged-in administrator.",

    "flask jsonify": "jsonify converts Python data into a JSON response that can be sent to a browser or frontend application.",

    "flask post": "A POST request is commonly used to send form or JSON data from the frontend to the Flask backend.",

    "flask get": "A GET request is commonly used to retrieve information from the Flask application.",


    # -----------------------------------------------------
    # HTML / CSS / JAVASCRIPT
    # -----------------------------------------------------

    "html form": "An HTML form collects user input and sends it to the backend.",

    "css flexbox": "Flexbox is a CSS layout system used to arrange elements in rows or columns.",

    "css grid": "CSS Grid is a two-dimensional layout system useful for building structured interfaces.",

    "javascript fetch": "The JavaScript fetch API can send HTTP requests to Flask routes without reloading the page.",

    "ajax": "AJAX allows a webpage to communicate with the server asynchronously.",


    # -----------------------------------------------------
    # SECURITY
    # -----------------------------------------------------

    "password security": "Passwords should ideally be stored using secure password hashing rather than plain text.",

    "sql injection": "SQL injection is a security problem caused by unsafe construction of SQL queries. Parameterized queries help prevent it.",

    "login security": "A secure login system should use hashed passwords, sessions, validation and proper authorization checks.",


    # -----------------------------------------------------
    # PROJECT FEATURES
    # -----------------------------------------------------

    "dashboard": "The dashboard displays important statistics such as total students, total certificates, pending certificates and generated certificates.",

    "admin login": "The administrator must log in before accessing protected management pages.",

    "logout": "The logout feature removes the administrator session and returns to the login page.",

    "excel upload": "The project can import student records from an Excel file using pandas.",

    "pandas": "Pandas is a Python library used in the project to read and process Excel data.",

    "playwright": "Playwright is used to render the certificate HTML page and generate a PDF.",

    "qrcode python": "The qrcode Python package is used to generate QR code images.",

    "flask mail": "Flask-Mail provides email integration for sending generated certificates.",


    # -----------------------------------------------------
    # TROUBLESHOOTING
    # -----------------------------------------------------

    "module not found": "A ModuleNotFoundError usually means Python cannot find a required Python module or local project file. Check the filename, project folder and installed packages.",

    "database connection error": "Check that MySQL is running, the database name is correct, and the username and password match your MySQL configuration.",

    "flask page blank": "A blank Flask page can be caused by a template error, JavaScript error, missing CSS or an exception in the Flask route. Check the terminal for the actual error.",

    "404 error": "A 404 error means Flask could not find a matching route or the requested static/template resource.",

    "500 error": "A 500 error usually means an exception occurred in the Flask backend. Check the terminal traceback for the exact problem.",

}


# =========================================================
# NORMALIZE QUESTION
# =========================================================

def normalize(text):

    text = text.lower().strip()

    text = re.sub(r"[?!.,]+", "", text)

    text = re.sub(r"\s+", " ", text)

    return text


# =========================================================
# FIND PROJECT ANSWER
# =========================================================

def get_project_answer(question):

    q = normalize(question)

    # Exact match
    if q in KNOWLEDGE:
        return KNOWLEDGE[q]

    # Partial match
    for key, answer in KNOWLEDGE.items():

        if key in q:
            return answer

    return None