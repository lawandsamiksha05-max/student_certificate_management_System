import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",         # Change if database is hosted online
            user="root",              # Your MySQL username (default is root)
            password="root123", # Your MySQL password
            database="student_certificate_system"        # Name of your SCMS database
        )
        if connection.is_connected():
            print("Successfully connected to the SCMS database!")
            return connection

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# To test the connection immediately
if __name__ == "__main__":
    conn = create_db_connection()
    if conn:
        conn.close()
