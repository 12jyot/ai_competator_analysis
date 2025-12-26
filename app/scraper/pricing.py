import requests
from bs4 import BeautifulSoup
import re

def scrape_pricing(url: str):
    try:
        r = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0"
        })
        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        monthly = re.search(r"\$ ?(\d+)\s*/\s*month", text, re.I)
        yearly = re.search(r"\$ ?(\d+)\s*/\s*year", text, re.I)
        free = re.search(r"free\s+(tier|plan)", text, re.I)

        return {
            "model": "Subscription",
            "freeTier": bool(free),
            "monthly": int(monthly.group(1)) if monthly else None,
            "yearly": int(yearly.group(1)) if yearly else None,
            "currency": "USD",
            "rawText": text[:800]
        }

    except Exception as e:
        return {
            "model": "Unknown",
            "error": str(e)
        }
