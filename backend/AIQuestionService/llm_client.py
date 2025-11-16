import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------------------------------
# LOAD ENV + CONFIG
# -----------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set!")

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = "gpt-4o-mini"      # change this to any model you want
MAX_TOKENS = 350


# -----------------------------------------------------
# Helper: extract JSON from model text
# -----------------------------------------------------
def _extract_json(text):
    cleaned = (
        text.replace("```json", "")
            .replace("```", "")
            .strip()
    )

    # Try direct JSON
    try:
        return json.loads(cleaned)
    except:
        pass

    # Try regex-based extraction
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            return None

    return None


# -----------------------------------------------------
# Validate JSON structure
# -----------------------------------------------------
REQUIRED_KEYS = ["question", "A", "B", "C", "D", "correct_option"]

def _is_valid_schema(obj):
    if not isinstance(obj, dict):
        return False

    for k in REQUIRED_KEYS:
        if k not in obj or not obj[k]:
            return False

    if obj["correct_option"] not in ["A", "B", "C", "D"]:
        return False

    return True


# -----------------------------------------------------
# Prompt builder
# -----------------------------------------------------
def _build_prompt(learning_goal):
    return f"""
You generate university-level multiple-choice questions.

OUTPUT RULES:
- Output must be EXACTLY one JSON object.
- No explanations, no markdown, no text outside JSON.

FORMAT STRICTLY:
{{
  "question": "string",
  "A": "string",
  "B": "string",
  "C": "string",
  "D": "string",
  "correct_option": "A"
}}

Learning Goal:
"{learning_goal}"

Now output ONLY the JSON object.
"""


# -----------------------------------------------------
# Main LLM Generator
# -----------------------------------------------------
def generate_llm_question(learning_goal, retries=3):
    prompt = _build_prompt(learning_goal)

    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=MAX_TOKENS,
                temperature=0.2,
            )

            raw_text = response.choices[0].message.content
            parsed = _extract_json(raw_text)

            if parsed and _is_valid_schema(parsed):
                return parsed

            print(f"[LLM WARNING] Attempt {attempt}: Invalid JSON:")
            print(raw_text)

        except Exception as e:
            print(f"[LLM ERROR] Attempt {attempt}: {e}")

    # If nothing works, return None — LET YOUR CALLER HANDLE IT
    return None