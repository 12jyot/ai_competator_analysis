from datetime import datetime, timezone
from app.database import competitors_col, history_col
from app.data.competitors import COMPETITORS

from app.scraper.website import scrape_website
from app.scraper.blog import scrape_blog
from app.scraper.docs import scrape_docs

from app.ai.openai_strategy import generate_strategy
from app.ai.swot import generate_swot
from app.ai.ai_score import generate_ai_score


def run_pipeline():
    print("🚀 Starting AI Competitive Analysis Pipeline")

    for c in COMPETITORS:
        try:
            print(f"🔍 Processing: {c['name']}")

            # -------------------------
            # Scraping Layer
            # -------------------------
            website_data = scrape_website(c["website"])
            blog_data = scrape_blog(c["blog"])
            docs_data = scrape_docs(c["docs"])

            # -------------------------
            # Core Data Object
            # -------------------------
            data = {
                "name": c["name"],
                "category": c.get("category", "AI Tool"),
                "website": c.get("website"),
                "blog": c.get("blog"),
                "docs": c.get("docs"),

                "websiteData": website_data,
                "blogData": blog_data,
                "docsData": docs_data,

                "updatedAt": datetime.now(timezone.utc)
            }

            # -------------------------
            # AI Analysis Layer
            # -------------------------
            data["marketingStrategy"] = generate_strategy(data)
            data["swot"] = generate_swot(data)

            ai_score = generate_ai_score(data)
            data["aiScore"] = ai_score["score"]
            data["aiScoreExplanation"] = ai_score["explanation"]

            # -------------------------
            # Save Competitor (UPSERT)
            # -------------------------
            competitors_col.update_one(
                {"name": data["name"]},
                {"$set": data},
                upsert=True
            )

            # -------------------------
            # Historical Snapshot
            # -------------------------
            history_col.insert_one({
                "name": data["name"],
                "aiScore": data["aiScore"],
                "marketingStrategy": data["marketingStrategy"],
                "swot": data["swot"],
                "timestamp": datetime.now(timezone.utc)
            })

            print(f"✅ Saved: {c['name']}")

        except Exception as e:
            print(f"❌ Error processing {c['name']}: {str(e)}")

    print("🎯 Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()
