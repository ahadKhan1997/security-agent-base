from groq import Groq
from config import settings

# Strip literal quotes or accidental whitespace
clean_key = settings.groq_api_key.strip('"').strip("'").strip()

print(f"Sanitized Key: {clean_key[:8]}...{clean_key[-4:]}")

client = Groq(api_key=clean_key)
res = client.chat.completions.create(
    model=settings.target_model,
    messages=[{"role": "user", "content": "Hello"}]
)
print("Groq Response:", res.choices[0].message.content)