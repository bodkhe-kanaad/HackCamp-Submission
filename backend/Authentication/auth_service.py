from db import get_connection
from backend.db import get_connection
import uuid

def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    # teammate will make the correct table and insert data
    cur.execute(
        "SELECT user_id FROM users WHERE username = %s AND password = %s;",
        (username, password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    # Return True if user exists, False otherwise
    return user is not None


def create_user(data):
    username = data.get("username")
    password = data.get("password")
    interests = data.get("interests", [])
    courses = data.get("courses", [])

    if not username or not password:
        return False, "Username and password required", None

    if not isinstance(interests, list):
        interests = []
    if not isinstance(courses, list):
        courses = []

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT 1 FROM "users" WHERE username = %s;', (username,))
        if cur.fetchone():
            return False, "Username already exists", None

        user_id = str(uuid.uuid4())

        cur.execute("""
            INSERT INTO "users" (user_id, username, password, interests, courses)
            VALUES (%s, %s, %s, %s, %s);
        """, (user_id, username, password, interests, courses))

        conn.commit()
        return True, "User created successfully", user_id
    except Exception as e:
        conn.rollback()
        return False, str(e), None
    finally:
        cur.close()
        conn.close()