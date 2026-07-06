import json
import requests
import math
from typing import List, Dict, Any, Optional

# Pre-curated premium attractions for popular cities (failsafe database)
CURATED_CITIES = {
    "paris": {
        "center": {"lat": 48.8566, "lon": 2.3522},
        "places": [
            {"name": "Eiffel Tower", "lat": 48.8584, "lon": 2.2945, "cost": 29.0, "duration_minutes": 120, "open_hours": "09:00 - 00:45", "category": "landmark", "description": "Iconic iron lattice tower on the Champ de Mars, offering panoramic views of Paris."},
            {"name": "Louvre Museum", "lat": 48.8606, "lon": 2.3376, "cost": 22.0, "duration_minutes": 180, "open_hours": "09:00 - 18:00", "category": "museum", "description": "The world's largest art museum and a historic monument, home to the Mona Lisa."},
            {"name": "Cathédrale Notre-Dame", "lat": 48.8530, "lon": 2.3499, "cost": 0.0, "duration_minutes": 60, "open_hours": "08:00 - 18:45", "category": "historical", "description": "Famous medieval Catholic cathedral, a masterpiece of French Gothic architecture."},
            {"name": "Arc de Triomphe", "lat": 48.8738, "lon": 2.2950, "cost": 16.0, "duration_minutes": 60, "open_hours": "10:00 - 23:00", "category": "landmark", "description": "Monument standing at the western end of the Champs-Élysées, honoring war heroes."},
            {"name": "Sainte-Chapelle", "lat": 48.8554, "lon": 2.3450, "cost": 13.0, "duration_minutes": 45, "open_hours": "09:00 - 19:00", "category": "historical", "description": "Royal medieval Gothic chapel, featuring stunning 13th-century stained glass windows."},
            {"name": "Jardin du Luxembourg", "lat": 48.8462, "lon": 2.3371, "cost": 0.0, "duration_minutes": 90, "open_hours": "07:30 - 21:30", "category": "park", "description": "Beautiful 17th-century palace garden with fountains, tree-lined promenades, and lawns."},
            {"name": "Musée d'Orsay", "lat": 48.8599, "lon": 2.3266, "cost": 16.0, "duration_minutes": 150, "open_hours": "09:30 - 18:00", "category": "museum", "description": "Museum in a grand former railway station housing the world's largest collection of impressionist art."},
            {"name": "Montmartre & Sacré-Cœur", "lat": 48.8867, "lon": 2.3431, "cost": 0.0, "duration_minutes": 120, "open_hours": "06:00 - 22:30", "category": "landmark", "description": "Historic hilltop neighborhood and stunning white basilica overlooking the city."},
            {"name": "Champs-Élysées", "lat": 48.8698, "lon": 2.3079, "cost": 0.0, "duration_minutes": 90, "open_hours": "24/7", "category": "shopping", "description": "World-famous avenue lined with theaters, cafes, luxury shops, and chestnut trees."},
            {"name": "Centre Pompidou", "lat": 48.8606, "lon": 2.3522, "cost": 15.0, "duration_minutes": 120, "open_hours": "11:00 - 21:00", "category": "museum", "description": "High-tech architectural marvel housing Europe's largest museum of modern art."}
        ]
    },
    "tokyo": {
        "center": {"lat": 35.6762, "lon": 139.6503},
        "places": [
            {"name": "Sensō-ji Temple", "lat": 35.7148, "lon": 139.7967, "cost": 0.0, "duration_minutes": 90, "open_hours": "06:00 - 17:00", "category": "historical", "description": "Tokyo's oldest and most famous Buddhist temple, located in Asakusa."},
            {"name": "Tokyo Skytree", "lat": 35.7101, "lon": 139.8107, "cost": 20.0, "duration_minutes": 120, "open_hours": "10:00 - 21:00", "category": "landmark", "description": "The tallest structure in Japan, offering jaw-dropping views of the metropolis."},
            {"name": "Shibuya Crossing", "lat": 35.6595, "lon": 139.7005, "cost": 0.0, "duration_minutes": 45, "open_hours": "24/7", "category": "landmark", "description": "The busiest pedestrian crossing in the world, surrounded by neon screens and shopping."},
            {"name": "Meiji Jingu Shrine", "lat": 35.6764, "lon": 139.6993, "cost": 0.0, "duration_minutes": 90, "open_hours": "05:00 - 18:00", "category": "historical", "description": "Shinto shrine dedicated to Emperor Meiji, nestled in a dense, peaceful forest."},
            {"name": "Shinjuku Gyoen National Garden", "lat": 35.6852, "lon": 139.7101, "cost": 3.5, "duration_minutes": 120, "open_hours": "09:00 - 16:30", "category": "park", "description": "Large imperial garden blending traditional Japanese, English landscape, and French formal styles."},
            {"name": "teamLab Planets", "lat": 35.6489, "lon": 139.7901, "cost": 28.0, "duration_minutes": 120, "open_hours": "09:00 - 22:00", "category": "museum", "description": "Immersive digital art museum where visitors walk through water and colorful projection spaces."},
            {"name": "Tokyo Tower", "lat": 35.6586, "lon": 139.7454, "cost": 8.0, "duration_minutes": 90, "open_hours": "09:00 - 22:30", "category": "landmark", "description": "Eiffel Tower-inspired communication and observation tower painted in white and orange."},
            {"name": "Tsukiji Outer Market", "lat": 35.6655, "lon": 139.7702, "cost": 0.0, "duration_minutes": 90, "open_hours": "05:00 - 14:00", "category": "dining", "description": "Lively street market packed with stalls selling fresh sushi, street snacks, and kitchen goods."},
            {"name": "Akihabara Electric Town", "lat": 35.6997, "lon": 139.7715, "cost": 0.0, "duration_minutes": 120, "open_hours": "10:00 - 21:00", "category": "shopping", "description": "Epicenter of electronics, anime, gaming culture, and maid cafes."}
        ]
    },
    "new york": {
        "center": {"lat": 40.7128, "lon": -74.0060},
        "places": [
            {"name": "Statue of Liberty & Ellis Island", "lat": 40.6892, "lon": -74.0445, "cost": 25.0, "duration_minutes": 180, "open_hours": "08:30 - 16:00", "category": "historical", "description": "Historic national monument offering harbor cruises and immigrant history exhibits."},
            {"name": "Central Park", "lat": 40.7829, "lon": -73.9654, "cost": 0.0, "duration_minutes": 180, "open_hours": "06:00 - 01:00", "category": "park", "description": "Massive urban park in Manhattan featuring lakes, woodlands, zoo, and beautiful bridges."},
            {"name": "Metropolitan Museum of Art (The Met)", "lat": 40.7794, "lon": -73.9632, "cost": 30.0, "duration_minutes": 180, "open_hours": "10:00 - 17:00", "category": "museum", "description": "One of the world's finest art museums, spanning 5,000 years of global culture."},
            {"name": "Empire State Building", "lat": 40.7484, "lon": -73.9857, "cost": 44.0, "duration_minutes": 90, "open_hours": "09:00 - 00:00", "category": "landmark", "description": "Iconic Art Deco skyscraper with world-famous 86th and 102nd floor observation decks."},
            {"name": "9/11 Memorial & Museum", "lat": 40.7115, "lon": -74.0131, "cost": 33.0, "duration_minutes": 120, "open_hours": "09:00 - 19:00", "category": "museum", "description": "Poignant memorial at the site of the Twin Towers, with reflecting pools and historical museum."},
            {"name": "Times Square", "lat": 40.7580, "lon": -73.9855, "cost": 0.0, "duration_minutes": 60, "open_hours": "24/7", "category": "landmark", "description": "The neon-lit heart of the theater district and one of the world's most visited tourist attractions."},
            {"name": "High Line Park", "lat": 40.7480, "lon": -74.0048, "cost": 0.0, "duration_minutes": 90, "open_hours": "07:00 - 22:00", "category": "park", "description": "Elevated public park built on a historic freight rail line along Manhattan's West Side."},
            {"name": "Brooklyn Bridge", "lat": 40.7061, "lon": -73.9969, "cost": 0.0, "duration_minutes": 70, "open_hours": "24/7", "category": "historical", "description": "Stunning neo-Gothic suspension bridge connecting Manhattan and Brooklyn."}
        ]
    },
    "london": {
        "center": {"lat": 51.5074, "lon": -0.1278},
        "places": [
            {"name": "British Museum", "lat": 51.5194, "lon": -0.1270, "cost": 0.0, "duration_minutes": 180, "open_hours": "10:00 - 17:00", "category": "museum", "description": "Dedicated to human history, art and culture, housing the Rosetta Stone."},
            {"name": "Tower of London & Tower Bridge", "lat": 51.5081, "lon": -0.0759, "cost": 34.0, "duration_minutes": 150, "open_hours": "09:00 - 17:30", "category": "historical", "description": "Historic castle on the north bank of the Thames, home to the Crown Jewels."},
            {"name": "London Eye", "lat": 51.5033, "lon": -0.1195, "cost": 38.0, "duration_minutes": 45, "open_hours": "11:00 - 18:00", "category": "landmark", "description": "Giant observation wheel on the South Bank of the River Thames."},
            {"name": "Westminster Abbey & Big Ben", "lat": 51.4994, "lon": -0.1273, "cost": 29.0, "duration_minutes": 120, "open_hours": "09:30 - 15:30", "category": "historical", "description": "Gothic coronation church and iconic clock tower at the Houses of Parliament."},
            {"name": "Hyde Park", "lat": 51.5073, "lon": -0.1657, "cost": 0.0, "duration_minutes": 120, "open_hours": "05:00 - 00:00", "category": "park", "description": "One of the largest royal parks in London, featuring the Serpentine lake."},
            {"name": "Tate Modern", "lat": 51.5076, "lon": -0.0994, "cost": 0.0, "duration_minutes": 120, "open_hours": "10:00 - 18:00", "category": "museum", "description": "National gallery of international modern and contemporary art in a former power station."},
            {"name": "Covent Garden", "lat": 51.5117, "lon": -0.1240, "cost": 0.0, "duration_minutes": 90, "open_hours": "09:00 - 23:00", "category": "dining", "description": "Vibrant district featuring street performers, market stalls, boutiques, and restaurants."}
        ]
    }
}

