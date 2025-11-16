
from flask import Blueprint, jsonify, request
from backend.db import get_connection

# AI and LeetCode logic
from backend.AIQuestionService.ai_question_service import (
    get_ai_question_for_user,
    generate_ai_question_for_pair,
    check_ai_answer
)

from backend.LeetcodeQuestionService.question_service import (
    get_leetcode_question_for_user,
    check_leetcode_answer
)

question_bp = Blueprint("question_bp", __name__)


# ---------------------------------------------------------
# GET /todays-task/<user_id>
# Unified endpoint → chooses AI or LeetCode + prevents repeat attempts
# ---------------------------------------------------------
@question_bp.get("/todays-task/<int:user_id>")
def todays_task_route(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Get pair info
    cur.execute("""
        SELECT p.pair_id, p.ai_mode, p.question_id,
               p.user1, p.user2,
               p.user1_answered, p.user2_answered
        FROM "Pair" p
        JOIN users u ON u.pair_id = p.pair_id
        WHERE u.user_id = %s;
    """, (user_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return jsonify({"error": "user not paired"}), 404

    (pair_id, ai_mode, current_qid,
     user1, user2, user1_answered, user2_answered) = row

    # 2. Prevent double-attempting
    if (user_id == user1 and user1_answered) or (user_id == user2 and user2_answered):
        cur.close()
        conn.close()
        return jsonify({"error": "already attempted today's task"}), 403

    cur.close()
    conn.close()

    # =========================================================
    # CASE 1 — AI MODE
    # =========================================================
    if ai_mode:
        q = get_ai_question_for_user(user_id)

        if q:  # Question already exists & user hasn't attempted
            return jsonify(q)

        # Need to generate the first AI question
        conn = get_connection()
        cur = conn.cursor()

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

        course = shared_courses[0]
        week = 2  # default

        generate_ai_question_for_pair(pair_id, course, week)

        return jsonify(get_ai_question_for_user(user_id))

    # =========================================================
    # CASE 2 — LEETCODE MODE
    # =========================================================
    q = get_leetcode_question_for_user(user_id)

    if q:
        return jsonify(q)
    return jsonify(get_leetcode_question_for_user(user_id))

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


