from flask import Blueprint, request, jsonify
from Pairing.pairing_service import pair_user, get_paired_user

pair_bp = Blueprint("pair_bp", __name__)

@pair_bp.post("/pair")
def pair():
    data = request.json
    user_id = data.get("user_id")

    partner_id = pair_user(user_id)
    return jsonify({"partner_id": partner_id})


@pair_bp.get("/status/<int:user_id>")
def status(user_id):
    partner_id = get_paired_user(user_id)
    return jsonify({"partner_id": partner_id})