import random
from backend.db import get_connection

def check_answer(question_id, user_choice, user_id):
    # Fetch the correct answer from PostgreSQL
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        'SELECT correct_option FROM "question" WHERE id = %s;',
        (question_id,)
    )
    row = cur.fetchone()
    
    if not row:
        cur.close()
        conn.close()
        return None  # question not found

    correct = (row[0] == user_choice)

    # 1. Get pair and which user they are
    cur.execute(
        'SELECT pair_id FROM "users" WHERE user_id = %s;',
        (user_id,)
    )
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return correct

    pair_id = row[0]

    # 2. Get pair record: who is user1 vs user2
    cur.execute(
        'SELECT user1, user2, user1_answered, user2_answered, streak FROM "Pair" WHERE pair_id = %s;',
        (pair_id,)
    )
    pair_row = cur.fetchone()

    if not pair_row:
        cur.close()
        conn.close()
        return correct

    user1_id, user2_id, u1_done, u2_done, streak = pair_row

    # 3. If answer is correct, update the correct flag
    if correct:
        if user_id == user1_id:
            cur.execute('UPDATE "Pair" SET user1_answered = TRUE WHERE pair_id = %s;', (pair_id,))
            u1_done = True
        else:
            cur.execute('UPDATE "Pair" SET user2_answered = TRUE WHERE pair_id = %s;', (pair_id,))
            u2_done = True

    # 4. If BOTH answered correctly → increment streak, reset question
    if u1_done and u2_done:
        cur.execute(
            '''
            UPDATE "Pair"
            SET streak = streak + 1,
                question_id = NULL,
                user1_answered = FALSE,
                user2_answered = FALSE
            WHERE pair_id = %s;
            ''',
            (pair_id,)
        )

    conn.commit()
    cur.close()
    conn.close()

    return correct


def get_question_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # Step 1. Get pair_id for user
    cur.execute(
        'SELECT pair_id FROM "users" WHERE user_id = %s;',
        (user_id,)
    )
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return None  # user is not paired

    pair_id = row[0]

    # Step 2. Get the pair's current question
    cur.execute(
        'SELECT question_id FROM "Pair" WHERE pair_id = %s;',
        (pair_id,)
    )
    row = cur.fetchone()
    assigned_qid = row[0] if row else None

    # CASE 1. Pair already has a question
    if assigned_qid is not None:
        cur.execute(
            'SELECT id, question, A, B, C, D FROM "question" WHERE id = %s;',
            (assigned_qid,)
        )
        q_row = cur.fetchone()
        if q_row:
            q = {
                "id": q_row[0],
                "question": q_row[1],
                "A": q_row[2],
                "B": q_row[3],
                "C": q_row[4],
                "D": q_row[5]
            }
            cur.close()
            conn.close()
            return q

    # CASE 2. No question assigned → generate one
    cur.execute('SELECT COUNT(*) FROM "question";')
    total = cur.fetchone()[0]
    
    if total == 0:
        cur.close()
        conn.close()
        return None

    cur.execute('SELECT id FROM "question" ORDER BY RANDOM() LIMIT 1;')
    q_row = cur.fetchone()
    question_id = q_row[0]

    # Save assigned question to pair table
    cur.execute(
        'UPDATE "Pair" SET question_id = %s, user1_answered = FALSE, user2_answered = FALSE WHERE pair_id = %s;',
        (question_id, pair_id)
    )
    conn.commit()

    cur.execute(
        'SELECT id, question, A, B, C, D FROM "question" WHERE id = %s;',
        (question_id,)
    )
    q_row = cur.fetchone()
    q = {
        "id": q_row[0],
        "question": q_row[1],
        "A": q_row[2],
        "B": q_row[3],
        "C": q_row[4],
        "D": q_row[5]
    }

    cur.close()
    conn.close()
    return q