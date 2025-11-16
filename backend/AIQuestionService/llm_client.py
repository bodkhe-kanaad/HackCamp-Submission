# llm_client.py
import json
import re
import os
from openai import OpenAI

# -----------------------------------------------------
# CONFIG
# -----------------------------------------------------
OPENAI_API_KEY = "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"
MODEL_NAME = "gpt-4o-mini"    # fast + good
MAX_TOKENS = 300

client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------------------------------
# JSON Extraction Helper
# -----------------------------------------------------
def _extract_json(text):
    """Extract the first valid JSON object from model output."""
    # Remove code fences
    cleaned = text.replace("```json", "").replace("```", "").strip()

    # Try full parse
    try:
        return json.loads(cleaned)
    except:
        pass

    # Try to grab a JSON object via regex
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        snippet = match.group(0)
        try:
            return json.loads(snippet)
        except:
            return None

    return None


# -----------------------------------------------------
# JSON Schema Validator
# -----------------------------------------------------
REQUIRED_KEYS = ["question", "A", "B", "C", "D", "correct_option"]

def _is_valid_schema(obj):
    if not isinstance(obj, dict):
        return False

    for k in REQUIRED_KEYS:
        if k not in obj or obj[k] is None or obj[k] == "":
            return False

    if obj["correct_option"] not in ["A", "B", "C", "D"]:
        return False

    return True


# -----------------------------------------------------
# Prompt Builder
# -----------------------------------------------------
def _build_prompt(learning_goal):
    return f"""
You are an AI that generates **university-level multiple-choice questions**.
Output MUST be **a single JSON object only**. No explanations. No markdown.

JSON FORMAT (STRICT):
{{
  "question": "A single clear question",
  "A": "Option A",
  "B": "Option B",
  "C": "Option C",
  "D": "Option D",
  "correct_option": "A"
}}

RULES:
- Do NOT add any text before or after the JSON.
- Options must be similar difficulty.
- Based ONLY on the following learning goal:

LEARNING GOAL:
"{learning_goal}"

Return ONLY the JSON:
"""


# -----------------------------------------------------
# Main Generator
# -----------------------------------------------------
def generate_llm_question(learning_goal, retries=3):
    prompt = _build_prompt(learning_goal)

    for attempt in range(1, retries + 1):
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=MAX_TOKENS,
                temperature=0.2,
            )

            raw_text = completion.choices[0].message["content"]
            parsed = _extract_json(raw_text)

            if parsed and _is_valid_schema(parsed):
                return parsed

            print(f"[LLM WARNING] Attempt {attempt}: invalid JSON output")
            print(raw_text[:200])

        except Exception as e:
            print(f"[LLM ERROR] Attempt {attempt}: {e}")

    # -----------------------------------------------------
    # FINAL FAILSAFE — never break your app
    # -----------------------------------------------------
    return {
        "question": "Fallback: What is the main concept behind this learning objective?",
        "A": "Concept A",
        "B": "Concept B",
        "C": "Concept C",
        "D": "Concept D",
        "correct_option": "A"
    }