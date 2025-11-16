from flask import Blueprint, jsonify
from backend.Leaderboard.leaderboard_service import (
    update_streaks_for_all_pairs,
    get_leaderboard
)

leaderboard_bp = Blueprint("leaderboard_bp", __name__)

@leaderboard_bp.get("/leaderboard")
def leaderboard_route():
    # Update streaks before displaying

    board = get_leaderboard()
    return jsonify(board)

@leaderboard_bp.route("/streak/<int:user_id>")
def get_user_streak_route(user_id):
    streak = get_user_streak(user_id)
    if streak is not None:
        return jsonify(streak)
    else:
        return jsonify({"error": "User not found"}), 404