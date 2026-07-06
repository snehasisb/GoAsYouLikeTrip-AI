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
        
    # If all fails or returned places is empty, generate generic attractions custom to the requested city
    print(f"Generating fallback generic attractions for {city_name}...")
    
    # Generic names tailored to requested city
    attractions = [
        {"suffix": "Central Park & Gardens", "category": "park", "cost": 0.0, "duration": 120, "desc": "A beautiful public green space with walking trails, fountains, and relaxing spots."},
        {"suffix": "National Museum of Art", "category": "museum", "cost": 15.0, "duration": 150, "desc": "Housing a magnificent collection of historic artifacts, sculptures, and galleries."},
        {"suffix": "Historic Landmark Tower", "category": "landmark", "cost": 10.0, "duration": 90, "desc": "A famous architectural marvel offering panoramic views of the city skyline."},
        {"suffix": "Old Town Square", "category": "historical", "cost": 0.0, "duration": 90, "desc": "Steeped in local history, featuring old buildings, street performers, and cafes."},
        {"suffix": "Scenic Riverwalk Promenade", "category": "landmark", "cost": 0.0, "duration": 60, "desc": "A scenic path along the water, perfect for photography and relaxing strolls."},
        {"suffix": "Science & Tech Center", "category": "museum", "cost": 18.0, "duration": 120, "desc": "Interactive exhibits, science shows, and fun learning activities for everyone."},
        {"suffix": "Traditional Food Market", "category": "dining", "cost": 0.0, "duration": 90, "desc": "A bustling local market with stalls selling traditional snacks, fruits, and food."},
        {"suffix": "City Center Botanical Garden", "category": "park", "cost": 5.0, "duration": 100, "desc": "Stunning greenhouses, exotic plants, and peaceful walking pathways."}
    ]
    
    fallback_places = []
    for i, attr in enumerate(attractions):
        # Distribute points within a ~3km radius
        offset_lat = 0.015 * math.sin(i * 2 * math.pi / len(attractions))
        offset_lon = 0.015 * math.cos(i * 2 * math.pi / len(attractions))
        
        fallback_places.append({
            "name": f"{city_name.title()} {attr['suffix']}",
            "lat": lat + offset_lat,
            "lon": lon + offset_lon,
            "cost": attr["cost"],
            "duration_minutes": attr["duration"],
            "open_hours": "09:00 - 18:00" if attr["category"] in ["museum", "historical"] else "24/7",
            "category": attr["category"],
            "description": f"{attr['desc']} Located in the heart of {city_name}."
        })
    return fallback_places

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

