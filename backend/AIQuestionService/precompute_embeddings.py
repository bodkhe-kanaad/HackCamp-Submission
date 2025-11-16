import json
import joblib
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).resolve().parent

# Load learning goals JSON
with open(BASE / "learning_goals.json") as f:
    LEARNING_GOALS = json.load(f)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

GOAL_EMB = {}   # final dict: {course: {week: np.matrix}}
GOAL_INDEX = [] # (course, week, idx)

for course, week_dict in LEARNING_GOALS.items():
    GOAL_EMB[course] = {}

    for week, goals in week_dict.items():
        # Encode all goals at once
        matrix = model.encode(goals)

        # Convert to numpy 2D matrix
        matrix = np.asarray(matrix)

        GOAL_EMB[course][week] = matrix

        for idx in range(len(goals)):
            GOAL_INDEX.append((course, week, idx))

# Save models
joblib.dump(GOAL_EMB, BASE / "goal_embeddings.joblib")
joblib.dump(GOAL_INDEX, BASE / "goal_index.joblib")

print("SUCCESS: Embeddings regenerated cleanly.")