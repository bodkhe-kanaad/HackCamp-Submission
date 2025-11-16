from db import get_connection
from backend.db import get_connection

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