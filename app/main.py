from fastapi import FastAPI
from app.database import competitors_col, history_col
from datetime import datetime, timezone

app = FastAPI(
    title="AI Competitive Intelligence",
    description="AI-driven competitor analysis for AI coding tools",
    version="1.0.0"
)

# -------------------------------
# Root / Health Check
# -------------------------------
@app.get("/")
def root():
    return {
        "success": True,
        "message": "AI-Driven Competitive Intelligence API",
        "status": "running",
        "endpoints": {
            "all_competitors": "/api/competitors",
            "single_competitor": "/api/competitors/{name}",
            "history": "/api/history/{name}",
            "tool_names": "/api/tools",
            "docs": "/docs"
        }
    }

# -------------------------------
# Get ALL competitors
# -------------------------------
@app.get("/api/competitors")
def get_competitors():
    data = list(competitors_col.find({}, {"_id": 0}))
    return {
        "success": True,
        "count": len(data),
        "generatedAt": datetime.now(timezone.utc),
        "results": data
    }

# -------------------------------
# Get SINGLE competitor by name
# -------------------------------
@app.get("/api/competitors/{name}")
def get_competitor(name: str):
    competitor = competitors_col.find_one(
        {"name": name},
        {"_id": 0}
    )

    if not competitor:
        return {
            "success": False,
            "message": "Competitor not found"
        }

    return {
        "success": True,
        "data": competitor
    }

# -------------------------------
# Historical trend data
# -------------------------------
@app.get("/api/history/{name}")
def history(name: str):
    data = list(history_col.find({"name": name}, {"_id": 0}))
    return {
        "success": True,
        "count": len(data),
        "data": data
    }

# -------------------------------
# Get ALL AI tool names (lightweight)
# -------------------------------
@app.get("/api/tools")
def get_all_tool_names():
    names = competitors_col.distinct("name")
    return {
        "success": True,
        "count": len(names),
        "tools": sorted(names)
    }
