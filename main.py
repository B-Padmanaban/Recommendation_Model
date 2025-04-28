from fastapi import FastAPI, Request
from recommender import recommend_schemes

app = FastAPI()

@app.post("/recommend")
async def get_recommendation(user_data: dict):
    try:
        recommendations = recommend_schemes(user_data)
        return {"success": True, "recommendations": recommendations}
    except Exception as e:
        return {"success": False, "error": str(e)}
