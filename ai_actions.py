# =========================================================
# ai_actions.py
# AI Action Detector
# =========================================================


def detect_action(question):

    if not question:
        return "unknown"


    q = question.lower().strip()


    # =====================================================
    # GREETING
    # =====================================================

    if q in [
        "hi",
        "hello",
        "hey",
        "hii",
        "helo",
        "good morning",
        "good afternoon"
    ]:
        return "greeting"



    # =====================================================
    # IDENTITY
    # =====================================================

    if any(x in q for x in [
        "who are you",
        "what are you",
        "your name"
    ]):
        return "identity"



    # =====================================================
    # THANKS
    # =====================================================

    if any(x in q for x in [
        "thanks",
        "thank you",
        "thankyou"
    ]):
        return "thanks"



    # =====================================================
    # GOODBYE
    # =====================================================

    if any(x in q for x in [
        "bye",
        "goodbye"
    ]):
        return "goodbye"



    # =====================================================
    # HELP
    # =====================================================

    if any(x in q for x in [
        "help",
        "what can you do",
        "features"
    ]):
        return "help"



    # =====================================================
    # NAVIGATION
    # =====================================================

    if "open" in q and "student" in q:
        return "open_students"


    if "open" in q and "certificate" in q:
        return "open_certificates"


    if "open" in q and "report" in q:
        return "open_reports"


    if "open" in q and "dashboard" in q:
        return "open_dashboard"



    # =====================================================
    # ADD RECORDS
    # =====================================================

    if any(x in q for x in [
        "add student",
        "new student",
        "create student"
    ]):
        return "add_student"



    if any(x in q for x in [
        "add certificate",
        "new certificate",
        "create certificate"
    ]):
        return "add_certificate"



    # =====================================================
    # STUDENT COUNT
    # =====================================================

    if any(x in q for x in [
        "how many students",
        "total students",
        "student count",
        "number of students"
    ]):
        return "student_count"



    # =====================================================
    # CERTIFICATE COUNT
    # =====================================================

    if any(x in q for x in [
        "how many certificates",
        "total certificates",
        "certificate count",
        "number of certificates"
    ]):
        return "certificate_count"



    # =====================================================
    # RECENT DATA
    # =====================================================

    if "recent" in q and "student" in q:
        return "recent_students"


    if "recent" in q and "certificate" in q:
        return "recent_certificates"



    # =====================================================
    # CERTIFICATE STATUS
    # =====================================================

    if "pending" in q and "certificate" in q:
        return "pending_certificates"


    if "generated" in q and "certificate" in q:
        return "generated_certificates"



    # =====================================================
    # STUDENT SEARCH
    # =====================================================

    if any(x in q for x in [
        "find student",
        "search student",
        "show student",
        "student details",
        "student information"
    ]):
        return "student_search"



    # =====================================================
    # CERTIFICATE SEARCH
    # =====================================================

    if any(x in q for x in [
        "find certificate",
        "search certificate",
        "certificate details",
        "certificate information"
    ]):
        return "certificate_search"



    # =====================================================
    # CERTIFICATE FEATURES
    # =====================================================

    if "generate certificate" in q:
        return "generate_certificate"


    if any(x in q for x in [
        "verify certificate",
        "certificate verification",
        "validate certificate"
    ]):
        return "verify_certificate"


    if "qr" in q:
        return "qr_code"


    if "pdf" in q:
        return "certificate_pdf"



    if any(x in q for x in [
        "email certificate",
        "send certificate email",
        "mail certificate"
    ]):
        return "email_certificate"



    if "whatsapp" in q:
        return "whatsapp_certificate"



    # =====================================================
    # PROGRAMMING
    # =====================================================

    if "python" in q:
        return "python_help"


    if "flask" in q:
        return "flask_help"


    if "html" in q:
        return "html_help"


    if "css" in q:
        return "css_help"


    if "javascript" in q or "java script" in q:
        return "javascript_help"



    if any(x in q for x in [
        "mysql",
        "sql",
        "database",
        "db"
    ]):
        return "database_help"



    if any(x in q for x in [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "generative ai"
    ]):
        return "ai_help"



    # =====================================================
    # ALL STUDENTS
    # =====================================================

    if any(x in q for x in [
        "all students",
        "list students",
        "show all students"
    ]):
        return "all_students"



    # =====================================================
    # DEPARTMENT STUDENTS
    # =====================================================

    if any(x in q for x in [

        "students from",
        "students in",
        "department students",

        "computer engineering students",
        "mechanical engineering students",
        "civil engineering students",
        "electrical engineering students",
        "electronic engineering students",
        "information technology students",
        "ai engineering students",

        "show computer engineering",
        "show mechanical engineering",
        "show civil engineering",
        "show electrical engineering",
        "show electronic engineering",
        "show information technology",
        "show ai engineering"

    ]):

        return "department_students"



    # =====================================================
    # REPORTS
    # =====================================================

    if any(x in q for x in [
        "department report",
        "students by department",
        "department wise"
    ]):
        return "department_report"



    if any(x in q for x in [
        "dashboard summary",
        "overall statistics",
        "project statistics"
    ]):
        return "dashboard_summary"



    if any(x in q for x in [
        "today activity",
        "today report",
        "today summary"
    ]):
        return "today_activity"



    if any(x in q for x in [
        "technology used",
        "technologies used",
        "tools used"
    ]):
        return "technology_used"



    if any(x in q for x in [
        "future scope",
        "future improvement",
        "improve project"
    ]):
        return "future_scope"



    # =====================================================
    # UNKNOWN
    # =====================================================

    return "unknown"