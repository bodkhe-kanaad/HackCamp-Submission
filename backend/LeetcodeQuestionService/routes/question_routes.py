from flask import Blueprint, jsonify, request
from backend.LeetcodeQuestionService.question_service import (
    get_question_for_user,
    check_answer
)

question_bp = Blueprint("question_bp", __name__)


# ---------------------------------------------------------
# GET /todays-task/<user_id>
# Returns the same question every time until both users answer
# ---------------------------------------------------------
@question_bp.get("/todays-task/<int:user_id>")
def todays_task_route(user_id):
    question = get_question_for_user(user_id)

    if question is None:
        return jsonify({"error": "no question available"}), 404

    return jsonify(question)


# ---------------------------------------------------------
# POST /check-answer
# user submits answer → updates pair table, streak, resets question
# ---------------------------------------------------------
@question_bp.post("/check-answer")
def check_answer_route():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    question_id = data.get("question_id")
    choice = data.get("choice")

    # Validate
    if user_id is None or question_id is None or choice is None:
        return jsonify({"error": "user_id, question_id, and choice are required"}), 400

    try:
        question_id = int(question_id)
    except:
        return jsonify({"error": "question_id must be an integer"}), 400

    # Call service logic
    result = check_answer(question_id, choice, user_id)

    if result is None:
        return jsonify({"error": "question not found"}), 404

    # result = True or False
    return jsonify({"correct": result})
