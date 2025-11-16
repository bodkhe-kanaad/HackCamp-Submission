import json
import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).resolve().parent

# Load learning goals
with open(BASE / "learning_goals.json") as f:
    LEARNING_GOALS = json.load(f)

# Load ML model + vectorizer
VECT = joblib.load(BASE / "vectorizer.joblib")
CLF = joblib.load(BASE / "classifier.joblib")

# Embedding model + precomputed embeddings
EMB = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
GOAL_EMB = joblib.load(BASE / "goal_embeddings.joblib")
GOAL_INDEX = joblib.load(BASE / "goal_index.joblib")  # list of (course, week, index)


def keyword_overlap(a, b):
    a_set = set(a.lower().split())
    b_set = set(b.lower().split())
    return len(a_set.intersection(b_set)) / (len(a_set) + 1)


def choose_best_learning_goal(course, week, query="generate a HOTS question"):
    """
    Returns ONE best matching learning goal using an ensemble:
    50% classifier, 35% embedding similarity, 15% keyword overlap
    """

    week = str(week)
    goals = LEARNING_GOALS[course][week]

    # --- ML classifier (coarse routing) ---
    clf_label = CLF.predict(VECT.transform([query]))[0]
    clf_course, clf_week, clf_idx = clf_label.split("|")
    clf_idx = int(clf_idx)

    clf_boost = (
        1 if (clf_course == course and clf_week == week and clf_idx < len(goals))
        else 0
    )

    # --- Embedding similarity ---
    q_emb = EMB.encode([query])
    sims = cosine_similarity(q_emb, GOAL_EMB[course][week])[0]

    # --- Keyword overlap ---
    kw_scores = [keyword_overlap(query, g) for g in goals]

    # --- Combine ---
    final_scores = []
    for i, g in enumerate(goals):
        final_scores.append(
            0.50 * (clf_boost if i == clf_idx else 0)
            + 0.35 * sims[i]
            + 0.15 * kw_scores[i]
        )

    best_idx = int(np.argmax(final_scores))
    return goals[best_idx]