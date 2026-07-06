import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional
import os

from itinerary_agent import geocode_city, plan_itinerary_agent

app = FastAPI(
    title="GoAsYouLikeTrip AI Agent",
    description="An AI-powered concierge agent that plans optimized travel itineraries based on location, budget, and schedules.",
    version="1.0.0"
)

# CORS middleware for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request schemas
class PlanRequest(BaseModel):
    city: str = Field(..., example="Paris")
    days: int = Field(..., ge=1, le=7, example=3)
    budget: float = Field(..., gt=0, example=500.0)
    interests: List[str] = Field(default=["museums", "historical", "parks", "dining"])
    transport: str = Field(default="transit", example="transit")
    pace: str = Field(default="moderate", example="moderate")
    start_hour: int = Field(default=9, example=9)
    end_hour: int = Field(default=18, example=18)
    hotel: Optional[str] = Field(default=None, example="Hotel Hilton Paris")
    ages: str = Field(default="25", example="25, 70, 8")
    include_meals: bool = Field(default=True)
    googleMapsApiKey: Optional[str] = None
    geminiApiKey: Optional[str] = None

class GeocodeRequest(BaseModel):
    city: str = Field(..., example="Paris")
    googleMapsApiKey: Optional[str] = None

@app.post("/api/geocode")
def api_geocode(req: GeocodeRequest):
    try:
        data = geocode_city(req.city, req.googleMapsApiKey)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plan")
def api_plan(req: PlanRequest):
    try:
        # 1. Geocode city first to get coordinates
        loc = geocode_city(req.city, req.googleMapsApiKey)
        
        # 1b. Geocode hotel if specified
        hotel_data = None
        if req.hotel and req.hotel.strip():
            try:
                # Append city name to hotel to make geocoding precise
                hotel_query = f"{req.hotel.strip()}, {req.city}"
                h_loc = geocode_city(hotel_query, req.googleMapsApiKey)
                hotel_data = {
                    "name": req.hotel.strip(),
                    "lat": h_loc["lat"],
                    "lon": h_loc["lon"]
                }
            except Exception as he:
                print(f"Failed to geocode hotel: {he}")
                # Fallback: place hotel slightly offset from city center
                hotel_data = {
                    "name": req.hotel.strip(),
                    "lat": loc["lat"] - 0.005,
                    "lon": loc["lon"] - 0.005
                }
        
        # Parse ages
        age_list = []
        try:
            age_list = [int(a.strip()) for a in req.ages.split(",") if a.strip()]
        except:
            age_list = [25]
        if not age_list:
            age_list = [25]
        
        # 2. Generate optimized itinerary via the agent
        itinerary = plan_itinerary_agent(
            city_name=req.city,
            lat=loc["lat"],
            lon=loc["lon"],
            days=req.days,
            budget=req.budget,
            interests=req.interests,
            transport=req.transport,
            pace=req.pace,
            start_hour=req.start_hour,
            end_hour=req.end_hour,
            hotel_data=hotel_data,
            ages=age_list,
            include_meals=req.include_meals,
            gemini_key=req.geminiApiKey,
            google_key=req.googleMapsApiKey
        )
        
        return {
            "success": True,
            "city_name": loc["display_name"],
            "lat": loc["lat"],
            "lon": loc["lon"],
            "plan": itinerary
        }
    except Exception as e:
        print(f"Error in api_plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files from the 'static' directory
# Place this at the end to avoid hijacking API routes
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
