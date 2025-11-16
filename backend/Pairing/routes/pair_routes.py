from flask import Blueprint, jsonify
from backend.Pairing.pairing_service import get_pairmate_details

pair_bp = Blueprint("pair_bp", __name__)

@pair_bp.get("/pair/mate/<int:user_id>")
def pairmate_info(user_id):
    result = get_pairmate_details(user_id)

    if result is None:
        return jsonify({"error": "User is not paired"}), 404

    return jsonify(result)