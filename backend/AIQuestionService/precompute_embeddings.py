import json
import joblib
from sentence_transformers import SentenceTransformer
from pathlib import Path

BASE = Path(__file__).resolve().parent

# Load learning goals JSON
with open(BASE / "learning_goals.json") as f:
    GOALS = json.load(f)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts = []
index = []  # (course, week, idx)

for course, weeks in GOALS.items():
    for week, items in weeks.items():
        for i, text in enumerate(items):
            texts.append(text)
            index.append((course, week, i))

embs = model.encode(texts, show_progress_bar=True)

joblib.dump(embs, BASE / "goal_embeddings.joblib")
joblib.dump(index, BASE / "goal_index.joblib")

print("Precomputed syllabus embeddings.")