# Helper to calculate distance between coordinates
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Radius of Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Geocoding function
def geocode_city(city_name: str, google_key: Optional[str] = None) -> Dict[str, Any]:
    city_clean = city_name.strip().lower()
    
    # 1. Check local cache
    if city_clean in CURATED_CITIES:
        return {
            "lat": CURATED_CITIES[city_clean]["center"]["lat"],
            "lon": CURATED_CITIES[city_clean]["center"]["lon"],
            "display_name": city_name.title()
        }
    
    # 2. Use Google Geocoding if key is provided
    if google_key:
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={requests.utils.quote(city_name)}&key={google_key}"
            res = requests.get(url, timeout=10).json()
            if res.get("status") == "OK":
                loc = res["results"][0]["geometry"]["location"]
                return {
                    "lat": loc["lat"],
                    "lon": loc["lng"],
                    "display_name": res["results"][0]["formatted_address"]
                }
        except Exception as e:
            print(f"Google Geocoding failed: {e}")
            
    # 3. Fallback to Nominatim OpenStreetMap (requires user-agent)
    try:
        headers = {"User-Agent": "AntigravityCityTripPlannerAgent/1.0"}
        url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(city_name)}&format=json&limit=1"
        res = requests.get(url, headers=headers, timeout=10).json()
        if res:
            return {
                "lat": float(res[0]["lat"]),
                "lon": float(res[0]["lon"]),
                "display_name": res[0]["display_name"]
            }
    except Exception as e:
        print(f"Nominatim Geocoding failed: {e}")
        
    # Final default fallback (Paris)
    return {
        "lat": 48.8566,
        "lon": 2.3522,
        "display_name": f"{city_name} (Estimated location, default Paris coordinates)"
    }

