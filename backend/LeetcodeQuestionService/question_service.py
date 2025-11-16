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


def check_leetcode_answer(question_id, choice, user_id):
    conn = get_connection()
    cur = conn.cursor()

    # Correct option
    cur.execute("""
        SELECT correct_option
        FROM "question"
        WHERE id=%s AND source_type='leetcode';
    """, (question_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None

    correct = (row[0] == choice)

    # Get pair_id for user (handle missing)
    cur.execute('SELECT pair_id FROM "users" WHERE user_id=%s;', (user_id,))
    pid_row = cur.fetchone()
    if not pid_row or pid_row[0] is None:
        cur.close()
        conn.close()
        return None
    pid = pid_row[0]

    # Identify slot (handle missing pair)
    cur.execute('SELECT user1, user2 FROM "Pair" WHERE pair_id=%s;', (pid,))
    pr = cur.fetchone()
    if not pr:
        cur.close()
        conn.close()
        return None
    user1, user2 = pr

    if user_id == user1:
        cur.execute('UPDATE "Pair" SET user1_answered=TRUE WHERE pair_id=%s;', (pid,))
    elif user_id == user2:
        cur.execute('UPDATE "Pair" SET user2_answered=TRUE WHERE pair_id=%s;', (pid,))
    else:
        # user not in pair
        cur.close()
        conn.close()
        return None

    conn.commit()
    cur.close()
    conn.close()

    return correct