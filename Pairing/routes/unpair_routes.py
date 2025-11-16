from flask import Blueprint, request, jsonify
from db import get_connection

unpair_bp = Blueprint("unpair_bp", __name__)

@unpair_bp.post("/unpair")
def unpair():
    data = request.json
    user_id = data.get("user_id")

    conn = get_connection()
    cur = conn.cursor()

    # 1. Check if the user exists
    cur.execute("SELECT partner_id FROM users WHERE id = %s;", (user_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return jsonify({"error": "user not found"}), 404

    partner_id = row[0]

    # 2. If user is already unpaired
    if partner_id is None:
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": "user already unpaired"})

    # 3. Check if partner still exists (important!)
    cur.execute("SELECT id FROM users WHERE id = %s;", (partner_id,))
    partner_row = cur.fetchone()

    # If partner user no longer exists, just unpair the main user
    if not partner_row:
        cur.execute("UPDATE users SET partner_id = NULL WHERE id = %s;", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": "partner missing; user unpaired"})

    # 4. Safe reciprocal unpairing
    cur.execute("UPDATE users SET partner_id = NULL WHERE id = %s;", (user_id,))
    cur.execute("UPDATE users SET partner_id = NULL WHERE id = %s;", (partner_id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"success": True})