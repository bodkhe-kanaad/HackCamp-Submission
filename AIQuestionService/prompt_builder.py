def build_hots_prompt(course, week, learning_goal):
    return f"""
You are an expert university-level tutor.

Using this learning goal:

"{learning_goal}"

Generate ONE higher-order thinking MCQ that assesses this outcome.

Rules:
- The question must require reasoning (not recall).
- Provide exactly 4 answer choices (A, B, C, D).
- All choices should be plausible.
- Provide exactly one correct answer.
- Output JSON only:

{{
  "question": "...",
  "option_A": "...",
  "option_B": "...",
  "option_C": "...",
  "option_D": "...",
  "correct_option": "A"
}}

Do not add explanations.
Do not add markdown.
"""