# Search points of interest (POIs)
def fetch_pois(city_name: str, lat: float, lon: float, google_key: Optional[str] = None) -> List[Dict[str, Any]]:
    city_clean = city_name.strip().lower()
    
    # 1. Use local cache if available for major cities (best quality)
    if city_clean in CURATED_CITIES:
        return CURATED_CITIES[city_clean]["places"]
        
    # 2. Use Google Places if key is provided
    if google_key:
        try:
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=5000&type=tourist_attraction&key={google_key}"
            res = requests.get(url, timeout=10).json()
            if res.get("status") in ["OK", "ZERO_RESULTS"]:
                places = []
                for item in res.get("results", [])[:15]:
                    cost_level = item.get("price_level", 1) # estimation
                    est_cost = 10.0 * cost_level if cost_level else 0.0
                    places.append({
                        "name": item["name"],
                        "lat": item["geometry"]["location"]["lat"],
                        "lon": item["geometry"]["location"]["lng"],
                        "cost": est_cost,
                        "duration_minutes": 90,
                        "open_hours": "09:00 - 18:00",
                        "category": "attraction",
                        "description": item.get("vicinity", "A popular local attraction.")
                    })
                if places:
                    return places
        except Exception as e:
            print(f"Google Places failed: {e}")
            
    # 3. Fallback to OpenStreetMap Overpass API
    try:
        url = "https://overpass-api.de/api/interpreter"
        # Search for tourist attractions, museums, viewpoints, historical elements, and parks within 6km
        query = f"""
        [out:json][timeout:15];
        (
          node["tourism"="museum"](around:6000, {lat}, {lon});
          node["tourism"="attraction"](around:6000, {lat}, {lon});
          node["tourism"="viewpoint"](around:6000, {lat}, {lon});
          node["historic"](around:6000, {lat}, {lon});
          way["tourism"="museum"](around:6000, {lat}, {lon});
          way["tourism"="attraction"](around:6000, {lat}, {lon});
          way["historic"](around:6000, {lat}, {lon});
        );
        out center 15;
        """
        res = requests.post(url, data={"data": query}, timeout=15).json()
        places = []
        for element in res.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name")
            if not name:
                continue
            
            # Estimate lat/lon
            p_lat = element.get("lat") or element.get("center", {}).get("lat")
            p_lon = element.get("lon") or element.get("center", {}).get("lon")
            if not p_lat or not p_lon:
                continue
                
            # Category extraction
            category = "attraction"
            if "museum" in tags.get("tourism", ""):
                category = "museum"
            elif "viewpoint" in tags.get("tourism", ""):
                category = "viewpoint"
            elif tags.get("historic"):
                category = "historical"
            elif "park" in tags.get("leisure", ""):
                category = "park"
                
            # Estimate cost based on category
            cost = 0.0
            if category == "museum":
                cost = 15.0
            elif category == "attraction":
                cost = 12.0
            
            places.append({
                "name": name,
                "lat": float(p_lat),
                "lon": float(p_lon),
                "cost": cost,
                "duration_minutes": 120 if category in ["museum", "attraction"] else 60,
                "open_hours": "09:00 - 17:30" if category in ["museum", "historical"] else "24/7",
                "category": category,
                "description": tags.get("description") or f"A notable {category} in {city_name}."
            })
            
        if places:
            return places
    except Exception as e:
        print(f"Overpass POI search failed: {e}")
        
    # If all fails, use Paris as dummy default
    return CURATED_CITIES["paris"]["places"]

