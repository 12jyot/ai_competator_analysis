from datetime import datetime, timezone
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
        print(f"\n🔍 Processing: {c['name']}")

        # -------------------------
        # SCRAPING LAYER (ALWAYS RUNS)
        # -------------------------
        try:
            website_data = scrape_website(c.get("website"))
            blog_data = scrape_blog(c.get("blog"))
            docs_data = scrape_docs(c.get("docs"))
            pricing_data = scrape_pricing(c.get("pricing"))
        except Exception as e:
            print(f"❌ Scraping failed for {c['name']} → {e}")
            continue

        # -------------------------
        # BASE DATA OBJECT
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
            "pricing": pricing_data,

            "updatedAt": datetime.now(timezone.utc)
        }

        # -------------------------
        # AI LAYER (OPTIONAL / SAFE)
        # -------------------------
        try:
            data["marketingStrategy"] = generate_strategy(data)
        except Exception as e:
            print(f"⚠️ Strategy skipped (AI issue): {e}")
            data["marketingStrategy"] = "Unavailable (AI quota or key issue)"

        try:
            data["swot"] = generate_swot(data)
        except Exception as e:
            print(f"⚠️ SWOT skipped (AI issue): {e}")
            data["swot"] = {}

        try:
            ai_score = generate_ai_score(data)
            data["aiScore"] = ai_score.get("score", 0)
            data["aiScoreExplanation"] = ai_score.get("explanation", "")
        except Exception as e:
            print(f"⚠️ AI score skipped (AI issue): {e}")
            data["aiScore"] = 0
            data["aiScoreExplanation"] = "AI scoring unavailable"

        # -------------------------
        # SAVE LATEST SNAPSHOT
        # -------------------------
        competitors_col.update_one(
            {"name": data["name"]},
            {"$set": data},
            upsert=True
        )

        # -------------------------
        # SAVE HISTORY (TREND DATA)
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

    print("\n🎯 Pipeline completed (with graceful AI handling)")


if __name__ == "__main__":
    run_pipeline()
