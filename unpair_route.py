from flask import Blueprint, request, jsonify
from db import get_connection

unpair_bp = Blueprint("unpair_bp", __name__)

@unpair_bp.post("/unpair")
def unpair():
    data = request.json
    user_id = data.get("user_id")

    conn = get_connection()
    cur = conn.cursor()

    # find the partner
    cur.execute("SELECT partner_id FROM users WHERE id = %s;", (user_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return jsonify({"error": "user not found"}), 404

    partner_id = row[0]

    # if user has no partner
    if partner_id is None:
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": "user already unpaired"})

    # unpair both sides
    cur.execute("UPDATE users SET partner_id = NULL WHERE id = %s OR id = %s;", (user_id, partner_id))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"success": True})