from backend.db import get_connection

# ---------------------------------------------------------
# Daily streak update logic
# ---------------------------------------------------------
def update_streaks_for_all_pairs():
    conn = get_connection()
    cur = conn.cursor()

    # Get all pairs and their answer status
    cur.execute(
        """
        SELECT pair_id, user1_answered, user2_answered
        FROM "Pair";
        """
    )
    rows = cur.fetchall()

    for pair_id, u1_done, u2_done in rows:

        if u1_done and u2_done:
            # Both answered → increment streak and reset daily fields
            cur.execute(
                """
                UPDATE "Pair"
                SET streak = streak + 1,
                    question_id = NULL,
                    user1_answered = FALSE,
                    user2_answered = FALSE
                WHERE pair_id = %s;
                """,
                (pair_id,)
            )
        else:
            # One or both did NOT answer → reset streak
            cur.execute(
                """
                UPDATE "Pair"
                SET streak = 0,
                    question_id = NULL,
                    user1_answered = FALSE,
                    user2_answered = FALSE
                WHERE pair_id = %s;
                """,
                (pair_id,)
            )

    conn.commit()
    cur.close()
    conn.close()


# ---------------------------------------------------------
# Leaderboard retrieval
# ---------------------------------------------------------
def get_leaderboard():
    conn = get_connection()
    cur = conn.cursor()

    # Get usernames + streak sorted by streak DESC
    cur.execute("""
        SELECT 
            P.pair_id,
            u1.username AS username1,
            u2.username AS username2,
            P.streak
        FROM "Pair" P
        LEFT JOIN users u1 ON P.user1 = u1.user_id
        LEFT JOIN users u2 ON P.user2 = u2.user_id
        ORDER BY P.streak DESC, P.pair_id ASC;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    leaderboard = []
    for pair_id, username1, username2, streak in rows:
        leaderboard.append({
            "pair_id": pair_id,
            "names": f"{username1} & {username2}",
            "streak": streak
        })

    return leaderboard

def get_user_streak(user_id):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT streak
        FROM "Pair"
        WHERE (user1 = %s OR user2 = %s)
        LIMIT 1;
    """
    cur.execute(query, (user_id, user_id))

    row = cur.fetchone()
    if row:
        streak = {"streak": row[0]}
    else:
        streak = None

    cur.close()
    conn.close()

    return streak