from dotenv import load_dotenv
load_dotenv() 
from fastapi import FastAPI, Query, Body
from app.database import competitors_col, history_col
from datetime import datetime, timezone
from typing import List, Optional

app = FastAPI(
    title="AI Competitive Intelligence",
    description="AI-driven competitor analysis backend for AI tools",
    version="1.0.0"
)

# --------------------------------------------------
# ROOT / HEALTH
# --------------------------------------------------
@app.get("/")
def root():
    from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="AI Competitive Intelligence",
    description="AI-driven competitor analysis backend for AI tools",
    version="1.0.0"
)

@app.get("/")
def api_index():
    return {
        "success": True,
        "service": "AI Competitive Intelligence API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now(timezone.utc),
        "routes": {
            "health": {
                "method": "GET",
                "path": "/health",
                "description": "Service health check"
            },
            "competitors": {
                "method": "GET",
                "path": "/api/competitors",
                "description": "Get all AI competitors (search, pagination)"
            },
            "competitor_detail": {
                "method": "GET",
                "path": "/api/competitors/{name}",
                "description": "Get single competitor details"
            },
            "tool_names": {
                "method": "GET",
                "path": "/api/tools",
                "description": "Get all AI tool names (dropdown)"
            },
            "categories": {
                "method": "GET",
                "path": "/api/categories",
                "description": "Get all categories"
            },
            "pricing_models": {
                "method": "GET",
                "path": "/api/pricing-models",
                "description": "Get pricing models"
            },
            "history": {
                "method": "GET",
                "path": "/api/history/{name}",
                "description": "Get historical trend data"
            },
            "latest_history": {
                "method": "GET",
                "path": "/api/history/latest/{name}",
                "description": "Get latest snapshot"
            },
            "compare": {
                "method": "POST",
                "path": "/api/compare",
                "description": "Compare multiple AI tools"
            },
            "stats_overview": {
                "method": "GET",
                "path": "/api/stats/overview",
                "description": "Dashboard overview statistics"
            },
            "top_tools": {
                "method": "GET",
                "path": "/api/stats/top-tools",
                "description": "Top AI tools by AI score"
            },
            "search": {
                "method": "GET",
                "path": "/api/search?q=",
                "description": "Global search across tools"
            },
            "meta": {
                "method": "GET",
                "path": "/api/meta",
                "description": "Frontend metadata"
            },
            "docs": {
                "method": "GET",
                "path": "/docs",
                "description": "Swagger API documentation"
            }
        }
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai_competitor_analysis",
        "time": datetime.now(timezone.utc)
    }

# --------------------------------------------------
# COMPETITORS
# --------------------------------------------------
@app.get("/api/competitors")
def get_all_competitors(
    search: Optional[str] = Query(None),
    limit: int = 50,
    skip: int = 0
):
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}

    data = list(
        competitors_col.find(query, {"_id": 0})
        .skip(skip)
        .limit(limit)
    )

    total = competitors_col.count_documents(query)

    return {
        "success": True,
        "total": total,
        "count": len(data),
        "results": data
    }

@app.get("/api/competitors/{name}")
def get_competitor(name: str):
    competitor = competitors_col.find_one(
        {"name": name},
        {"_id": 0}
    )

    if not competitor:
        return {"success": False, "message": "Competitor not found"}

    return {"success": True, "data": competitor}

# --------------------------------------------------
# DROPDOWN / LIGHTWEIGHT
# --------------------------------------------------
@app.get("/api/tools")
def get_tool_names():
    names = competitors_col.distinct("name")
    return {
        "success": True,
        "count": len(names),
        "tools": sorted(names)
    }

@app.get("/api/categories")
def get_categories():
    categories = competitors_col.distinct("category")
    return {
        "success": True,
        "categories": sorted(categories)
    }

@app.get("/api/pricing")
def pricing_overview():
    data = list(
        competitors_col.find(
            {},
            {"_id": 0, "name": 1, "pricing": 1}
        )
    )
    return {
        "success": True,
        "results": data
    }


