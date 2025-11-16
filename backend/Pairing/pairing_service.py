from backend.db import get_connection

# Fetch a user and all relevant attributes
def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id, courses, interests, pair_id FROM users WHERE user_id = %s;",
        (user_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "user_id": row[0],
        "courses": row[1] or [],
        "interests": row[2] or [],
        "pair_id": row[3]
    }


# Get all users who are unpaired
def get_unpaired_users(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT user_id, courses, interests
        FROM users
        WHERE pair_id IS NULL AND user_id != %s;
        """,
        (user_id,)
    )
    rows = cur.fetchall()

    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "user_id": row[0],
            "courses": row[1] or [],
            "interests": row[2] or []
        })

    return users


# Similarity scoring
def compute_similarity(u1, u2):
    score = 0
    score += 3 * len(set(u1["courses"]).intersection(u2["courses"]))
    score += 2 * len(set(u1["interests"]).intersection(u2["interests"]))
    return score


# Pair two users and create a pair table entry
def pair_user(user_id):
    user = get_user(user_id)
    if not user:
        return None, None

    # Already paired
    if user["pair_id"] is not None:
        return user["pair_id"], None

    others = get_unpaired_users(user_id)
    if not others:
        return None, None

    best_match = None
    best_score = -1

    for other in others:
        score = compute_similarity(user, other)
        if score > best_score:
            best_score = score
            best_match = other

    if not best_match:
        return None, None

    user2_id = best_match["user_id"]

    # Insert into pair table
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO pair (user1, user2)
        VALUES (%s, %s)
        RETURNING pair_id;
        """,
        (user_id, user2_id)
    )

    pair_id = cur.fetchone()[0]

    # Update both users with this pair_id
    cur.execute("UPDATE users SET pair_id = %s WHERE user_id = %s;", (pair_id, user_id))
    cur.execute("UPDATE users SET pair_id = %s WHERE user_id = %s;", (pair_id, user2_id))

    conn.commit()
    cur.close()
    conn.close()

    return pair_id, user2_id

def unpair_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # Find pair_id
    cur.execute("SELECT pair_id FROM users WHERE user_id = %s;", (user_id,))
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return {"success": True, "message": "User not paired"}

    pair_id = row[0]

    # Get both users in the pair
    cur.execute(
        "SELECT user1, user2 FROM pair WHERE pair_id = %s;",
        (pair_id,)
    )
    pair_row = cur.fetchone()

    if not pair_row:
        cur.close()
        conn.close()
        return {"success": True, "message": "Pair not found"}

    user1, user2 = pair_row

    # Remove pair_id from both users
    cur.execute("UPDATE users SET pair_id = NULL WHERE user_id = %s;", (user1,))
    cur.execute("UPDATE users SET pair_id = NULL WHERE user_id = %s;", (user2,))

    # Delete pair row
    cur.execute("DELETE FROM pair WHERE pair_id = %s;", (pair_id,))

    conn.commit()
    cur.close()
    conn.close()

    return {"success": True}


def get_user_pair_status(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # get pair_id from users
    cur.execute(
        "SELECT pair_id FROM users WHERE user_id = %s;",
        (user_id,)
    )
    row = cur.fetchone()

    if not row or row[0] is None:
        cur.close()
        conn.close()
        return None

    pair_id = row[0]

    # get the pair info
    cur.execute(
        "SELECT user1, user2 FROM pair WHERE pair_id = %s;",
        (pair_id,)
    )
    pr = cur.fetchone()

    cur.close()
    conn.close()

    if not pr:
        return None

    user1, user2 = pr
    partner_id = user2 if user1 == user_id else user1

    return {
        "pair_id": pair_id,
        "partner_id": partner_id
    }