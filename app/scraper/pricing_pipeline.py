from app.scraper.pricing import scrape_pricing
from app.ai.pricing_ai import extract_pricing_with_ai

def get_pricing_data(url):
    data = scrape_pricing(url)

    if data.get("monthly") or data.get("yearly"):
        return data

    # fallback to AI
    ai_data = extract_pricing_with_ai(data.get("rawText", ""))
    return {
        "model": "Subscription",
        "rawText": ai_data
    }
