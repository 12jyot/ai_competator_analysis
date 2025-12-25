import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CompetitorBot/1.0)"
}

def scrape_blog(url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        paragraphs = []

        # Extract meaningful paragraph text
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if len(text) > 60:   # ignore short/noisy lines
                paragraphs.append(text)

        # Combine into one paragraph (limit size)
        combined_text = " ".join(paragraphs[:6])

        return {
            "blogUrl": url,
            "contentParagraph": combined_text,
            "paragraphCount": len(paragraphs)
        }

    except Exception as e:
        return {
            "blogUrl": url,
            "contentParagraph": "",
            "paragraphCount": 0,
            "error": str(e)
        }