# Itinerary Guardrail and Sequence Formatting
def guardrail_and_format_itinerary(
    plan_data: Dict[str, Any],
    hotel_data: Optional[Dict[str, Any]],
    ages: List[int],
    include_meals: bool,
    start_hour: int,
    end_hour: int,
    pace: str,
    transport: str,
    budget: float,
    days: int,
    city_pass: str
):
    # Calculate group multiplier
    multiplier_sum = 0.0
    for age in ages:
        if age < 12: multiplier_sum += 0.5
        elif age <= 25: multiplier_sum += 0.7
        elif age >= 65: multiplier_sum += 0.6
        else: multiplier_sum += 1.0

    for day in plan_data.get("days", []):
        places = day.get("places", [])
        
        # Filter existing places (discard any old Start/End markers)
        filtered_places = []
        for p in places:
            if p.get("category") == "hotel" and (p["name"].startswith("Start:") or p["name"].startswith("End:")):
                continue
            # Remove any trailing / Hotel / Restaurant from names if we want clean formatting
            filtered_places.append(p)
            
        # Check if breakfast, lunch, dinner are already present
        has_breakfast = any("breakfast" in p["name"].lower() or p.get("category") == "restaurant" and "breakfast" in p["description"].lower() for p in filtered_places)
        has_lunch = any("lunch" in p["name"].lower() or p.get("category") == "restaurant" and "lunch" in p["description"].lower() for p in filtered_places)
        has_dinner = any("dinner" in p["name"].lower() or p.get("category") == "restaurant" and "dinner" in p["description"].lower() for p in filtered_places)
        
        if include_meals:
            # Inject breakfast
            if not has_breakfast:
                filtered_places.insert(0, {
                    "name": "Breakfast Break",
                    "lat": hotel_data["lat"] if hotel_data else (filtered_places[0]["lat"] if filtered_places else 0),
                    "lon": hotel_data["lon"] if hotel_data else (filtered_places[0]["lon"] if filtered_places else 0),
                    "cost": 8.0 * len(ages),
                    "duration_minutes": 45,
                    "open_hours": "24/7",
                    "category": "restaurant",
                    "description": "Enjoy breakfast at a local cafe to start the day."
                })
            # Inject lunch
            if not has_lunch:
                mid_index = len(filtered_places) // 2 if filtered_places else 0
                filtered_places.insert(mid_index, {
                    "name": "Lunch en route",
                    "lat": filtered_places[mid_index-1]["lat"] if mid_index > 0 else (hotel_data["lat"] if hotel_data else 0),
                    "lon": filtered_places[mid_index-1]["lon"] if mid_index > 0 else (hotel_data["lon"] if hotel_data else 0),
                    "cost": 12.0 * len(ages),
                    "duration_minutes": 60,
                    "open_hours": "24/7",
                    "category": "restaurant",
                    "description": "Take a rest and enjoy local specialties for lunch."
                })
            # Inject dinner
            if not has_dinner:
                filtered_places.append({
                    "name": "Dinner Break",
                    "lat": hotel_data["lat"] if hotel_data else (filtered_places[-1]["lat"] if filtered_places else 0),
                    "lon": hotel_data["lon"] if hotel_data else (filtered_places[-1]["lon"] if filtered_places else 0),
                    "cost": 20.0 * len(ages),
                    "duration_minutes": 90,
                    "open_hours": "24/7",
                    "category": "restaurant",
                    "description": "Unwind with dinner at a traditional local restaurant."
                })

        # Insert hotel start/end markers
        if hotel_data:
            filtered_places.insert(0, {
                "name": f"Start: {hotel_data['name']}",
                "lat": hotel_data["lat"],
                "lon": hotel_data["lon"],
                "cost": 0.0,
                "duration_minutes": 0,
                "open_hours": "24/7",
                "category": "hotel",
                "description": "Depart from hotel to start the day's adventure."
            })
            filtered_places.append({
                "name": f"End: {hotel_data['name']}",
                "lat": hotel_data["lat"],
                "lon": hotel_data["lon"],
                "cost": 0.0,
                "duration_minutes": 0,
                "open_hours": "24/7",
                "category": "hotel",
                "description": "Return to hotel for a restful night."
            })
            
        # Re-schedule times sequentially starting at start_hour
        current_hour = start_hour
        current_minute = 0
        
        for p in filtered_places:
            duration = p.get("duration_minutes", 60)
            if p.get("category") == "hotel":
                duration = 0
                
            start_str = f"{current_hour:02d}:{current_minute:02d}"
            
            current_minute += duration
            current_hour += current_minute // 60
            current_minute = current_minute % 60
            
            if p.get("category") == "hotel":
                p["recommended_time_slot"] = f"{start_str} - {start_str}"
            else:
                end_str = f"{current_hour:02d}:{current_minute:02d}"
                p["recommended_time_slot"] = f"{start_str} - {end_str}"
                
                # Gap after activity (except for restaurant/hotel)
                if p.get("category") not in ["hotel", "restaurant"]:
                    current_minute += 30
                    current_hour += current_minute // 60
                    current_minute = current_minute % 60
                    
        day["places"] = filtered_places

    # Recalculate budget summary
    total_attraction = 0.0
    total_food = 0.0
    for day in plan_data.get("days", []):
        for p in day.get("places", []):
            if p.get("category") == "restaurant":
                total_food += p.get("cost", 0.0)
            elif p.get("category") not in ["hotel"]:
                total_attraction += p.get("cost", 0.0)
                
    estimated_transport = days * (2.0 if transport == "walking" else 8.0 if transport == "transit" else 20.0) * len(ages)
    total_spent = total_attraction + total_food + estimated_transport
    
    if "budget_summary" not in plan_data:
        plan_data["budget_summary"] = {}
        
    plan_data["budget_summary"]["total_attraction_cost"] = total_attraction
    plan_data["budget_summary"]["estimated_transport_cost"] = estimated_transport
    plan_data["budget_summary"]["estimated_food_cost"] = total_food
    plan_data["budget_summary"]["total_spent"] = total_spent
    plan_data["budget_summary"]["remaining_budget"] = budget - total_spent
    
    # Prepend age discount info to optimization notes
    orig_notes = plan_data["budget_summary"].get("optimization_notes", "")
    plan_data["budget_summary"]["optimization_notes"] = (
        f"Group Profile: {len(ages)} traveler(s) with ages {ages} (Multiplier: {multiplier_sum:.2f}x). "
        f"Pass Rec: {city_pass}. "
        f"{orig_notes}"
    )

