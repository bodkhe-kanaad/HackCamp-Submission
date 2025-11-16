from flask import Blueprint, request, jsonify
from backend.db import get_connection

mode_bp = Blueprint("mode_bp", __name__)

@mode_bp.post("/pair/toggle-mode")
def toggle_mode():
    data = request.json
    user_id = data.get("user_id")
    ai_mode = data.get("ai_mode")   # boolean true or false

    if user_id is None or ai_mode is None:
        return jsonify({"error": "user_id and ai_mode required"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Find pair
    cur.execute("SELECT pair_id FROM users WHERE user_id = %s;", (user_id,))
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return jsonify({"error": "user is not paired"}), 400

    pair_id = row[0]

    # Update mode
    cur.execute("""
        UPDATE Pair
        SET ai_mode = %s
        WHERE pair_id = %s;
    """, (ai_mode, pair_id))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"success": True, "ai_mode": ai_mode})