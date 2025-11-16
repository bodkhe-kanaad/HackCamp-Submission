import json
import requests
import re

# -----------------------------
# MODEL CONFIGURATION
# -----------------------------
LLM_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "mistral:7b-instruct-v0.3"   # LM Studio model name
MAX_TOKENS = 350


# --------------------------------------------------------
# SIMPLE + ROBUST JSON EXTRACTOR (works best for Mistral)
# --------------------------------------------------------
def extract_json(text):
    text = text.strip()

    # Remove markdown fences if they appear
    text = text.replace("```json", "").replace("```", "")

    # Find first JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    snippet = text[start: end + 1]

    try:
        return json.loads(snippet)
    except:
        return None


# --------------------------------------------------------
# SIMPLE SCHEMA VALIDATION
# --------------------------------------------------------
REQUIRED_KEYS = ["question", "A", "B", "C", "D", "correct_option"]

def valid_schema(j):
    return (
        isinstance(j, dict)
        and all(k in j for k in REQUIRED_KEYS)
        and j.get("correct_option") in ["A", "B", "C", "D"]
    )


# --------------------------------------------------------
# PROMPT OPTIMIZED FOR MISTRAL
# --------------------------------------------------------
def build_prompt(learning_goal):
    return f"""
You are an AI that writes clear, simple multiple-choice questions.

Generate ONE easy MCQ based on this learning goal:

"{learning_goal}"

OUTPUT RULES (IMPORTANT):
- Output ONLY a JSON object.
- No explanation.
- No markdown.
- No extra text.
- Use VERY SIMPLE language.

JSON FORMAT TO OUTPUT EXACTLY:

{{
  "question": "A short and clear question.",
  "A": "Option A",
  "B": "Option B",
  "C": "Option C",
  "D": "Option D",
  "correct_option": "A"
}}

Now output ONLY the JSON:
"""


# --------------------------------------------------------
# MAIN GENERATOR — MISTRAL VERSION
# --------------------------------------------------------
def generate_llm_question(learning_goal):
    prompt = build_prompt(learning_goal)

    try:
        response = requests.post(
            LLM_URL,
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "max_tokens": MAX_TOKENS,
                "stream": False,
                "options": {
                    "temperature": 0.2,     # Mistral behaves very well at 0.1–0.3
                    "stop": ["\n\n", "</s>", "</json>"]  # helps prevent rambling
                }
            }
        )

        raw = response.json().get("response", "")
        parsed = extract_json(raw)

        if parsed and valid_schema(parsed):
            return parsed

        print("[MISTRAL WARNING] Invalid JSON:", raw[:200])

    except Exception as e:
        print("[MISTRAL ERROR]:", e)

    # -------------------------------------
    # LAST-RESORT FALLBACK (should rarely occur)
    # -------------------------------------
    return {
        "question": f"What is a key idea in '{learning_goal}'?",
        "A": "Idea A",
        "B": "Idea B",
        "C": "Idea C",
        "D": "Idea D",
        "correct_option": "A",
    }