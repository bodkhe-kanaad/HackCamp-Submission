from backend.db import get_connection
from backend.AIQuestionService.llm_client import generate_llm_question
from backend.AIQuestionService.ensemble_selector import choose_best_learning_goal


# ---------------------------------------------------------
# Helper: normalize LLM QA payload
# ---------------------------------------------------------
def _normalize_llm_qa(raw):
    """
    Accepts whatever generate_llm_question returns and normalizes to:

    {
        "question": str,
        "A": str,
        "B": str,
        "C": str,
        "D": str,
        "correct": "A" | "B" | "C" | "D"
    }
    """

    if raw is None:
        raise ValueError("LLM returned None as QA payload")

    if not isinstance(raw, dict):
        raise ValueError(f"LLM QA payload must be dict, got {type(raw)}: {raw}")

    # Try common shapes

    # Case 1: already in desired format
    if all(k in raw for k in ["question", "A", "B", "C", "D"]) and (
        "correct" in raw or "correct_option" in raw
    ):
        correct = raw.get("correct") or raw.get("correct_option")
        return {
            "question": raw["question"],
            "A": raw["A"],
            "B": raw["B"],
            "C": raw["C"],
            "D": raw["D"],
            "correct": correct,
        }

    # Case 2: options nested under "options" and answer under "answer" / "correct"
    if "question" in raw and "options" in raw:
        opts = raw["options"]
        correct = raw.get("answer") or raw.get("correct") or raw.get("correct_option")

        return {
            "question": raw["question"],
            "A": opts.get("A"),
            "B": opts.get("B"),
            "C": opts.get("C"),
            "D": opts.get("D"),
            "correct": correct,
        }

    # If we get here, we do not know how to interpret the payload
    raise ValueError(f"Unrecognized LLM QA format: {raw}")


# ---------------------------------------------------------
# Generate + store a new AI question for a pair
# ---------------------------------------------------------
def generate_ai_question_for_pair(pair_id, course, week):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Choose best learning goal (RAG + ML + embeddings)
    learning_goal = choose_best_learning_goal(course, week)

    # 2. Generate multiple-choice question using local LLM
    raw_qa = generate_llm_question(learning_goal)

    # Normalize whatever the LLM returned
    qa = _normalize_llm_qa(raw_qa)

    # Extra defensive checks
    if qa["correct"] not in {"A", "B", "C", "D"}:
        raise ValueError(f"LLM returned invalid correct option: {qa['correct']} from payload {raw_qa}")

    # 3. Insert into shared question table
    cur.execute(
        """
        INSERT INTO "question" (question, a, b, c, d, correct_option, source_type)
        VALUES (%s, %s, %s, %s, %s, %s, 'ai')
        RETURNING id;
        """,
        (
            qa["question"],
            qa["A"],
            qa["B"],
            qa["C"],
            qa["D"],
            qa["correct"],
        ),
    )

    qid = cur.fetchone()[0]

    # 4. Assign to pair
    cur.execute(
        """
        UPDATE "Pair"
        SET question_id = %s,
            user1_answered = FALSE,
            user2_answered = FALSE
        WHERE pair_id = %s;
        """,
        (qid, pair_id),
    )

    conn.commit()
    cur.close()
    conn.close()

    return qid


# ---------------------------------------------------------
# Retrieve today's AI question for a user
# ---------------------------------------------------------
def get_ai_question_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT p.question_id
        FROM "Pair" p
        JOIN users u ON u.pair_id = p.pair_id
        WHERE u.user_id = %s;
        """,
        (user_id,),
    )
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return None

    qid = row[0]

    # Fetch question from shared table
    cur.execute(
        """
        SELECT question, a, b, c, d
        FROM "question"
        WHERE id = %s AND source_type = 'ai';
        """,
        (qid,),
    )
    q = cur.fetchone()

    cur.close()
    conn.close()

    if not q:
        return None

    return {
        "id": qid,
        "question": q[0],
        "options": {
            "A": q[1],
            "B": q[2],
            "C": q[3],
            "D": q[4],
        },
    }


# ---------------------------------------------------------
# Record a user's answer attempt (NOT correctness)
# ---------------------------------------------------------
def check_ai_answer(user_id, question_id, choice):
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
        return {"error": "user not in pair"}

    pair_id, user1, user2, u1_done, u2_done = row

    # 2. Prevent double-submission
    if (user_id == user1 and u1_done) or (user_id == user2 and u2_done):
        cur.close()
        conn.close()
        return {"error": "already attempted today's task"}

    # 3. Get correct answer
    cur.execute("""
        SELECT correct_option
        FROM "question"
        WHERE id=%s AND source_type='ai';
    """, (question_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return {"error": "question not found"}

    correct_option = row[0]
    is_correct = (correct_option == choice)

    # 4. Mark attempt
    if user_id == user1:
        cur.execute("""UPDATE "Pair" SET user2_answered = TRUE WHERE pair_id=%s;""", (pair_id,))
    else:
        cur.execute("""UPDATE "Pair" SET user1_answered = TRUE WHERE pair_id=%s;""", (pair_id,))

    conn.commit()
    cur.close()
    conn.close()

    return {"correct": is_correct}