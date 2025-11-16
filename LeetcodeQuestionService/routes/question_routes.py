from flask import Blueprint, jsonify, request
from question_service import get_random_question, check_answer

question_bp = Blueprint("question_bp", __name__)

@question_bp.get("/question")
def question_route():
    question = get_random_question()
    if question is None:
        return jsonify({"error": "no questions available"}), 404
    return jsonify(question)

@question_bp.post("/check-answer")
def check_answer_route():
    data = request.get_json(silent=True) or {}
    question_id = data.get("question_id")
    choice = data.get("choice")

    if question_id is None or choice is None:
        return jsonify({"error": "question_id and choice are required"}), 400

    try:
        question_id = int(question_id)
    except (TypeError, ValueError):
        return jsonify({"error": "question_id must be an integer"}), 400

    result = check_answer(question_id, choice)

    if result is None:
        return jsonify({"error": "question not found"}), 404

    return jsonify({"correct": result})
