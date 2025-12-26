from openai import OpenAI
import os
from app.config import OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_pricing_with_ai(text: str):
    prompt = f"""
Extract pricing details from this text.

Return JSON with:
model, freeTier, monthly, yearly, currency.

Text:
{text}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content
