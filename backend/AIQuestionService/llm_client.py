import json
import requests
import re

LLM_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3.1"   # replace with your model name
MAX_TOKENS = 1024


# ---------------------------------------------
# Clean model output (remove markdown, code fences, junk)
# ---------------------------------------------
def _extract_json(text):
    """
    Extract the FIRST valid JSON object from the text.
    Cleans markdown ``` fences and other wrappers.
    """
    # Remove code fences
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = text.replace("```json", "").replace("```", "").strip()

    # Try direct JSON parse
    try:
        return json.loads(text)
    except:
        pass

    # Try to locate JSON substring using regex
    json_match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if json_match:
        snippet = json_match.group(0)
        try:
            return json.loads(snippet)
        except:
            return None

    return None


# ---------------------------------------------
# Validate JSON structure
# ---------------------------------------------
REQUIRED_KEYS = ["question", "A", "B", "C", "D", "correct_option"]

def _is_valid_schema(obj):
    if not isinstance(obj, dict):
        return False
    for k in REQUIRED_KEYS:
        if k not in obj or not obj[k]:
            return False
    return True


# ---------------------------------------------
# Build strong prompt
# ---------------------------------------------
def _build_prompt(learning_goal):
    return f"""
You are an AI that generates **university-level HOTS multiple-choice questions**.

You must strictly output **one** JSON object with exactly this structure:

{{
  "question": "<one clear question>",
  "A": "<option A>",
  "B": "<option B>",
  "C": "<option C>",
  "D": "<option D>",
  "correct_option": "A"  // only A, B, C, or D
}}

Rules:
• Do NOT include explanations.
• Do NOT include more than one answer.
• Do NOT include text outside the JSON object.
• Options should be similar in length/difficulty.
• The question must require higher-order reasoning, based on the following learning goal:

Learning goal:
"{learning_goal}"

Now generate the JSON object.
"""


# ---------------------------------------------
# Main generation function
# ---------------------------------------------
def generate_llm_question(learning_goal, retries=3):
    prompt = _build_prompt(learning_goal)

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

            raw = response.json().get("response", "")
            parsed = _extract_json(raw)

            if parsed and _is_valid_schema(parsed):
                return parsed

            print(f"[LLM WARNING] Invalid JSON attempt {attempt}: {raw[:200]}...")

        except Exception as e:
            print(f"[LLM ERROR] Attempt {attempt} failed: {e}")

    # -----------------------------------------
    # FINAL FALLBACK (never let question fail)
    # -----------------------------------------
    return {
        "question": "Fallback HOTS question: Based on the learning goal, what is the most important concept?",
        "A": "Key concept A",
        "B": "Key concept B",
        "C": "Key concept C",
        "D": "Key concept D",
        "correct_option": "A"
    }