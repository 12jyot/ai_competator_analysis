from fastapi import FastAPI
from app.database import competitors_col, history_col
from datetime import datetime

app = FastAPI(title="AI Competitive Intelligence")

@app.get("/")
def root():
    return {
        "message": "AI-Driven Competitive Intelligence API",
        "status": "running",
        "endpoints": {
            "competitors": "/api/competitors",
            "history": "/api/history/{company_name}",
            "docs": "/docs"
        }
    }

@app.get("/api/competitors")
def get_competitors():
    data = list(competitors_col.find({}, {"_id": 0}))
    return {
        "count": len(data),
        "generatedAt": datetime.utcnow(),
        "results": data
    }

@app.get("/api/history/{name}")
def history(name: str):
    return list(history_col.find({"name": name}, {"_id": 0}))
