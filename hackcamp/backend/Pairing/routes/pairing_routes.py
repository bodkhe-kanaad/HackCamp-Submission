from flask import Blueprint, request, jsonify
from Pairing.pairing_service import pair_user, get_user_pair_status

pair_bp = Blueprint("pair_bp", __name__)


# --------------------------------------------------
# POST /pair
# Pairs a user with the best match
# Returns: pair_id and the matched user_id
# --------------------------------------------------
@pair_bp.post("/pair")
def pair():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400

    pair_id, matched_user_id = pair_user(user_id)

    if pair_id is None:
        return jsonify({
            "pair_id": None,
            "matched_user_id": None,
            "message": "No available users to pair with"
        })

    return jsonify({
        "pair_id": pair_id,
        "matched_user_id": matched_user_id
    })


# --------------------------------------------------
# GET /pair/status/<user_id>
# Returns pair_id and partner_id for frontend
# --------------------------------------------------
@pair_bp.get("/pair/status/<int:user_id>")
def status(user_id):
    result = get_user_pair_status(user_id)

    if result is None:
        return jsonify({"pair_id": None, "partner_id": None})

    return jsonify(result)