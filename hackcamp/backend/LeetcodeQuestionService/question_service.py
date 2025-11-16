import random
from backend.db import get_connection
from backend.LeetcodeQuestionService.db_mongo import questions_collection

def check_answer(question_id, user_choice, user_id):
    # Fetch the correct answer from MongoDB
    q = questions_collection.find_one({"id": question_id})
    if not q:
        return None  # question not found

    correct = (q["correct_option"] == user_choice)

    # Now update SQL flags for the pair
    conn = get_connection()
    cur = conn.cursor()

    # 1. Get pair and which user they are
    cur.execute(
        "SELECT pair_id FROM users WHERE user_id = %s;",
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
        "SELECT user1, user2, user1_answered, user2_answered, streak FROM pair WHERE pair_id = %s;",
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
            cur.execute("UPDATE pair SET user1_answered = TRUE WHERE pair_id = %s;", (pair_id,))
            u1_done = True
        else:
            cur.execute("UPDATE pair SET user2_answered = TRUE WHERE pair_id = %s;", (pair_id,))
            u2_done = True

    # 4. If BOTH answered correctly → increment streak, reset question
    if u1_done and u2_done:
        cur.execute(
            """
            UPDATE pair
            SET streak = streak + 1,
                question_id = NULL,
                user1_answered = FALSE,
                user2_answered = FALSE
            WHERE pair_id = %s;
            """,
            (pair_id,)
        )

    conn.commit()
    cur.close()
    conn.close()

    return correct


import random
from backend.db import get_connection
from backend.LeetcodeQuestionService.db_mongo import questions_collection


def get_question_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Find user's pair
    cur.execute(
        "SELECT pair_id FROM users WHERE user_id = %s;",
        (user_id,)
    )
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return None  # user not paired or not found

    pair_id = row[0]

    # 2. Check existing question for the pair
    cur.execute(
        """
        SELECT question_id
        FROM pair
        WHERE pair_id = %s;
        """,
        (pair_id,)
    )
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None  # pair not found

    assigned_qid = row[0]

    # CASE 1: question already assigned → return same question
    if assigned_qid is not None:
        q = questions_collection.find_one({"id": assigned_qid})
        if q:
            q["_id"] = str(q["_id"])
            del q["correct_option"]
            cur.close()
            conn.close()
            return q

    # CASE 2: no question assigned → pick new random question
    total = questions_collection.count_documents({})
    if total == 0:
        cur.close()
        conn.close()
        return None

    idx = random.randint(0, total - 1)
    q = list(questions_collection.find().skip(idx).limit(1))[0]
    question_id = q["id"]

    # 3. Save new question into pair table
    cur.execute(
        """
        UPDATE pair
        SET question_id = %s,
            user1_answered = FALSE,
            user2_answered = FALSE
        WHERE pair_id = %s;
        """,
        (question_id, pair_id)
    )
    conn.commit()

    q["_id"] = str(q["_id"])
    del q["correct_option"]

    cur.close()
    conn.close()
    return q