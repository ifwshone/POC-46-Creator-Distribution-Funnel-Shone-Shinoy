from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import random
import json

app = FastAPI(title="Real Rails API: Creator Distribution Funnel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_synthetic_funnel():
    platforms = ["YouTube", "TikTok", "Instagram", "X"]
    data = []
    for platform in platforms:
        impressions = random.randint(100000, 5000000)
        clicks = int(impressions * random.uniform(0.02, 0.08))
        watch_time_hours = int(clicks * random.uniform(0.5, 3.0))
        conversions = int(clicks * random.uniform(0.01, 0.05))
        
        data.append({
            "platform": platform,
            "impressions": impressions,
            "clicks": clicks,
            "ctr": round((clicks / impressions) * 100, 2),
            "watch_time": watch_time_hours,
            "conversions": conversions
        })
    return pd.DataFrame(data)

@app.get("/api/funnel")
async def get_funnel_data(platform_filter: str = "All"):
    df = generate_synthetic_funnel()
    if platform_filter != "All":
        df = df[df['platform'] == platform_filter]
    
    total_impressions = df['impressions'].sum()
    total_conversions = df['conversions'].sum()
    avg_conversion_rate = round((total_conversions / total_impressions) * 100, 4) if total_impressions > 0 else 0

    return {
        "metrics": df.to_dict(orient="records"),
        "aggregates": {
            "total_impressions": int(total_impressions),
            "total_conversions": int(total_conversions),
            "avg_conversion_rate": avg_conversion_rate
        }
    }

@app.get("/api/sidebar-context")
async def get_sidebar_context():
    return {
        "title": "Creator Distribution Funnel",
        "rail_category": "Distribution & Demand",
        "why_this_matters": "Directly helpful for founders and creators thinking about demand rails.",
        "who_controls": "Content creation to algorithmic reach to monetization."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)