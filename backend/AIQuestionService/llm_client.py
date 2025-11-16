import json
import requests
import re

# -----------------------------------
# MODEL CONFIGURATION
# -----------------------------------
LLM_URL = "http://localhost:1234/v1/chat/completions"   # LM Studio chat endpoint
LLM_MODEL = "mistral-7b-instruct-v0.3"
MAX_TOKENS = 400
REQUEST_TIMEOUT = 60

# -----------------------------------
# JSON EXTRACTION & VALIDATION
# -----------------------------------
def _strip_fences(text: str) -> str:
    return text.replace("```json", "").replace("```", "").strip()

def _extract_json(text: str):
    if not text:
        return None
    text = _strip_fences(text)
    try:
        return json.loads(text)
    except:
        pass
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        try:
            return json.loads(m.group(0))
        except:
            return None
    return None

REQUIRED_KEYS = ["question", "A", "B", "C", "D", "correct_option"]

def _valid_schema(obj):
    if not isinstance(obj, dict):
        return False
    for k in REQUIRED_KEYS:
        if k not in obj or not obj[k]:
            return False
    if obj["correct_option"] not in ["A", "B", "C", "D"]:
        return False
    return True

# -----------------------------------
# PROMPT FOR MISTRAL
# -----------------------------------
def _build_prompt(learning_goal: str) -> str:
    return f"""
You are a question-generation AI. You must OUTPUT EXACTLY one JSON object and NOTHING else.

JSON schema:
{{
  "question": "A short higher-order thinking question",
  "A": "Option A",
  "B": "Option B",
  "C": "Option C",
  "D": "Option D",
  "correct_option": "A"
}}

Rules:
- No explanation, no commentary, no reasoning text.
- No markdown, no backticks.
- Options similar in length/difficulty.
- The question must be HOTS (higher-order thinking), based strictly on the learning goal.
Learning goal:
"{learning_goal}"

Now output only the JSON object.
"""

# -----------------------------------
# MODEL CALL
# -----------------------------------
def generate_llm_question(learning_goal: str, retries: int = 3):
    prompt = _build_prompt(learning_goal)
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(
                LLM_URL,
                json={
                    "model": LLM_MODEL,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": MAX_TOKENS,
                    "temperature": 0.2
                },
                timeout=REQUEST_TIMEOUT
            )
            resp.raise_for_status()
            raw = resp.json()["choices"][0]["message"]["content"]
            parsed = _extract_json(raw)
            if parsed and _valid_schema(parsed):
                return parsed
            print(f"[MISTRAL WARNING] attempt {attempt}: bad JSON → {raw[:150]}")
        except Exception as e:
            print(f"[MISTRAL ERROR] attempt {attempt}: {e}")
    # fallback
    return {
        "question": "Fallback question: Identify the key concept related to the goal.",
        "A": "Concept A",
        "B": "Concept B",
        "C": "Concept C",
        "D": "Concept D",
        "correct_option": "A"
    }