# Get exact routing via OSRM
def fetch_route_geometry(waypoints: List[Dict[str, float]], mode: str = "foot") -> List[List[float]]:
    if len(waypoints) < 2:
        return []
        
    osrm_mode = "foot" if mode == "walking" else "driving"
    coords_str = ";".join([f"{wp['lon']},{wp['lat']}" for wp in waypoints])
    url = f"https://router.project-osrm.org/route/v1/{osrm_mode}/{coords_str}?overview=full&geometries=geojson"
    
    try:
        res = requests.get(url, timeout=10).json()
        if res.get("code") == "Ok":
            routes = res.get("routes", [])
            if routes:
                # OSRM returns coordinates as [lon, lat] - we need [lat, lon] for Leaflet
                geom = routes[0]["geometry"]["coordinates"]
                return [[coord[1], coord[0]] for coord in geom]
    except Exception as e:
        print(f"OSRM routing failed: {e}")
        
    # Fallback to straight line segments
    line_coords = []
    for i in range(len(waypoints) - 1):
        line_coords.append([waypoints[i]["lat"], waypoints[i]["lon"]])
        line_coords.append([waypoints[i+1]["lat"], waypoints[i+1]["lon"]])
    return line_coords

# AI Agent loop: plans and optimizes the itinerary
def plan_itinerary_agent(
    city_name: str, 
    lat: float, 
    lon: float, 
    days: int, 
    budget: float, 
    interests: List[str], 
    transport: str,
    gemini_key: Optional[str] = None
) -> Dict[str, Any]:
    
    # 1. Fetch available POIs
    pois = fetch_pois(city_name, lat, lon)
    
    # 2. Formulate prompt for LLM
    poi_list_str = "\n".join([
        f"- {p['name']} (Lat: {p['lat']}, Lon: {p['lon']}, Cost: ${p['cost']}, Open: {p['open_hours']}, Duration: {p['duration_minutes']}m, Category: {p['category']}): {p['description']}"
        for p in pois
    ])
    
    prompt = f"""You are an expert AI Travel Agent. Your task is to plan a structured, optimal, day-by-day travel itinerary for a city trip.
City: {city_name}
Duration: {days} days
Total Budget: ${budget} USD
Preferences/Interests: {", ".join(interests)}
Transport Mode: {transport} (walking, driving, transit)

Here is a list of available Attractions/Points of Interest (POIs):
{poi_list_str}

Please plan the itinerary following these strict rules:
1. Divide the attractions into {days} separate days. Group nearby places on the same day (minimize travel distances).
2. Schedule a maximum of 3-4 places per day (morning, afternoon, evening). Ensure they fit within their open hours.
3. Keep track of costs. Estimate:
   - Attraction Costs (use the provided costs, or adjust if they are too high)
   - Transport Cost: Estimate ${2 if transport == "walking" else 8 if transport == "transit" else 20} per day for transport.
   - Food Cost: Estimate $30 per day for food.
4. Budget Constraint: The sum of Attraction Costs + Transport Costs + Food Costs MUST NOT exceed the total budget of ${budget} USD.
   If the total cost exceeds the budget, YOU MUST OPTIMIZE: Swap expensive attractions with free attractions (e.g. parks, scenic walks, free landmarks) and document this in the 'optimization_notes'.
5. Return ONLY a valid JSON object matching the following structure. Do not include markdown code block syntax (like ```json) in your raw response, just output the JSON itself:
{{
  "days": [
    {{
      "day_number": 1,
      "places": [
        {{
          "name": "Attraction Name",
          "lat": 48.8584,
          "lon": 2.2945,
          "cost": 15.0,
          "duration_minutes": 120,
          "open_hours": "09:00 - 18:00",
          "recommended_time_slot": "09:00 - 11:00",
          "category": "landmark",
          "description": "Short description of what the user does there."
        }}
      ]
    }}
  ],
  "budget_summary": {{
    "total_attraction_cost": 45.0,
    "estimated_transport_cost": 24.0,
    "estimated_food_cost": 90.0,
    "total_spent": 159.0,
    "remaining_budget": 341.0,
    "optimization_notes": "Explanation of budget choices, changes made, and travel recommendations."
  }}
}}"""

    raw_response = ""
    # 3. Call LLM (Gemini or local Ollama)
    if gemini_key:
        print("Using Gemini API...")
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            raw_response = response.text
        except Exception as e:
            print(f"Gemini API execution failed, falling back to local Ollama: {e}")
            gemini_key = None # trigger local Ollama fallback
            
    if not gemini_key:
        print("Using local Ollama (gemma3:latest)...")
        try:
            res = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "gemma3:latest",
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1}
                },
                timeout=45
            ).json()
            raw_response = res.get("response", "").strip()
        except Exception as e:
            print(f"Ollama execution failed: {e}")
            
    # Parse the response
    plan_data = None
    if raw_response:
        try:
            # Strip any markdown block formatting just in case
            cleaned = raw_response
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            plan_data = json.loads(cleaned)
        except Exception as parse_error:
            print(f"JSON parsing failed for LLM response: {parse_error}")
            print(f"Raw Response was: {raw_response}")

    # 4. Fallback Logic: Deterministic Rules-based Planner if LLM failed or response is malformed
    if not plan_data:
        print("LLM planning failed. Applying deterministic rules-based fallback agent...")
        # Sort POIs by distance from center
        sorted_pois = sorted(pois, key=lambda x: haversine_distance(lat, lon, x["lat"], x["lon"]))
        
        # Simple clustering: split sorted list into groups of days
        places_per_day = math.ceil(len(sorted_pois) / days)
        if places_per_day < 2:
            places_per_day = 2
            
        days_list = []
        total_attraction_cost = 0.0
        
        for d in range(days):
            day_places = []
            start_idx = d * places_per_day
            end_idx = min(start_idx + places_per_day, len(sorted_pois))
            
            # Select places for this day
            candidate_places = sorted_pois[start_idx:end_idx]
            
            # Time scheduler
            current_hour = 9
            for i, p in enumerate(candidate_places):
                cost = p["cost"]
                
                # Dynamic Budget Optimization: If we are low on budget, swap high-cost items
                if total_attraction_cost + cost + (days * 30.0) + (days * 8.0) > budget:
                    # Swap with free item/skip cost
                    cost = 0.0
                    p["name"] = f"{p['name']} (Free Walk outside / Photo Stop)"
                    p["description"] = f"Viewed from outside to fit within budget constraint. {p['description']}"
                
                total_attraction_cost += cost
                duration = p["duration_minutes"]
                start_str = f"{current_hour:02d}:00"
                end_hour = current_hour + math.ceil(duration / 60)
                end_str = f"{end_hour:02d}:00"
                
                day_places.append({
                    "name": p["name"],
                    "lat": p["lat"],
                    "lon": p["lon"],
                    "cost": cost,
                    "duration_minutes": duration,
                    "open_hours": p["open_hours"],
                    "recommended_time_slot": f"{start_str} - {end_str}",
                    "category": p["category"],
                    "description": p["description"]
                })
                current_hour = end_hour + 1 # 1 hour gap/transit
                
            days_list.append({
                "day_number": d + 1,
                "places": day_places
            })
            
        estimated_transport_cost = days * (2.0 if transport == "walking" else 8.0 if transport == "transit" else 20.0)
        estimated_food_cost = days * 30.0
        total_spent = total_attraction_cost + estimated_transport_cost + estimated_food_cost
        
        plan_data = {
            "days": days_list,
            "budget_summary": {
                "total_attraction_cost": total_attraction_cost,
                "estimated_transport_cost": estimated_transport_cost,
                "estimated_food_cost": estimated_food_cost,
                "total_spent": total_spent,
                "remaining_budget": budget - total_spent,
                "optimization_notes": "Itinerary planned using spatial clustering. Swapped expensive entrances to outer views if budget bounds were exceeded."
            }
        }

    # 5. Route calculation (add map geometries to each day)
    for day in plan_data["days"]:
        places = day.get("places", [])
        if len(places) >= 2:
            waypoints = [{"lat": p["lat"], "lon": p["lon"]} for p in places]
            day["route_geometry"] = fetch_route_geometry(waypoints, transport)
        else:
            day["route_geometry"] = []
            
    return plan_data

if __name__ == "__main__":
    # Self-test run
    result = plan_itinerary_agent("Paris", 48.8566, 2.3522, 2, 200.0, ["museums", "landmarks"], "walking")
    print(json.dumps(result, indent=2))
