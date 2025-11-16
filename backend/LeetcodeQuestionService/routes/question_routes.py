from flask import Blueprint, jsonify, request
from backend.db import get_connection

# LeetCode question services
from backend.LeetcodeQuestionService.question_service import (
    get_leetcode_question_for_user,
    check_leetcode_answer
)

# AI question services
from backend.AIQuestionService.ai_question_service import (
    get_ai_question_for_user,
    check_ai_answer,
    generate_ai_question_for_pair
)

question_bp = Blueprint("question_bp", __name__)


# ---------------------------------------------------------
# GET /todays-task/<user_id>
# Unified endpoint → decides LeetCode or AI based on ai_mode
# ---------------------------------------------------------
@question_bp.get("/todays-task/<int:user_id>")
def todays_task_route(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # Find pair + mode + question
    cur.execute("""
        SELECT p.pair_id, p.ai_mode, p.question_id
        FROM pair p
        JOIN users u ON u.pair_id = p.pair_id
        WHERE u.user_id = %s;
    """, (user_id,))
    row = cur.fetchone()

    if not row:
        return jsonify({"error": "user not paired"}), 404

    pair_id, ai_mode, current_question_id = row
    cur.close()
    conn.close()

    # -----------------------------------------------------
    # CASE 1 — AI MODE ON
    # -----------------------------------------------------
    if ai_mode:
        q = get_ai_question_for_user(user_id)

        if q:       # already assigned
            return jsonify(q)

        # No AI question yet → generate one
        conn = get_connection()
        cur = conn.cursor()

        # fetch shared courses
        cur.execute("""
            SELECT u1.courses, u2.courses
            FROM users u1
            JOIN users u2 ON u1.pair_id = u2.pair_id
            WHERE u1.user_id=%s AND u2.user_id!=%s;
        """, (user_id, user_id))

        shared = cur.fetchone()
        cur.close()
        conn.close()

        if not shared:
            return jsonify({"error": "Unable to determine shared courses"}), 400

        courses1, courses2 = shared
        shared_courses = list(set(courses1).intersection(courses2))

        if not shared_courses:
            return jsonify({"error": "No shared courses available"}), 400

        # Pick the first one for now
        course = shared_courses[0]
        week = 1     # default unless tracked

        # Generate AI question
        generate_ai_question_for_pair(pair_id, course, week)

        # Return new AI question
        return jsonify(get_ai_question_for_user(user_id))

    # -----------------------------------------------------
    # CASE 2 — NORMAL MODE → LEETCODE QUESTION
    # -----------------------------------------------------
    lc_question = get_leetcode_question_for_user(user_id)

    if lc_question:
        return jsonify(lc_question)

    return jsonify({"error": "no question available"}), 404


# ---------------------------------------------------------
# POST /check-answer
# Determines whether to check LeetCode or AI question
# ---------------------------------------------------------
@question_bp.post("/check-answer")
def check_answer_route():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    question_id = data.get("question_id")
    choice = data.get("choice")

    if not user_id or not question_id or not choice:
        return jsonify({"error": "user_id, question_id, and choice required"}), 400

    try:
        question_id = int(question_id)
    except:
        return jsonify({"error": "question_id must be integer"}), 400

    # Determine whether this is AI or LeetCode question
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT source_type FROM question WHERE id=%s;", (question_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "question not found"}), 404

    source = row[0]  # 'ai' or 'leetcode'

    if source == "leetcode":
        correct = check_leetcode_answer(question_id, choice, user_id)
        return jsonify({"correct": correct})

    if source == "ai":
        correct = check_ai_answer(user_id, question_id, choice)
        return jsonify({"correct": correct})

    return jsonify({"error": "Invalid question source"}), 400


import random
from backend.db import get_connection


def get_leetcode_question_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # Find pair_id
    cur.execute("SELECT pair_id FROM users WHERE user_id=%s;", (user_id,))
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return None

    pair_id = row[0]

    # Check active question
    cur.execute("SELECT question_id FROM pair WHERE pair_id=%s;", (pair_id,))
    assigned = cur.fetchone()[0]

    # CASE 1: Already assigned
    if assigned is not None:
        cur.execute("""
            SELECT id, question, option_A, option_B, option_C, option_D
            FROM question
            WHERE id=%s AND source_type='leetcode';
        """, (assigned,))
        qrow = cur.fetchone()
        cur.close()
        conn.close()

        if not qrow:
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
        SELECT id FROM question
        WHERE source_type='leetcode';
    """)

    ids = [r[0] for r in cur.fetchall()]

    if not ids:
        cur.close()
        conn.close()
        return None

    qid = random.choice(ids)

    cur.execute("""
        SELECT question, option_A, option_B, option_C, option_D
        FROM question
        WHERE id=%s;
    """, (qid,))
    qrow = cur.fetchone()

    # Assign question to pair
    cur.execute("""
        UPDATE pair
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
        FROM question
        WHERE id=%s AND source_type='leetcode';
    """, (question_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None

    correct = (row[0] == choice)

    # Update user1_answered or user2_answered
    cur.execute("SELECT pair_id FROM users WHERE user_id=%s;", (user_id,))
    pid = cur.fetchone()[0]

    # Identify slot
    cur.execute("SELECT user1, user2 FROM pair WHERE pair_id=%s;", (pid,))
    user1, user2 = cur.fetchone()

    if user_id == user1:
        cur.execute("UPDATE pair SET user1_answered=TRUE WHERE pair_id=%s;", (pid,))
    else:
        cur.execute("UPDATE pair SET user2_answered=TRUE WHERE pair_id=%s;", (pid,))

    conn.commit()
    cur.close()
    conn.close()

    return correct