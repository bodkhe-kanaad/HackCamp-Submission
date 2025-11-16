from backend.db import get_connection
from AIQuestionService.llm_client import generate_llm_question
from AIQuestionService.ensemble_selector import choose_best_learning_goal


def generate_ai_question_for_pair(pair_id, course, week):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Choose best learning goal (RAG + ML + embeddings)
    learning_goal = choose_best_learning_goal(course, week)

    # 2. Generate question using local LLM
    qa = generate_llm_question(learning_goal)

    # 3. Store into shared question table
    cur.execute("""
        INSERT INTO question (question, option_A, option_B, option_C, option_D, correct_option, source_type)
        VALUES (%s, %s, %s, %s, %s, %s, 'ai')
        RETURNING id;
    """, (
        qa["question"], qa["A"], qa["B"], qa["C"], qa["D"], qa["correct"]
    ))

    qid = cur.fetchone()[0]

    # 4. Assign to pair
    cur.execute("""
        UPDATE pair
        SET question_id = %s,
            user1_answered = FALSE,
            user2_answered = FALSE
        WHERE pair_id = %s;
    """, (qid, pair_id))

    conn.commit()
    cur.close()
    conn.close()

    return qid


def get_ai_question_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.question_id
        FROM pair p
        JOIN users u ON u.pair_id = p.pair_id
        WHERE u.user_id = %s;
    """, (user_id,))
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return None

    qid = row[0]

    cur.execute("""
        SELECT question, option_A, option_B, option_C, option_D
        FROM question
        WHERE id = %s;
    """, (qid,))
    q = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "id": qid,
        "question": q[0],
        "options": {
            "A": q[1], "B": q[2], "C": q[3], "D": q[4]
        }
    }


def check_ai_answer(user_id, question_id, choice):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Get correct answer for feedback only
    cur.execute("""
        SELECT correct_option
        FROM question
        WHERE id=%s AND source_type='ai';
    """, (question_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None

    correct = (row[0] == choice)

    # 2. Get pair_id
    cur.execute("SELECT pair_id FROM users WHERE user_id=%s;", (user_id,))
    pid = cur.fetchone()[0]

    # 3. Identify user slot (user1 or user2)
    cur.execute("""
        SELECT user1, user2
        FROM pair
        WHERE pair_id=%s;
    """, (pid,))
    user1, user2 = cur.fetchone()

    # 4. Mark ATTEMPT — not correctness
    if user_id == user1:
        cur.execute("UPDATE pair SET user1_answered = TRUE WHERE pair_id=%s;", (pid,))
    else:
        cur.execute("UPDATE pair SET user2_answered = TRUE WHERE pair_id=%s;", (pid,))

    conn.commit()
    cur.close()
    conn.close()

    return correct