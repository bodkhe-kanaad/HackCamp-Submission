import random
from backend.db import get_connection


def get_leetcode_question_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # Find pair_id
    cur.execute('SELECT pair_id FROM "users" WHERE user_id=%s;', (user_id,))
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return None

    pair_id = row[0]

    # Check active question (handle missing row)
    cur.execute('SELECT question_id FROM "Pair" WHERE pair_id=%s;', (pair_id,))
    assigned_row = cur.fetchone()
    assigned = assigned_row[0] if assigned_row else None

    # CASE 1: Already assigned
    if assigned is not None:
        cur.execute("""
            SELECT id, question, a, b, c, d
            FROM "question"
            WHERE id=%s AND source_type='leetcode';
        """, (assigned,))
        qrow = cur.fetchone()

        cur.close()
        conn.close()

        if not qrow:
            # assigned question does not exist, fall through to pick random
            return None

        return {
            "id": qrow[0],
            "question": qrow[1],
            "options": {
                "A": qrow[2],
                "B": qrow[3],
                "C": qrow[4],
                "D": qrow[5]
            }
        }

    # CASE 2: No question → pick random LeetCode question
    cur.execute("""
        SELECT id FROM "question"
        WHERE source_type='leetcode';
    """)

    ids = [r[0] for r in cur.fetchall()]

    if not ids:
        cur.close()
        conn.close()
        return None

    qid = random.choice(ids)

    cur.execute("""
        SELECT question, A, B, C, D
        FROM "question"
        WHERE id=%s;
    """, (qid,))
    qrow = cur.fetchone()

    # Assign question to pair
    cur.execute("""
        UPDATE "Pair"
        SET question_id=%s, user1_answered=FALSE, user2_answered=FALSE
        WHERE pair_id=%s;
    """, (qid, pair_id))

    conn.commit()
    cur.close()
    conn.close()

    return {
        "id": qid,
        "question": qrow[0],
        "options": {
            "A": qrow[1],
            "B": qrow[2],
            "C": qrow[3],
            "D": qrow[4]
        }
    }

def check_leetcode_answer(user_id, question_id, choice):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Fetch pair + flags
    cur.execute("""
        SELECT p.pair_id, p.user1, p.user2,
               p.user1_answered, p.user2_answered
        FROM "Pair" p
        JOIN users u ON u.pair_id = p.pair_id
        WHERE u.user_id = %s;
    """, (user_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None

    pair_id, user1, user2, u1_done, u2_done = row

    # 2. Prevent double-submission
    if (user_id == user1 and u1_done) or (user_id == user2 and u2_done):
        cur.close()
        conn.close()
        return {"error": "already attempted today's task"}

    # 3. Fetch correct answer
    cur.execute("""
        SELECT correct_option
        FROM "question"
        WHERE id = %s AND source_type = 'leetcode';
    """, (question_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None

    correct_option = row[0]
    correct = (correct_option == choice)

    # 4. Mark attempt flag
    if user_id == user1:
        cur.execute("""UPDATE "Pair" SET user1_answered = TRUE WHERE pair_id=%s;""", (pair_id,))
    else:
        cur.execute("""UPDATE "Pair" SET user2_answered = TRUE WHERE pair_id=%s;""", (pair_id,))

    conn.commit()
    cur.close()
    conn.close()

    return {"correct": correct}