# AI Agent loop: plans and optimizes the itinerary
def plan_itinerary_agent(
    city_name: str, 
    lat: float, 
    lon: float, 
    days: int, 
    budget: float, 
    interests: List[str], 
    transport: str,
    pace: str = "moderate",
    start_hour: int = 9,
    end_hour: int = 18,
    hotel_data: Optional[Dict[str, Any]] = None,
    ages: List[int] = [25],
    include_meals: bool = True,
    gemini_key: Optional[str] = None,
    google_key: Optional[str] = None
) -> Dict[str, Any]:
    
    # 1. Fetch available POIs
    pois = fetch_pois(city_name, lat, lon, google_key)
    
    # Calculate traveler multiplier
    multiplier_sum = 0.0
    traveler_types = []
    for age in ages:
        if age < 12:
            multiplier_sum += 0.5
            traveler_types.append(f"Child (age {age}, 50% discount)")
        elif age <= 25:
            multiplier_sum += 0.7
            traveler_types.append(f"Student/Youth (age {age}, 30% discount)")
        elif age >= 65:
            multiplier_sum += 0.6
            traveler_types.append(f"Senior (age {age}, 40% discount)")
        else:
            multiplier_sum += 1.0
            traveler_types.append(f"Adult (age {age})")
            
    # Recommendations for transit / passes
    pass_recommendations = {
        "paris": "Paris Visite Pass (Unlimited transit in zones 1-3 from €13.90/day. Details: https://www.ratp.fr/en/titres-et-tarifs/paris-visite-pass)",
        "london": "Visitor Oyster Card (Daily caps apply. Details: https://tfl.gov.uk/travel-information/visiting-london)",
        "tokyo": "Tokyo Subway 24/48/72-Hour Ticket (Unlimited subway from ¥800. Details: https://www.tokyometro.jp/en/ticket/travel/)",
        "new york": "MTA MetroCard / OMNY (Pay-per-ride or 7-Day Unlimited for $34. Details: https://new.mta.info/fares)",
        "kolkata": "Kolkata Metro Smart Card (Offers 10% discount on standard fares. Details: https://mtp.indianrailways.gov.in/)"
    }
    city_pass = pass_recommendations.get(
        city_name.lower(), 
        f"{city_name.title()} Public Transit Pass (Buy a local tourist day pass for discounted transit. Search details on Google.)"
    )
    
    # 2. Formulate prompt for LLM
    poi_list_str = "\n".join([
        f"- {p['name']} (Lat: {p['lat']}, Lon: {p['lon']}, Cost: ${p['cost']}, Open: {p['open_hours']}, Duration: {p['duration_minutes']}m, Category: {p['category']}): {p['description']}"
        for p in pois
    ])
    
    prompt = f"""You are an expert AI Travel Agent. Your task is to plan a structured, day-by-day travel itinerary for a city trip.
City: {city_name}
Duration: {days} days
Total Budget: ${budget} USD
Preferences/Interests: {", ".join(interests)}
Transport Mode: {transport}

Traveler Profile:
- Number of travelers: {len(ages)}
- Ages: {", ".join(map(str, ages))}
- Traveler Breakdown: {", ".join(traveler_types)}
- Total Group Discount Factor: {multiplier_sum:.2f}x (Note: child < 12 is 50% cost, student 12-25 is 70% cost, senior 65+ is 60% cost). Make sure to sum up attraction admission costs across ALL travelers using their ages and apply these discounts!

Starting/Ending Hotel Location:
{f'- Name: {hotel_data["name"]}, Latitude: {hotel_data["lat"]}, Longitude: {hotel_data["lon"]}' if hotel_data else '- No hotel location specified. Start directly at attractions.'}

Meal Suggestions:
{'- Include breakfast, lunch, and dinner recommendations in the itinerary timeline (at appropriate hours: e.g. ~08:30, ~13:00, ~19:30).' if include_meals else '- Do not schedule detailed meal slots.'}

Transit Pass & Discounts Recommendation:
{city_pass}

Here is a list of available Attractions/Points of Interest (POIs):
{poi_list_str}

Please plan the itinerary following these strict rules:
1. Hotel Integration: If a hotel is specified, start each day at the hotel, visit attractions, and end each day back at the hotel.
2. Schedule places based on the preferred pace:
   - relaxed (1-2 attractions/day)
   - moderate (3 attractions/day)
   - hasty (4-5 attractions/day)
3. Timing Constraint: Start activities at {start_hour}:00, and end no later than {end_hour}:00.
4. Intersperse meals (breakfast, lunch, dinner) at suitable times if meals are requested.
5. Budget Constraint: The sum of Group Attraction Costs + Group Transport Costs + Group Food Costs MUST NOT exceed the total budget of ${budget} USD.
   If the total cost exceeds the budget, YOU MUST OPTIMIZE: Swap expensive attractions with free attractions or recommend cheaper dining and document this in the 'optimization_notes'.
6. Include the suggested transit pass name and link in the 'optimization_notes'.
7. Return ONLY a valid JSON object matching the following structure. Do not include markdown code block syntax (like ```json) in your raw response, just output the JSON itself:
{{
  "days": [
    {{
      "day_number": 1,
      "places": [
        {{
          "name": "Attraction Name / Hotel / Restaurant",
          "lat": 48.8584,
          "lon": 2.2945,
          "cost": 15.0, // calculated group cost (multiplied by group factor)
          "duration_minutes": 120,
          "open_hours": "09:00 - 18:00",
          "recommended_time_slot": "09:00 - 11:00",
          "category": "landmark", // "hotel", "restaurant", or "landmark"/"museum"/etc.
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
    "optimization_notes": "Explanation of budget choices, discounts applied, and links for recommended passes."
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
        
        # Determine places per day based on pace
        if pace == "relaxed":
            places_per_day = 2
        elif pace == "hasty":
            places_per_day = 4
        else:
            places_per_day = 3
            
        days_list = []
        total_attraction_cost = 0.0
        
        for d in range(days):
            day_places = []
            
            # Start at Hotel
            if hotel_data:
                day_places.append({
                    "name": f"Start: {hotel_data['name']}",
                    "lat": hotel_data["lat"],
                    "lon": hotel_data["lon"],
                    "cost": 0.0,
                    "duration_minutes": 0,
                    "open_hours": "24/7",
                    "recommended_time_slot": f"{start_hour:02d}:00 - {start_hour:02d}:00",
                    "category": "hotel",
                    "description": "Depart from hotel to start the day's adventure."
                })
            
            current_hour = start_hour
            
            # Optional Breakfast
            if include_meals:
                day_places.append({
                    "name": "Breakfast Break",
                    "lat": hotel_data["lat"] if hotel_data else lat,
                    "lon": hotel_data["lon"] if hotel_data else lon,
                    "cost": 8.0 * len(ages),
                    "duration_minutes": 45,
                    "open_hours": "24/7",
                    "recommended_time_slot": f"{current_hour:02d}:00 - {current_hour:02d}:45",
                    "category": "restaurant",
                    "description": "Enjoy a local breakfast to fuel up for the day."
                })
                current_hour += 1
            
            start_idx = d * places_per_day
            end_idx = min(start_idx + places_per_day, len(sorted_pois))
            candidate_places = sorted_pois[start_idx:end_idx]
            
            for i, p in enumerate(candidate_places):
                # Apply traveler age discounts
                cost = p["cost"] * multiplier_sum
                
                # Check lunch insertion
                if include_meals and current_hour >= 13 and not any(dp["category"] == "restaurant" and "Lunch" in dp["name"] for dp in day_places):
                    day_places.append({
                        "name": "Lunch en route",
                        "lat": p["lat"],
                        "lon": p["lon"],
                        "cost": 12.0 * len(ages),
                        "duration_minutes": 60,
                        "open_hours": "24/7",
                        "recommended_time_slot": "13:00 - 14:00",
                        "category": "restaurant",
                        "description": "Enjoy lunch near attractions."
                    })
                    current_hour = max(current_hour, 14)
                
                # Dynamic Budget Optimization
                total_est_so_far = total_attraction_cost + cost + (days * 30.0 * len(ages)) + (days * (2.0 if transport == "walking" else 8.0 if transport == "transit" else 20.0))
                if total_est_so_far > budget:
                    cost = 0.0
                    p["name"] = f"{p['name']} (Free Walk outside / Photo Stop)"
                    p["description"] = f"Viewed from outside to fit within budget constraint. {p['description']}"
                
                total_attraction_cost += cost
                duration = p["duration_minutes"]
                start_str = f"{current_hour:02d}:00"
                e_hour = current_hour + math.ceil(duration / 60)
                if e_hour > end_hour:
                    e_hour = end_hour
                end_str = f"{e_hour:02d}:00"
                
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
                current_hour = e_hour + 1 # transit gap
                if current_hour >= end_hour:
                    break
            
            # Optional Dinner
            if include_meals and current_hour < end_hour:
                day_places.append({
                    "name": "Dinner Break",
                    "lat": hotel_data["lat"] if hotel_data else lat,
                    "lon": hotel_data["lon"] if hotel_data else lon,
                    "cost": 20.0 * len(ages),
                    "duration_minutes": 90,
                    "open_hours": "24/7",
                    "recommended_time_slot": f"{current_hour:02d}:00 - {min(current_hour+2, end_hour):02d}:00",
                    "category": "restaurant",
                    "description": "Relax with dinner at a traditional local restaurant."
                })
                current_hour = min(current_hour + 2, end_hour)
            
            # End at Hotel
            if hotel_data:
                day_places.append({
                    "name": f"End: {hotel_data['name']}",
                    "lat": hotel_data["lat"],
                    "lon": hotel_data["lon"],
                    "cost": 0.0,
                    "duration_minutes": 0,
                    "open_hours": "24/7",
                    "recommended_time_slot": f"{end_hour:02d}:00 - {end_hour:02d}:00",
                    "category": "hotel",
                    "description": "Return to hotel for a restful night."
                })
                
            days_list.append({
                "day_number": d + 1,
                "places": day_places
            })
            
        estimated_transport_cost = days * (2.0 if transport == "walking" else 8.0 if transport == "transit" else 20.0) * len(ages)
        estimated_food_cost = days * 30.0 * len(ages)
        total_spent = total_attraction_cost + estimated_transport_cost + estimated_food_cost
        
        plan_data = {
            "days": days_list,
            "budget_summary": {
                "total_attraction_cost": total_attraction_cost,
                "estimated_transport_cost": estimated_transport_cost,
                "estimated_food_cost": estimated_food_cost,
                "total_spent": total_spent,
                "remaining_budget": budget - total_spent,
                "optimization_notes": f"Itinerary planned using spatial clustering. Group size: {len(ages)} traveler(s) with ages {ages}. {city_pass}"
            }
        }

    # Apply post-processing guardrail to align hotel, meals, and times
    guardrail_and_format_itinerary(
        plan_data=plan_data,
        hotel_data=hotel_data,
        ages=ages,
        include_meals=include_meals,
        start_hour=start_hour,
        end_hour=end_hour,
        pace=pace,
        transport=transport,
        budget=budget,
        days=days,
        city_pass=city_pass
    )

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
