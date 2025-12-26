import os
from openai import OpenAI
from app.config import OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_score(competitor: dict):
    """
    Generates AI score (0–100) + explanation using OpenAI
    """

    prompt = f"""
You are an AI market analyst.

Evaluate the following AI coding tool and assign:
1. An AI Score between 0 and 100
2. A short explanation (2–3 lines)

Tool data:
Name: {competitor.get("name")}
Category: {competitor.get("category")}
Description: {competitor.get("description")}
Website: {competitor.get("website")}
Features: {competitor.get("features", [])}

Return JSON ONLY in this format:
{{
  "score": number,
  "explanation": "text"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return eval(response.choices[0].message.content)
