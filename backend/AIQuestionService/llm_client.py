import json
from openai import OpenAI, OpenAIError

client = OpenAI()

SYSTEM = """
You are a multiple–choice question generator.
Always output valid JSON with keys:
question, A, B, C, D, correct.
Never output explanations or extra text.
Never use backticks.
"""

def extract_json(text):
    """Extract JSON inside <json> ... </json>."""
    if "<json>" in text and "</json>" in text:
        text = text.split("<json>")[1].split("</json>")[0]
    return text.strip()

def safe_json_parse(s):
    try:
        return json.loads(s)
    except:
        return None


def generate_llm_question(learning_goal: str):
    prompt = f"""
Generate ONE MCQ for this learning goal: "{learning_goal}"

Rules:
- Question max 25 words
- Options max 10 words each
- No reasoning
- Only JSON
- Format strictly:

<json>
{{
  "question": "...",
  "A": "...",
  "B": "...",
  "C": "...",
  "D": "...",
  "correct": "A"
}}
</json>
"""

    try:
        resp = client.chat.completions.create(
            model="llama3:8b-instruct",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=300,
        )

        raw = resp.choices[0].message.content
        json_str = extract_json(raw)

        # Try direct parse
        data = safe_json_parse(json_str)
        if data:
            return data

        # Last resort: regenerate ONCE
        resp2 = client.chat.completions.create(
            model="llama3:8b-instruct",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=300,
        )

        raw2 = resp2.choices[0].message.content
        json_str2 = extract_json(raw2)
        data2 = safe_json_parse(json_str2)

        return data2

    except OpenAIError as e:
        print("LLM ERROR:", e)
        return None