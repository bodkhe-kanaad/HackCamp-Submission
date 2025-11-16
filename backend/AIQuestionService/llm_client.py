import json
import requests
import time

LLM_URL = "http://localhost:1234/v1/chat/completions"   # LM Studio default
MODEL_NAME = "Llama-3-8B-Instruct"                      # or your exact model name

# ---------------------------------------------------------
# INTERNAL HELPER — FORCE VALID JSON
# ---------------------------------------------------------
def _extract_json(text):
    """
    Finds and parses JSON from a model response.
    Auto-fixes common formatting issues.
    """
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        cleaned = text[start:end]
        return json.loads(cleaned)
    except Exception:
        return None


# ---------------------------------------------------------
# MAIN FUNCTION — GENERATE A GOOD MCQ
# ---------------------------------------------------------
def generate_llm_question(learning_goal):
    """
    Generates a clean, multiple-choice HOTS question based on
    a learning goal (RAG-selected).
    """

    prompt = f"""
You are an expert university instructor. 
You must generate ONE higher-order thinking question based on the following learning goal:

LEARNING GOAL:
"{learning_goal}"

REQUIREMENTS:
- The question must require reasoning, not memorization.
- Options MUST be 4 MCQ options: A, B, C, D
- Include exactly ONE correct answer.
- Difficulty: moderate–hard.
- No explanations, no reasoning, no markdown.

RETURN STRICT JSON OF THIS FORM ONLY:

{{
  "question": "…",
  "A": "…",
  "B": "…",
  "C": "…",
  "D": "…",
  "correct_option": "A"
}}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "max_tokens": 350,       # More expressive
        "top_p": 0.9,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0
    }

    # ---------------------------------------------------------
    # CALL LLM
    # ---------------------------------------------------------
    resp = requests.post(LLM_URL, json=payload)
    data = resp.json()

    if "choices" not in data:
        raise RuntimeError(f"LLM returned no choices: {data}")

    raw_text = data["choices"][0]["message"]["content"]

    # ---------------------------------------------------------
    # TRY TO PARSE JSON
    # ---------------------------------------------------------
    qa = _extract_json(raw_text)
    if qa and all(k in qa for k in ["question", "A", "B", "C", "D", "correct_option"]):
        return qa

    # ---------------------------------------------------------
    # If model messed up → retry with more force
    # ---------------------------------------------------------
    retry_prompt = """
Return ONLY valid JSON. 
No text before it. No text after it.

Correct your output to match EXACTLY this schema:

{
  "question": "...",
  "A": "...",
  "B": "...",
  "C": "...",
  "D": "...",
  "correct_option": "A"
}
"""

    payload["messages"].append({"role": "user", "content": retry_prompt})

    resp2 = requests.post(LLM_URL, json=payload)
    raw2 = resp2.json()["choices"][0]["message"]["content"]

    qa2 = _extract_json(raw2)
    if qa2:
        return qa2

    # ---------------------------------------------------------
    # Final fallback (safe dummy question)
    # ---------------------------------------------------------
    return {
        "question": "Fallback: What is 2 + 2?",
        "A": "3",
        "B": "4",
        "C": "5",
        "D": "22",
        "correct_option": "B"
    }