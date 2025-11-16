# llm_client.py
import json
import re
import os
from openai import OpenAI

# -----------------------------------------------------
# CONFIG
# -----------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"    # fast + good
MAX_TOKENS = 300

client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------------------------------
# JSON Extraction Helper
# -----------------------------------------------------
def _extract_json(text