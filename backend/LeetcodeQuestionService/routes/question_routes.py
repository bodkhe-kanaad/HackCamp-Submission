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
        FROM "Pair" p
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


