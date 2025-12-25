from fastapi import FastAPI, Query
from app.database import competitors_col, history_col
from datetime import datetime, timezone
from typing import List, Optional

app = FastAPI(
    title="AI Competitive Intelligence",
    description="AI-driven competitor analysis backend for AI tools",
    version="1.0.0"
)

# --------------------------------------------------
# ROOT / HEALTH CHECK
# --------------------------------------------------
@app.get("/")
def root():
    return {
        "success": True,
        "message": "AI Competitive Intelligence API is running",
        "timestamp": datetime.now(timezone.utc),
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai_competitor_analysis",
        "time": datetime.now(timezone.utc)
    }

# --------------------------------------------------
# COMPETITORS (MAIN DATA)
# --------------------------------------------------
@app.get("/api/competitors")
def get_all_competitors(
    search: Optional[str] = Query(None, description="Search by name"),
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
def get_competitor_detail(name: str):
    competitor = competitors_col.find_one(
        {"name": name},
        {"_id": 0}
    )

    if not competitor:
        return {"success": False, "message": "Competitor not found"}

    return {"success": True, "data": competitor}

# --------------------------------------------------
# DROPDOWN / LIGHTWEIGHT ROUTES
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

@app.get("/api/pricing-models")
def get_pricing_models():
    pricing = competitors_col.distinct("pricingModel")
    return {
        "success": True,
        "pricingModels": pricing
    }

# --------------------------------------------------
# HISTORY / CHART DATA
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
def get_latest_history(name: str):
    data = history_col.find_one(
        {"name": name},
        sort=[("updatedAt", -1)],
        projection={"_id": 0}
    )
    return {"success": True, "data": data}

# --------------------------------------------------
# COMPARISON (SIDE-BY-SIDE)
# --------------------------------------------------
@app.post("/api/compare")
def compare_tools(names: List[str]):
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

# --------------------------------------------------
# INSIGHTS / STATS (DASHBOARD)
# --------------------------------------------------
@app.get("/api/stats/overview")
def overview_stats():
    total_tools = competitors_col.count_documents({})
    categories = competitors_col.distinct("category")

    return {
        "success": True,
        "totalTools": total_tools,
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

# --------------------------------------------------
# SEARCH & FILTER
# --------------------------------------------------
@app.get("/api/search")
def global_search(q: str):
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
# METADATA FOR FRONTEND
# --------------------------------------------------
@app.get("/api/meta")
def frontend_meta():
    return {
        "success": True,
        "appName": "AI Competitor Intelligence",
        "version": "1.0.0",
        "features": [
            "Competitor Analysis",
            "AI Scoring",
            "Trend Tracking",
            "Tool Comparison"
        ]
    }
