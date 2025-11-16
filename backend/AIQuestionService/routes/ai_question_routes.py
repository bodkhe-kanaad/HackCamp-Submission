from flask import Blueprint, jsonify, request
from backend.AIQuestionService.ai_question_service import (
    get_ai_question_for_user,
    check_ai_answer,
    generate_ai_question_for_pair
)

ai_bp = Blueprint("ai_bp", __name__)


@ai_bp.get("/ai/todays-task/<int:user_id>")
def ai_todays_task(user_id):
    q = get_ai_question_for_user(user_id)
    if q is None:
        return jsonify({"error": "no AI question available"}), 404
    return jsonify(q)


@ai_bp.post("/ai/check-answer")
def ai_check_answer():
    data = request.json
    result = check_ai_answer(
        data["user_id"],
        data["question_id"],
        data["choice"]
    )
    return jsonify({"correct": result})


@ai_bp.post("/ai/generate")
def ai_generate():
    data = request.json
    qid = generate_ai_question_for_pair(
        data["pair_id"],
        data["course"],
        data["week"]
    )
    return jsonify({"question_id": qid})