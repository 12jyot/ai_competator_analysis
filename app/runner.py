from datetime import datetime
from app.database import competitors_col, history_col
from app.data.competitors import COMPETITORS
from app.scraper.website import scrape_website
from app.scraper.blog import scrape_blog
from app.scraper.docs import scrape_docs
from app.ai.openai_strategy import generate_strategy
from app.ai.swot import generate_swot

def run_pipeline():
    for c in COMPETITORS:
        print("Processing:", c["name"])

        data = {
            "name": c["name"],
            "websiteData": scrape_website(c["website"]),
            "blogData": scrape_blog(c["blog"]),
            "docsData": scrape_docs(c["docs"]),
            "updatedAt": datetime.utcnow()
        }

        data["marketingStrategy"] = generate_strategy(data)
        data["swot"] = generate_swot(data)

        competitors_col.update_one(
            {"name": data["name"]},
            {"$set": data},
            upsert=True
        )

        history_col.insert_one({
            "name": data["name"],
            "snapshot": data,
            "timestamp": datetime.utcnow()
        })

        print("Saved:", c["name"])

if __name__ == "__main__":
    run_pipeline()
