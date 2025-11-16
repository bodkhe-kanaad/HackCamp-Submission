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
    return user


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

        cur.execute("""
            INSERT INTO "users" (username, password, interests, courses)
            VALUES (%s, %s, %s, %s);
        """, (username, password, interests, courses))
        cur.execute('SELECT user_id FROM "users" WHERE username = %s;', (username,))
        conn.commit()
        user_id = cur.fetchone()[0]
        return True, "User created successfully", user_id
    except Exception as e:
        conn.rollback()
        return False, str(e), None
    finally:
        cur.close()
        conn.close()


def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        'SELECT user_id, courses, interests, pair_id FROM "users" WHERE user_id = %s;',
        (user_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "user_id": row[0],
        "courses": row[1] or [],
        "interests": row[2] or [],
        "pair_id": row[3]
    }