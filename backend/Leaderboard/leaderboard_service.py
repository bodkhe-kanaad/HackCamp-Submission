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

    cur.execute(
        """
        SELECT pair_id, user1, user2, streak
        FROM "Pair"
        ORDER BY streak DESC, pair_id ASC;
        """
    )
    rows = cur.fetchall()

    cur.close()
    conn.close()

    leaderboard = []
    for pair_id, user1, user2, streak in rows:
        leaderboard.append({
            "pair_id": pair_id,
            "user1": user1,
            "user2": user2,
            "streak": streak
        })

    return leaderboard