# --------------------------------------------------
# HISTORY / TRENDS
# --------------------------------------------------
@app.get("/api/history/{name}")
def get_history(name: str):
    data = list(history_col.find({"name": name}, {"_id": 0}))
    return {
        "success": True,
        "count": len(data),
        "data": data
    }

@app.get("/api/history/latest/{name}")
def latest_history(name: str):
    data = history_col.find_one(
        {"name": name},
        sort=[("timestamp", -1)],
        projection={"_id": 0}
    )
    return {"success": True, "data": data}

@app.get("/api/trends/ai-score/{name}")
def ai_score_trend(name: str):
    trend = list(
        history_col.find(
            {"name": name},
            {"_id": 0, "timestamp": 1, "aiScore": 1}
        ).sort("timestamp", 1)
    )

    return {
        "success": True,
        "count": len(trend),
        "trend": trend
    }

# --------------------------------------------------
# COMPARE
# --------------------------------------------------
@app.post("/api/compare")
def compare_tools(names: List[str] = Body(..., example=["ChatGPT", "GitHub Copilot"])):
    data = list(
        competitors_col.find(
            {"name": {"$in": names}},
            {"_id": 0}
        )
    )

    return {
        "success": True,
        "count": len(data),
        "results": data
    }

@app.post("/api/compare/summary")
def compare_summary(names: List[str] = Body(...)):
    data = list(
        competitors_col.find(
            {"name": {"$in": names}},
            {"_id": 0, "name": 1, "aiScore": 1, "category": 1, "pricingModel": 1}
        )
    )

    winner = max(data, key=lambda x: x.get("aiScore", 0))["name"] if data else None

    return {
        "success": True,
        "winner": winner,
        "results": data
    }

# --------------------------------------------------
# SWOT & STRATEGY
# --------------------------------------------------
@app.get("/api/swot/{name}")
def get_swot(name: str):
    data = competitors_col.find_one(
        {"name": name},
        {"_id": 0, "swot": 1}
    )

    if not data:
        return {"success": False, "message": "Not found"}

    return {"success": True, "swot": data.get("swot")}

@app.get("/api/strategy/{name}")
def get_strategy(name: str):
    data = competitors_col.find_one(
        {"name": name},
        {"_id": 0, "marketingStrategy": 1}
    )

    if not data:
        return {"success": False, "message": "Not found"}

    return {"success": True, "strategy": data.get("marketingStrategy")}

# --------------------------------------------------
# STATS / DASHBOARD
# --------------------------------------------------
@app.get("/api/stats/overview")
def overview():
    total = competitors_col.count_documents({})
    categories = competitors_col.distinct("category")

    return {
        "success": True,
        "totalTools": total,
        "totalCategories": len(categories),
        "categories": categories
    }

@app.get("/api/stats/top-tools")
def top_tools(limit: int = 5):
    data = list(
        competitors_col.find({}, {"_id": 0})
        .sort("aiScore", -1)
        .limit(limit)
    )

    return {"success": True, "results": data}

@app.get("/api/leaderboard")
def leaderboard(limit: int = 10):
    data = list(
        competitors_col.find(
            {},
            {"_id": 0, "name": 1, "aiScore": 1, "category": 1}
        )
        .sort("aiScore", -1)
        .limit(limit)
    )

    return {"success": True, "results": data}

# --------------------------------------------------
# SEARCH
# --------------------------------------------------
@app.get("/api/search")
def search(q: str):
    data = list(
        competitors_col.find(
            {"name": {"$regex": q, "$options": "i"}},
            {"_id": 0}
        )
    )

    return {
        "success": True,
        "count": len(data),
        "results": data
    }

# --------------------------------------------------
# FRONTEND META
# --------------------------------------------------
@app.get("/api/meta")
def meta():
    return {
        "success": True,
        "appName": "AI Competitor Intelligence",
        "version": "1.0.0",
        "features": [
            "Competitor Analysis",
            "AI Scoring",
            "SWOT Analysis",
            "Strategy Detection",
            "Trend Tracking",
            "Comparison"
        ]
    }
