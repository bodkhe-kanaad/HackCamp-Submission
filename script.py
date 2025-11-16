import os
from openai import OpenAI

# Debug print
print("=== DEBUG ===")
print("OPENAI_API_KEY exists:", "OPENAI_API_KEY" in os.environ)

if "OPENAI_API_KEY" in os.environ:
    print("KEY PREVIEW:", os.environ["OPENAI_API_KEY"][:5] + "*****")
else:
    print("NO KEY FOUND!")
    raise SystemExit("Secret not available to workflow.")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello"}]
)

print("\nAI RESPONSE:")
print(resp.choices[0].message.content)