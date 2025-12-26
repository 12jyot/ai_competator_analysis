from datetime import datetime, timezone
from app.config import OPENAI_API_KEY
from app.database import competitors_col, history_col
from app.data.competitors import COMPETITORS

from app.scraper.website import scrape_website
from app.scraper.blog import scrape_blog
from app.scraper.docs import scrape_docs
from app.scraper.pricing import scrape_pricing

from app.ai.openai_strategy import generate_strategy
from app.ai.swot import generate_swot
from app.ai.ai_score import generate_ai_score


def run_pipeline():
    print("🚀 Starting AI Competitive Intelligence Pipeline")

    for c in COMPETITORS:
        try:
            print(f"\n🔍 Processing: {c['name']}")

            # -------------------------
            # SCRAPING LAYER
            # -------------------------
            website_data = scrape_website(c["website"])
            blog_data = scrape_blog(c["blog"])
            docs_data = scrape_docs(c["docs"])
            pricing_data = scrape_pricing(c.get("pricing"))

            # -------------------------
            # CORE DATA OBJECT
            # -------------------------
            data = {
                "name": c["name"],
                "category": c.get("category", "AI Tool"),
                "website": c["website"],
                "blog": c["blog"],
                "docs": c["docs"],

                "websiteData": website_data,
                "blogData": blog_data,
                "docsData": docs_data,
                "pricing": pricing_data,

                "updatedAt": datetime.now(timezone.utc)
            }

            # -------------------------
            # AI INTELLIGENCE LAYER
            # -------------------------
            data["marketingStrategy"] = generate_strategy(data)
            data["swot"] = generate_swot(data)

            ai_score = generate_ai_score(data)
            data["aiScore"] = ai_score["score"]
            data["aiScoreExplanation"] = ai_score["explanation"]

            # -------------------------
            # UPSERT LATEST DATA
            # -------------------------
            competitors_col.update_one(
                {"name": data["name"]},
                {"$set": data},
                upsert=True
            )

            # -------------------------
            # SAVE HISTORICAL SNAPSHOT
            # -------------------------
            history_col.insert_one({
                "name": data["name"],
                "aiScore": data["aiScore"],
                "pricing": pricing_data,
                "marketingStrategy": data["marketingStrategy"],
                "swot": data["swot"],
                "timestamp": datetime.now(timezone.utc)
            })

            print(f"✅ Saved successfully: {c['name']}")

        except Exception as e:
            print(f"❌ Failed for {c['name']} → {str(e)}")

    print("\n🎯 Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()
