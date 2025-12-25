import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DocsCrawler/1.0)"
}

def scrape_docs(url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        headings = []

        for tag in soup.find_all(["h1", "h2", "h3"]):
            text = tag.get_text(strip=True)
            if len(text) > 3:
                headings.append(text)

        return {
            "docsUrl": url,
            "title": soup.title.text if soup.title else "",
            "sectionsCount": len(headings),
            "topSections": headings[:10],
            "keywords": list(set(headings[:20]))
        }

    except Exception as e:
        return {
            "docsUrl": url,
            "error": str(e),
            "sectionsCount": 0,
            "topSections": [],
            "keywords": []
        }
