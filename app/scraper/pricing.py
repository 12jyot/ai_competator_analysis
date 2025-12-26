import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PRICE_REGEX = re.compile(r'(\$|₹|€|£)\s?\d+(\.\d+)?')

def scrape_pricing(url: str):
    """
    Scrapes pricing plans from SaaS pricing pages.
    NO AI. NO dummy data.
    """
    if not url:
        return []

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        plans = []

        # Common pricing card containers
        cards = soup.find_all(
            ["div", "section"],
            class_=lambda c: c and "price" in c.lower()
        )

        for card in cards:
            text = card.get_text(" ", strip=True)

            prices = PRICE_REGEX.findall(text)
            if not prices:
                continue

            plan = {
                "rawText": text[:300],   # safe preview
                "pricesFound": list(set([p[0] for p in prices]))
            }

            # Detect monthly / yearly
            plan["billing"] = []
            if "month" in text.lower():
                plan["billing"].append("monthly")
            if "year" in text.lower() or "annual" in text.lower():
                plan["billing"].append("yearly")

            plans.append(plan)

        return plans[:5]  # limit noise

    except Exception as e:
        return {
            "error": str(e)
        }
