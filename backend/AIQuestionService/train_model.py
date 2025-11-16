# backend/AIQuestionService/train_model.py

import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

BASE = Path(__file__).parent
GOALS_PATH = BASE / "learning_goals.json"

def load_learning_goals():
    print(">>> Loading learning goals...")
    with open(GOALS_PATH, "r") as f:
        data = json.load(f)

    texts = []
    labels = []

    for course, weeks in data.items():
        for week, goals in weeks.items():
            for idx, goal in enumerate(goals):
                texts.append(goal)
                labels.append(f"{course}|{week}|{idx}")

    print(f">>> Loaded {len(texts)} total goals.")
    return texts, labels

def train():
    print(">>> Starting model training...")

    texts, labels = load_learning_goals()

    print(">>> Building TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000
    )
    X = vectorizer.fit_transform(texts)

    print(">>> Training Logistic Regression classifier...")
    clf = LogisticRegression(max_iter=1500)
    clf.fit(X, labels)

    print(">>> Saving vectorizer.joblib and classifier.joblib...")
    joblib.dump(vectorizer, BASE / "vectorizer.joblib")
    joblib.dump(clf, BASE / "classifier.joblib")

    print(">>> Training complete.")

if __name__ == "__main__":
    print(">>> Entering main...")
    train()