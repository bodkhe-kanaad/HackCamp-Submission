# llm_client.py
import json
import re
import os
from openai import OpenAI
from dotenv import load_dotenv

# -----------------------------------------------------
# LOAD ENV + API KEY
# -----------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in environment!")

client = OpenAI(api_key=OPENAI_API_KEY)

# Model and token config
MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 300


# -----------------------------------------------------
# Extract JSON from model output
# -----------------------------------------------------
def _extract_json(text: str) -> dict | None:
    """Extract a JSON object cleanly from LLM output."""
    if not text:
        return None

    # Remove code fences if present
    cleaned = text.replace("```json", "").replace("```", "").strip()

    # Try direct parse
    try:
        return json.loads(cleaned)
    except:
        pass

    # Fallback: regex find first {...}
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        snippet = match.group(0)
        try:
            return json.loads(snippet)
        except:
            return None

    return None


# -----------------------------------------------------
# Validate LLM output schema
# -----------------------------------------------------
REQUIRED_KEYS = ["question", "A", "B", "C", "D", "correct_option"]

def _is_valid_schema(obj: dict) -> bool:
    if not isinstance(obj, dict):
        return False

    for k in REQUIRED_KEYS:
        if k not in obj or not obj[k]:
            return False

    if obj["correct_option"] not in ["A", "B", "C", "D"]:
        return False

    return True


# -----------------------------------------------------
# Prompt Builder
# -----------------------------------------------------
def _build_prompt(goal: str) -> str:
    return f"""
You generate **university-level multiple-choice questions**.

Output MUST be **ONLY a JSON object**. No explanation. No markdown.

FORMAT (STRICT):
{{
  "question": "A clear question",
  "A": "Option A",
  "B": "Option B",
  "C": "Option C",
  "D": "Option D",
  "correct_option": "A"
}}

LEARNING GOAL:
"{goal}"

Return ONLY the JSON.
"""


# -----------------------------------------------------
# Main: generate good MCQ
# -----------------------------------------------------
def generate_llm_question(learning_goal: str, retries: int = 3) -> dict:
    prompt = _build_prompt(learning_goal)

    for attempt in range(1, retries + 1):
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=MAX_TOKENS,
                temperature=0.1,
            )

            raw = completion.choices[0].message.content
            parsed = _extract_json(raw)

            if parsed and _is_valid_schema(parsed):
                return parsed

            print(f"[WARN] Invalid JSON on attempt {attempt}")
            print(raw[:200])

        except Exception as e:
            print(f"[ERROR] LLM error attempt {attempt}: {e}")

    # Final fallback (only if OpenAI fully fails)
    return {
        "question": "Fallback: Which option best matches your learning goal?",
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D",
        "correct_option": "A"
    }