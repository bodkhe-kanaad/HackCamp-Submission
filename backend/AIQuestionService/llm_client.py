import json
import requests

def generate_llm_question(learning_goal):
    prompt = f"""
You are an educational AI assistant.

Create ONE high-quality conceptual question based on this learning goal:

LEARNING GOAL:
{learning_goal}

Return ONLY JSON in this exact format:
{{
 "question": "...",
 "A": "...",
 "B": "...",
 "C": "...",
 "D": "...",
 "correct": "A"
}}
"""

    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json={
            "model": "lmstudio",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )

    raw = response.json()["choices"][0]["message"]["content"]
    return json.loads(raw)