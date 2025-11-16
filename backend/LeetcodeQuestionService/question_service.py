from db import get_connection
from db import questions_collection
import random

def get_question_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # Step 1: Check if user already has assigned question
    cur.execute("SELECT todays_question FROM users WHERE id = %s;", (user_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None  # user not found

    assigned_qid = row[0]

    # CASE 1: question already assigned for today
    if assigned_qid is not None:
        q = questions_collection.find_one({"id": assigned_qid})
        if q:
            q["_id"] = str(q["_id"])
            del q["correct_option"]
            cur.close()
            conn.close()
            return q

    # CASE 2: no question assigned → assign a new one
    total = questions_collection.count_documents({})
    idx = random.randint(0, total - 1)
    q = list(questions_collection.find().skip(idx).limit(1))[0]

    # save assigned question id in PostgreSQL
    cur.execute(
        "UPDATE users SET todays_question = %s WHERE id = %s;",
        (q["id"], user_id)
    )
    conn.commit()

    q["_id"] = str(q["_id"])
    del q["correct_option"]

    cur.close()
    conn.close()
    return q