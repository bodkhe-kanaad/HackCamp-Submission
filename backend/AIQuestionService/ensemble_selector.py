import json
import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).resolve().parent

# --------------------------------------------------
# LOAD RESOURCES
# --------------------------------------------------

with open(BASE / "learning_goals.json") as f:
    LEARNING_GOALS = json.load(f)

VECT = joblib.load(BASE / "vectorizer.joblib")
CLF = joblib.load(BASE / "classifier.joblib")

EMB = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# In your latest setup this is usually a nested dict:
#   GOAL_EMB[course][week_key] -> np.ndarray of shape (num_goals, dim)
GOAL_EMB = joblib.load(BASE / "goal_embeddings.joblib")
GOAL_INDEX = joblib.load(BASE / "goal_index.joblib")  # kept for completeness


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def _extract_week_number(raw_week: str) -> int:
    """
    Accepts things like 'WEEK_1', 'week_14', '1', '14'
    and always returns an integer 1, 14, etc.
    """
    raw_week = raw_week.strip().upper()

    if raw_week.startswith("WEEK_"):
        raw_week = raw_week.split("_", 1)[1]

    digits = "".join(c for c in raw_week if c.isdigit())
    if digits:
        return int(digits)
    return 1


def _normalize_week_for_course(course: str, requested_week_any: str | int) -> str:
    """
    Map a numeric week (like 14) to the closest valid week KEY
    in LEARNING_GOALS[course].

    This is the key part: it understands keys like "1" or "WEEK_1"
    and always returns the ORIGINAL key string from the JSON.
    """
    if course not in LEARNING_GOALS:
        raise ValueError(f"Unknown course: {course}")

    # Build (week_num, key_str) pairs from whatever keys exist in JSON
    key_pairs = []
    for key in LEARNING_GOALS[course].keys():
        week_num = _extract_week_number(key)
        key_pairs.append((week_num, key))

    # Sort by numeric week
    key_pairs.sort(key=lambda x: x[0])

    requested_week = _extract_week_number(str(requested_week_any))

    # Clamp requested to min/max
    min_week = key_pairs[0][0]
    max_week = key_pairs[-1][0]

    if requested_week < min_week:
        requested_week = min_week
    if requested_week > max_week:
        requested_week = max_week

    # Return the key whose week_num == requested_week
    for week_num, key_str in key_pairs:
        if week_num == requested_week:
            return key_str

    # Fallback: return the last key if something weird happens
    return key_pairs[-1][1]


def keyword_overlap(a: str, b: str) -> float:
    a_set = set(a.lower().split())
    b_set = set(b.lower().split())
    if not a_set:
        return 0.0
    return len(a_set.intersection(b_set)) / (len(a_set) + 1)


# --------------------------------------------------
# MAIN SELECTOR
# --------------------------------------------------

def choose_best_learning_goal(course: str, week, query: str = "generate a HOTS question") -> str:
    """
    Returns ONE best learning goal using:
      - 50% classifier guidance
      - 35% embedding similarity (RAG)
      - 15% keyword overlap

    Works even if:
      - LEARNING_GOALS has keys "1" or "WEEK_1"
      - classifier predicts week 14 but course has only 1–5
    """

    if course not in LEARNING_GOALS:
        raise ValueError(f"Unknown course: {course}")

    # Normalize week to a valid KEY string in LEARNING_GOALS[course]
    normalized_week_key = _normalize_week_for_course(course, week)

    goals = LEARNING_GOALS[course][normalized_week_key]
    num_goals = len(goals)

    # ------------------------------------------------
    # 1. Classifier prediction (coarse routing)
    # ------------------------------------------------
    clf_pred = CLF.predict(VECT.transform([query]))[0]

    try:
        clf_course, clf_week_raw, clf_idx_raw = clf_pred.split("|")
    except Exception:
        clf_course, clf_week_raw, clf_idx_raw = course, str(week), "0"

    clf_week_num = _extract_week_number(clf_week_raw)
    clf_week_key = _normalize_week_for_course(course, clf_week_num)

    try:
        clf_idx = int(clf_idx_raw)
    except Exception:
        clf_idx = 0

    if clf_idx < 0 or clf_idx >= num_goals:
        clf_idx = 0

    classifier_boost = (
        1.0 if (clf_course == course and clf_week_key == normalized_week_key) else 0.0
    )

    # ------------------------------------------------
    # 2. Embedding similarity
    # ------------------------------------------------
    q_emb = EMB.encode([query])

    # Access embeddings using the same week key mapping
    if course in GOAL_EMB and normalized_week_key in GOAL_EMB[course]:
        emb_matrix = GOAL_EMB[course][normalized_week_key]
    else:
        # fallback: first available week’s embeddings if mismatch
        first_week_key = _normalize_week_for_course(course, 1)
        emb_matrix = GOAL_EMB[course][first_week_key]

    sims = cosine_similarity(q_emb, emb_matrix)[0]  # shape: (num_goals,)

    # ------------------------------------------------
    # 3. Keyword heuristic
    # ------------------------------------------------
    kw_scores = [keyword_overlap(query, g) for g in goals]

    # ------------------------------------------------
    # 4. Final weighted ensemble
    # ------------------------------------------------
    scores = []
    for i in range(num_goals):
        clf_score = classifier_boost if i == clf_idx else 0.0
        emb_score = float(sims[i]) if i < len(sims) else 0.0
        kw_score = kw_scores[i]

        final = 0.50 * clf_score + 0.35 * emb_score + 0.15 * kw_score
        scores.append(final)

    best_idx = int(np.argmax(scores))
    return goals[best_idx]