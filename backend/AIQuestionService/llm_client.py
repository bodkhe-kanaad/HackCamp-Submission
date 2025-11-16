
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = "gpt-4o-mini"   # cheap, fast, reliable
MAX_TOKENS = 300


# -----------------------------------------------------
# JSON Extraction — strongest version
# -----------------------------------------------------
def extract_json_str(text: str):
    """Extract the first valid JSON object from a messy LLM response."""
    if not text:
        return None

    # Remove code fences
    cleaned = (
        text.replace("```json", "")
        .replace("```", "")
        .replace("`", "")
        .strip()
    )

    # Direct attempt
    try:
        return cleaned if json.loads(cleaned) else None
    except:
        pass

    # Regex-based extraction (greedy)
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        snippet = match.group(0)
        try:
            json.loads(snippet)
            return snippet
        except:
            pass

    return None


def parse_json(s: str):
    """Safely parse JSON string to Python dict."""
    try:
        return json.loads(s)
    except:
        return None


# -----------------------------------------------------
# SCHEMA CHECK
# -----------------------------------------------------
REQUIRED = ["question", "A", "B", "C", "D", "correct_option"]

def is_valid_schema(obj):
    if not isinstance(obj, dict):
        return False
    for k in REQUIRED:
        if k not in obj or not obj[k]:
            return False
    if obj["correct_option"] not in ["A", "B", "C", "D"]:
        return False
    return True


# -----------------------------------------------------
# PROMPT BUILDER (bulletproof)
# -----------------------------------------------------
def build_prompt(goal: str):
    return f"""
You generate EXACTLY ONE multiple-choice question in pure JSON.

RULES:
- Output ONLY a JSON object.
- NO text before or after the JSON.
- NO markdown.
- NO backticks.
- NO explanations.
- JSON must be valid and parseable by Python json.loads().
- correct_option MUST be one of: "A","B","C","D".

FORMAT YOU MUST FOLLOW EXACTLY:
{{
  "question": "University-level question here.",
  "A": "Option A",
  "B": "Option B",
  "C": "Option C",
  "D": "Option D",
  "correct_option": "A"
}}

Learning Goal:
"{goal}"

Return ONLY the JSON object. If you output anything else, the system will fail.
"""


# -----------------------------------------------------
# MAIN GENERATOR
# -----------------------------------------------------
def generate_llm_question(learning_goal: str):
    prompt = build_prompt(learning_goal)

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=MAX_TOKENS
        )

        raw = completion.choices[0].message.content
        print("\n--- RAW LLM OUTPUT ---\n", raw, "\n----------------------\n")

        json_str = extract_json_str(raw)
        if not json_str:
            print("[JSON ERROR] Could not extract JSON from model output.")
            return fallback_question()

        obj = parse_json(json_str)
        if not obj:
            print("[PARSE ERROR] Could not parse extracted JSON.")
            return fallback_question()

        if not is_valid_schema(obj):
            print("[SCHEMA ERROR] JSON missing required fields.")
            return fallback_question()

        return obj

    except Exception as e:
        print("[LLM ERROR]:", e)
        return fallback_question()


# -----------------------------------------------------
# FALLBACK — last resort ONLY
# -----------------------------------------------------
def fallback_question():
    return {
        "question": "Fallback question: Which option best describes the main concept?",
        "A": "Concept A",
        "B": "Concept B",
        "C": "Concept C",
        "D": "Concept D",
        "correct_option": "A"
    }