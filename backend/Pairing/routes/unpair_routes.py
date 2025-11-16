from flask import Blueprint, request, jsonify
from backend.Pairing.pairing_service import unpair_user

unpair_bp = Blueprint("unpair_bp", __name__)

@unpair_bp.post("/unpair")
def unpair():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400

    result = unpair_user(user_id)
    return jsonify(result)