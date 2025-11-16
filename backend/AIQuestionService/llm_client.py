import json
import requests
import re

# -----------------------------------
# MODEL CONFIGURATION
# -----------------------------------
LLM_URL = "http://localhost:11434/api/generate"
# For Ollama this might look like "qwen2.5:7b-instruct"
# For LM Studio, map this to the model name you exposed via the API
LLM_MODEL = "qwen2.5:7b-instruct"

MAX_TOKENS = 480
REQUEST_TIMEOUT = 60  # seconds


# -----------------------------------
# JSON CLEANING AND EXTRACTION
# -----------------------------------

def _strip_code_fences(text: str) -> str:
    """Remove ``` and ```json fences if present."""
    text = text.replace("```json", "")
    text = text.replace("```", "")
    return text.strip()


def _extract_json(text: str):
    """
    Extract the first valid JSON object from the text.
    Handles extra prose around the JSON.
    """
    if not text:
        return None

    text = _strip_code_fences(text)

    # Try direct parse first
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try to find a JSON object substring
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None

    snippet = match.group(0)
    try:
        return json.loads(snippet)
    except Exception:
        return None


REQUIRED_KEYS = ["question", "A", "B", "C", "D", "correct_option"]


def _valid_schema(obj) -> bool:
    """Check that the object matches our expected schema."""
    if not isinstance(obj, dict):
        return False

    for key in REQUIRED_KEYS:
        if key not in obj:
            return False
        if obj[key] is None:
            return False
        if isinstance(obj[key], str) and not obj[key].strip():
            return False

    if obj["correct_option"] not in ["A", "B", "C", "D"]:
        return False

    return True


def _repair_schema(obj):
    """
    Try to coerce a slightly wrong JSON into our target schema.
    Returns a fixed dict or None if cannot repair.
    Target schema:
      {
        "question": str,
        "A": str,
        "B": str,
        "C": str,
        "D": str,
        "correct_option": "A" | "B" | "C" | "D"
      }
    """
    if not isinstance(obj, dict):
        return None

    # Case: nested options
    if "question" in obj and "options" in obj and isinstance(obj["options"], dict):
        options = obj["options"]
        fixed = {
            "question": obj["question"],
            "A": options.get("A") or options.get("a") or "",
            "B": options.get("B") or options.get("b") or "",
            "C": options.get("C") or options.get("c") or "",
            "D": options.get("D") or options.get("d") or "",
            "correct_option": obj.get("correct_option")
                or obj.get("correct")
                or obj.get("answer")
        }
        if fixed["correct_option"] and isinstance(fixed["correct_option"], str):
            fixed["correct_option"] = fixed["correct_option"].strip().upper()
        if _valid_schema(fixed):
            return fixed

    # Case: correct vs correct_option mismatch
    if all(k in obj for k in ["question", "A", "B", "C", "D"]):
        fixed = {
            "question": obj["question"],
            "A": obj["A"],
            "B": obj["B"],
            "C": obj["C"],
            "D": obj["D"],
            "correct_option": obj.get("correct_option") or obj.get("correct") or obj.get("answer")
        }
        if fixed["correct_option"] and isinstance(fixed["correct_option"], str):
            fixed["correct_option"] = fixed["correct_option"].strip().upper()
        if _valid_schema(fixed):
            return fixed

    return None


# -----------------------------------
# PROMPT FOR QWEN STYLE MODELS
# -----------------------------------

def _build_prompt(learning_goal: str) -> str:
    """
    Prompt tuned for Qwen style instruction models.
    The model must output only one JSON object.
    """
    return f"""
You are an assistant that writes high quality university level multiple choice questions.

You must output exactly ONE JSON object and nothing else.
Do not include markdown. Do not include explanations. Do not include commentary.

The JSON structure must be:

{{
  "question": "A single clear question",
  "A": "Option A",
  "B": "Option B",
  "C": "Option C",
  "D": "Option D",
  "correct_option": "A"
}}

Rules:
- "correct_option" must be exactly "A", "B", "C", or "D".
- Options should be similar in length and difficulty.
- The question must require higher order thinking, not simple recall.
- The content must be based on the following learning goal:

LEARNING GOAL:
"{learning_goal}"

Now output ONLY the JSON object.
"""


# -----------------------------------
# STREAMING CALL TO LOCAL LLM
# -----------------------------------

def _call_model_streaming(prompt: str) -> str:
    """
    Call the local LLM using Ollama compatible streaming API.
    Collects all chunks' "response" fields into one string.
    """
    try:
        resp = requests.post(
            LLM_URL,
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "max_tokens": MAX_TOKENS,
                "stream": True
            },
            stream=True,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
    except Exception as e:
        print(f"[LLM ERROR] HTTP failure: {e}")
        return ""

    full_text = ""

    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue

        try:
            data = json.loads(line)
        except Exception:
            # If this is not clean JSON, just append the raw line
            full_text += str(line)
            continue

        chunk = data.get("response")
        if chunk:
            full_text += chunk

        if data.get("done"):
            break

    return full_text.strip()


# -----------------------------------
# PUBLIC ENTRYPOINT
# -----------------------------------

def generate_llm_question(learning_goal: str, retries: int = 3):
    """
    Main function used by the rest of the app.

    Returns a dict of the form:
    {
        "question": str,
        "A": str,
        "B": str,
        "C": str,
        "D": str,
        "correct_option": "A" | "B" | "C" | "D"
    }

    If the model fails repeatedly, returns a safe fallback.
    """
    prompt = _build_prompt(learning_goal)

    for attempt in range(1, retries + 1):
        print(f"[LLM] Generating question (attempt {attempt})")

        raw_text = _call_model_streaming(prompt)

        if not raw_text:
            print(f"[LLM WARNING] Empty response on attempt {attempt}")
            continue

        parsed = _extract_json(raw_text)
        if parsed is None:
            print(f"[LLM WARNING] Could not parse JSON from text (attempt {attempt})")
            print(raw_text[:300])
            continue

        if _valid_schema(parsed):
            return parsed

        repaired = _repair_schema(parsed)
        if repaired and _valid_schema(repaired):
            return repaired

        print(f"[LLM WARNING] Parsed JSON has invalid schema on attempt {attempt}: {parsed}")

    # Final fallback if all attempts fail
    print("[LLM WARNING] Falling back to static HOTS question")
    return {
        "question": "Fallback HOTS question: Based on the learning goal, which concept is most central to solving advanced problems in this topic?",
        "A": "Concept A related to the goal",
        "B": "Concept B related to the goal",
        "C": "Concept C related to the goal",
        "D": "Concept D related to the goal",
        "correct_option": "A"
    }