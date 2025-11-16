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

REQUIRED_KEYS = ["question", "A", "B", "C", "D", "correct_option"]


# -----------------------------------------------------
# JSON extraction helpers
# -----------------------------------------------------

def _extract_json_block(text: str) -> Dict[str, Any] | None:
    """
    Try to extract the first JSON object from the LLM output.
    Handles extra chatter before and after.
    """
    if not text:
        print("[LLM DEBUG] Empty response text")
        return None

    # Remove common code fences
    cleaned = text.replace("```json", "").replace("```", "").strip()

    # First try parsing entire thing
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # Try to find a JSON object inside the text
    match = re.search(r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}", cleaned, flags=re.DOTALL)
    if not match:
        print("[LLM DEBUG] No JSON block found in response")
        return None

    snippet = match.group(0)
    try:
        return json.loads(snippet)
    except Exception as e:
        print("[LLM DEBUG] Failed to parse JSON snippet:", e)
        print("[LLM DEBUG] Snippet was:", snippet[:300])
        return None


# -----------------------------------------------------
# Schema normalization and validation
# -----------------------------------------------------

def _normalize_schema(raw: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Normalize whatever the model produced into:
    {
        "question": str,
        "A": str,
        "B": str,
        "C": str,
        "D": str,
        "correct_option": "A" | "B" | "C" | "D"
    }
    Returns None if it cannot be repaired.
    """
    if not isinstance(raw, dict):
        print("[LLM DEBUG] Raw JSON is not a dict:", type(raw))
        return None

    obj = dict(raw)  # shallow copy so we can mutate

    # Case 1: options nested under "options"
    if "options" in obj and isinstance(obj["options"], dict):
        opts = obj["options"]
        # allow lowercase keys in options
        obj["A"] = obj.get("A") or opts.get("A") or opts.get("a")
        obj["B"] = obj.get("B") or opts.get("B") or opts.get("b")
        obj["C"] = obj.get("C") or opts.get("C") or opts.get("c")
        obj["D"] = obj.get("D") or opts.get("D") or opts.get("d")

    # Case 2: lowercase keys everywhere
    lower = {k.lower(): v for k, v in obj.items()}
    if "question" in lower and "question" not in obj:
        obj["question"] = lower["question"]
    for letter in ["a", "b", "c", "d"]:
        if letter in lower and letter.upper() not in obj:
            obj[letter.upper()] = lower[letter]
    if "correct_option" in lower and "correct_option" not in obj:
        obj["correct_option"] = lower["correct_option"]
    if "answer" in lower and "correct_option" not in obj:
        obj["correct_option"] = lower["answer"]

    # Ensure required keys exist and are non empty
    for k in ["question", "A", "B", "C", "D"]:
        if k not in obj or not isinstance(obj[k], str) or not obj[k].strip():
            print(f"[LLM DEBUG] Missing or empty field: {k}")
            return None

    # Normalize correct_option
    correct = obj.get("correct_option")
    if isinstance(correct, str):
        correct = correct.strip()
    else:
        correct = str(correct).strip()

    # If model gave the letter, normalize to uppercase
    if correct.upper() in ["A", "B", "C", "D"]:
        obj["correct_option"] = correct.upper()
    else:
        # Maybe model returned the actual text of the option
        # Try to map it to a letter by equality
        for letter in ["A", "B", "C", "D"]:
            if correct == obj[letter]:
                obj["correct_option"] = letter
                break

    if obj.get("correct_option") not in ["A", "B", "C", "D"]:
        print("[LLM DEBUG] Invalid correct_option:", obj.get("correct_option"))
        return None

    return {
        "question": obj["question"].strip(),
        "A": obj["A"].strip(),
        "B": obj["B"].strip(),
        "C": obj["C"].strip(),
        "D": obj["D"].strip(),
        "correct_option": obj["correct_option"],
    }


def _is_valid_schema(obj: Dict[str, Any]) -> bool:
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

def _build_prompt(learning_goal: str) -> str:
    return f"""
You are an AI that generates university level multiple choice questions.

You MUST respond with ONE JSON object only. No explanations. No markdown. No commentary.

JSON FORMAT:
{{
  "question": "A single clear question",
  "A": "Option A",
  "B": "Option B",
  "C": "Option C",
  "D": "Option D",
  "correct_option": "A"
}}

Rules:
- Do not add any text before or after the JSON.
- Options should be similar in difficulty and plausible.
- The question must be based ONLY on this learning goal:

"{learning_goal}"
"""


# -----------------------------------------------------
# Main generator
# -----------------------------------------------------

def generate_llm_question(learning_goal: str, retries: int = 3) -> Dict[str, Any]:
    """
    Generate a multiple choice question using OpenAI.
    Returns a dict with keys: question, A, B, C, D, correct_option.
    Will fall back to a generic question only if everything fails.
    """
    prompt = _build_prompt(learning_goal)

    for attempt in range(1, retries + 1):
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You generate strict JSON only."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=MAX_TOKENS,
                temperature=0.4,
            )

            # New client API: message.content is already a string
            raw_text = completion.choices[0].message.content
            print(f"[LLM DEBUG] Raw content (attempt {attempt}):", raw_text[:200])

            raw_json = _extract_json_block(raw_text)
            if raw_json is None:
                print(f"[LLM DEBUG] No JSON extracted on attempt {attempt}")
                continue

            normalized = _normalize_schema(raw_json)
            if normalized is None:
                print(f"[LLM DEBUG] Could not normalize schema on attempt {attempt}")
                continue

            if not _is_valid_schema(normalized):
                print(f"[LLM DEBUG] Schema invalid after normalization on attempt {attempt}")
                continue

            # Success
            return normalized

        except Exception as e:
            print(f"[LLM ERROR] Attempt {attempt} failed with exception: {e}")

    # Final fallback if everything above fails
    print("[LLM WARN] Falling back to generic question after all attempts failed")

    return {
        "question": f"Fallback question based on learning goal: {learning_goal}",
        "A": "Concept A",
        "B": "Concept B",
        "C": "Concept C",
        "D": "Concept D",
        "correct_option": "A",
    }