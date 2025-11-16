# ============================================================
# AI PIPELINE TEST SCRIPT - FULLY FIXED VERSION
# ============================================================

import os
import sys
from pathlib import Path
import joblib

# ------------------------------------------------------
# PATH FIX — works no matter where script is executed
# ------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
BACKEND_DIR = THIS_FILE.parents[1]              # .../backend
PROJECT_ROOT = THIS_FILE.parents[2]             # .../HackCamp-Submission

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_DIR))

print("Injected paths:")
print("  PROJECT_ROOT:", PROJECT_ROOT)
print("  BACKEND_DIR :", BACKEND_DIR)

# ------------------------------------------------------
# BASE PATH for model files
# ------------------------------------------------------
BASE = BACKEND_DIR / "AIQuestionService"


# ------------------------------------------------------
# START TESTING
# ------------------------------------------------------
print("\n===============================")
print("  AI PIPELINE TEST SCRIPT")
print("===============================")
print("\nStarting tests...")


# ------------------------------------------------------
# TEST 1 — MODEL FILE CHECK
# ------------------------------------------------------
print("\nTEST 1 — Checking model files...")

required_files = [
    "vectorizer.joblib",
    "classifier.joblib",
    "goal_embeddings.joblib",
    "goal_index.joblib",
    "learning_goals.json"
]

for f in required_files:
    fp = BASE / f
    if fp.exists():
        print(f"  - {f}: OK ✓")
    else:
        print(f"  - {f}: MISSING ✗")


# ------------------------------------------------------
# TEST 2 — Classifier test
# ------------------------------------------------------
print("\nTEST 2 — Classifier inference...")

try:
    vect = joblib.load(BASE / "vectorizer.joblib")
    clf = joblib.load(BASE / "classifier.joblib")

    sample = ["derivative rules from MATH 100"]
    X = vect.transform(sample)
    pred = clf.predict(X)[0]

    print("  - Prediction:", pred, "✓")

except Exception as e:
    print("  - FAILED ✗")
    print("    Error:", e)


# ------------------------------------------------------
# TEST 3 — Embeddings load
# ------------------------------------------------------
print("\nTEST 3 — Embeddings load...")

try:
    embeddings = joblib.load(BASE / "goal_embeddings.joblib")
    print("  - Embeddings OK; shape:", embeddings.shape, "✓")

    index = joblib.load(BASE / "goal_index.joblib")
    print("  - Index OK; items:", len(index), "✓")

except Exception as e:
    print("  - FAILED ✗")
    print("    Error:", e)


# ------------------------------------------------------
# TEST 4 — Ensemble Selector
# ------------------------------------------------------
print("\nTEST 4 — Ensemble selector...")

try:
    from backend.AIQuestionService.ensemble_selector import choose_best_learning_goal
    out = choose_best_learning_goal("MATH 100", 14, "chain rule practice")
    print("  - Output:", out, "✓")

except Exception as e:
    print("  - FAILED ✗")
    print("    Error:", e)


# ------------------------------------------------------
# TEST 5 — AI Question Generator
# ------------------------------------------------------
print("\nTEST 5 — AI question generator...")

try:
    from backend.AIQuestionService.ai_question_service import generate_llm_question
    qa = generate_llm_question("derivatives and limit definition")

    print("  - Question:", qa["question"][:60], "...")
    print("  - A:", qa["A"])
    print("  - B:", qa["B"])
    print("  - C:", qa["C"])
    print("  - D:", qa["D"])
    print("  - Correct:", qa["correct"])
    print("  ✓ PASS")

except Exception as e:
    print("  - FAILED ✗")
    print("    Error:", e)


print("\n===============================")
print("  TEST RESULTS SUMMARY")
print("===============================\n")
print("Model files present         : ✓" if all((BASE/f).exists() for f in required_files) else "Model files present         : ✗")
print("Classifier works            : ✓" if 'pred' in locals() else "Classifier works            : ✗")
print("Embeddings load             : ✓" if 'embeddings' in locals() else "Embeddings load             : ✗")
print("Ensemble selector works     : ✓" if 'out' in locals() else "Ensemble selector works     : ✗")
print("AI question generator       : ✓" if 'qa' in locals() else "AI question generator       : ✗")

print("\nDone.\n")