import json
import requests
import re

# -----------------------------
# MODEL CONFIGURATION
# -----------------------------
LLM_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen2.5:7b-instruct"   # BEST CHOICE
MAX_TOKENS = 480                    # enough without overloading

# -----------------------------
# CLEAN + JSON EXTRACTION
# -----------------------------
def _extract_json(text):
    """Extract the first valid JSON object from model output."""
    # Remove code fences
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = text.replace("```json", "").replace("```", "").strip()

    # Try direct parse
    try:
        return json.loads(text)
    except:
        pass

    # Try regex extraction
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        snippet = m.group(0)
        try:
            return json.loads(snippet)
        except:
            return None

    return None


REQUIRED_KEYS = ["question", "A", "B", "C", "D", "correct_option"]

def _valid_schema(obj):
    """Ensure the JSON has the required keys AND correct field formatting."""
    if not isinstance(obj, dict):
        return False
    for key in REQUIRED_KEYS:
        if key not in obj or not obj[key]:
            return False

    # Ensure correct_option is one of A/B/C/D
    if obj["correct_option"] not in ["A", "B", "C", "D"]:
        return False

    return True


# -----------------------------
# PROMPT ENGINEERING FOR QWEN
# -----------------------------
def _prompt(learning_goal):
    return f"""
You are an AI that generates **high-quality university-level HOTS multiple-choice questions**.

IMPORTANT — Your ENTIRE OUTPUT **must be ONE JSON object only**, with NO explanations, NO extra text, NO markdown.

JSON SCHEMA (STRICT):
{{
  "question": "A single clear question",
  "A": "Option A",
  "B": "Option B",
  "C": "Option C",
  "D": "Option D",
  "correct_option": "A"  // must be exactly A, B, C, or D
}}

RULES:
• Do NOT include explanations.
• Do NOT include reasoning.
• DO NOT write anything outside the JSON.
• Options must be similar in difficulty.
• The question must require higher-order thinking.
• Base the question ONLY on this learning goal:

LEARNING GOAL:
"{learning_goal}"

Now output ONLY the JSON object:
"""


# -----------------------------
# MAIN GENERATOR
# -----------------------------
def generate_llm_question(learning_goal, retries=3):
    prompt = _prompt(learning_goal)

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(
                LLM_URL,
                json={
                    "model": LLM_MODEL,
                    "prompt": prompt,
                    "max_tokens": MAX_TOKENS,
                    "stream": False,
                }
            )

            raw_text = response.json().get("response", "")
            parsed = _extract_json(raw_text)

            if parsed and _valid_schema(parsed):
                return parsed

            print(f"[QWEN WARNING] Invalid JSON (attempt {attempt}): {raw_text[:200]}")

        except Exception as e:
            print(f"[QWEN ERROR] {attempt=}: {e}")

    # ----------------------------------------
    #  FINAL SAFETY: NEVER RETURN NOTHING
    # ----------------------------------------
    return {
        "question": "Fallback HOTS question: Identify the key concept based on the learning goal.",
        "A": "Concept A",
        "B": "Concept B",
        "C": "Concept C",
        "D": "Concept D",
        "correct_option": "A"
    }