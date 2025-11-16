import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from AIQuestionService.ai_question_service import generate_llm_question

print("OK!")