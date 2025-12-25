import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        return {
            "title": soup.title.text if soup.title else "",
            "metaDescription": soup.find("meta", {"name": "description"}).get("content", "")
            if soup.find("meta", {"name": "description"}) else ""
        }
    except:
        return {}
