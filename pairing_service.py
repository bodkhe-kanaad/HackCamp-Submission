from db import get_connection

# Get a single user's full data
def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, courses, study_time, interests, partner_id FROM users WHERE id = %s;",
        (user_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "courses": row[1] or [],
        "study_time": row[2],
        "interests": row[3] or [],
        "partner_id": row[4]
    }


# Get all users who are unpaired and not the current user
def get_unpaired_users(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, courses, study_time, interests
        FROM users
        WHERE partner_id IS NULL AND id != %s;
        """,
        (user_id,)
    )
    
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "courses": row[1] or [],
            "study_time": row[2],
            "interests": row[3] or []
        })

    return users


# Similarity scoring
def compute_similarity(u1, u2):
    score = 0

    score += 3 * len(set(u1["courses"]).intersection(u2["courses"]))
    if u1["study_time"] == u2["study_time"]:
        score += 5
    score += 2 * len(set(u1["interests"]).intersection(u2["interests"]))

    return score


# Main pairing function
def pair_user(user_id):
    current_user = get_user(user_id)
    if not current_user:
        return None

    # Already paired?
    if current_user["partner_id"] is not None:
        return current_user["partner_id"]

    others = get_unpaired_users(user_id)
    if not others:
        return None

    best_match = None
    best_score = -1

    for other in others:
        score = compute_similarity(current_user, other)
        if score > best_score:
            best_score = score
            best_match = other

    if not best_match:
        return None

    partner_id = best_match["id"]

    # Update DB
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET partner_id = %s WHERE id = %s OR id = %s;",
        (partner_id, user_id, partner_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return partner_id


# Get the user's partner (for frontend)
def get_paired_user(user_id):
    user = get_user(user_id)
    return user["partner_id"]