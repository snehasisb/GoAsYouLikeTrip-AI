# GoAsYouLikeTrip AI - Intelligent City Trip Planner Agent

**GoAsYouLikeTrip AI** is an advanced, end-to-end travel concierge application powered by AI agents. Designed as a submission for the *Kaggle 5-Day AI Agents Intensive Course*, the application helps travelers plan optimal, budget-conscious day-by-day travel itineraries. 

By leveraging **local Ollama models (Gemma 3)** for offline utility and **Google Gemini 2.5 Flash** for premium cloud reasoning, the system clusters points of interest (POIs) spatially, tracks schedules, manages transport logistics, and optimizes overall expenses to guarantee compliance with budget bounds.

![GoAsYouLikeTrip AI Dashboard](https://raw.githubusercontent.com/username/project/main/screenshot.png) *(Placeholder for your repository screenshot - you can use `loaded_itinerary_1783361351982.png` here!)*

---

## 🚀 Key Features

1. **Dual-LLM Planning Engine**:
   - **Local / Free Mode**: Uses a local **Ollama** service running **Gemma 3 (4.3B or 270M)**. No API keys or credit cards required.
   - **Google Cloud Mode**: Seamlessly upgrades to **Gemini 2.5 Flash** using the official Google GenAI SDK if an API key is provided in the settings.

2. **Spatial POI Clustering**:
   - Fetches target attractions using **OpenStreetMap Overpass API** (Free) or **Google Places API** (Premium).
   - Groups nearby places on the same day to minimize transit times and distances.

3. **Dynamic Budget Optimization**:
   - Establishes daily transport and food estimates.
   - Tracks attraction costs. If total cost exceeds the user's budget, the AI Agent acts as an optimizer: it dynamically swaps expensive attraction entries for scenic free alternatives (e.g. public parks, photostops, viewpoints) and provides structured reasoning of its decisions in the dashboard.

4. **Real-Street Routing**:
   - Requests exact navigation geometries from **OSRM (Open Source Routing Machine)** or **Google Directions**.
   - Draws path polylines and numbered markers on an interactive Leaflet map styled in **CartoDB Dark Matter**.

5. **Premium UI Dashboard**:
   - Single-page application styled using **Vanilla CSS Glassmorphism**.
   - Animated loading indicator checklist mimicking agent actions ("Clustering locations...", "Checking budget bounds...").
   - Dynamic budget allocation visualization using a **Chart.js Doughnut Chart**.

---

## 🛠️ Architecture & Tech Stack

```
               +---------------------------------------+
               |          HTML / CSS / JS Frontend     |
               |     (Leaflet Map + Chart.js Doughnut) |
               +-------------------+-------------------+
                                   |
                                   v  POST /api/plan
               +-------------------+-------------------+
               |            FastAPI Backend            |
               +-------------------+-------------------+
                                   |
            +----------------------+----------------------+
            | Nominatim/OSRM       | Local Ollama         | Google API Client
            | (Geocode & Routes)   | (Gemma 3 Model)      | (Gemini 2.5 + Places)
            +----------------------+----------------------+
```

- **Backend**: FastAPI (Python 3.9+), Uvicorn, Requests, Pydantic, Google-GenAI SDK.
- **Frontend**: HTML5, Vanilla CSS, JS (ES6+), Leaflet.js (Map rendering), Chart.js (Budget breakdowns).

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Ollama installed and running (`gemma3:latest` pulled)

### 1. Clone & Set Up Directory
```bash
# Navigate to project workspace
cd /home/snehasis/Code/temp/kaggle
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn requests pydantic google-genai
```

### 3. Run the App
```bash
python3 main.py
```
*The application will start running on **`http://localhost:8000`**.*

---

## 📝 Kaggle Submission Writeup Draft

Below is the finalized writeup for your submission:

```markdown
# Capstone Submission: GoAsYouLikeTrip AI - Multi-Agent Concierge Travel Planner

*   **🎬 YouTube Video Walkthrough**: https://youtu.be/ud_kqIlqoZk
*   **💻 GitHub Source Code**: https://github.com/snehasisb/GoAsYouLikeTrip-AI
*   **🌐 Live Deployed Application**: https://goasyouliketrip-ai.onrender.com

---

### 📷 Application Interface Preview
Below is a screenshot of the live welcome dashboard ready to plan a new trip:

![GoAsYouLikeTrip AI Welcome Screen](https://raw.githubusercontent.com/snehasisb/GoAsYouLikeTrip-AI/main/welcome_screenshot.png)

---

### 1. Project Overview & Dynamic Agent Features
**GoAsYouLikeTrip AI** is a highly premium, dark-themed travel planner that dynamically builds and schedules day-by-day itineraries tailored to traveler demographics, transport modes, timing constraints, and budget targets:
*   **Stay Location (Hotel) Loop Routing**: Users can specify their hotel stay. The agent geocodes the hotel and wraps each day's route to start and end at the hotel (drawing closed loop routes on the map).
*   **Multi-Traveler Age Discounts**: Parses traveler ages (e.g. `25, 71, 9`) and applies group discount factors (Child <12: 50% off; Youth 12-25: 30% off; Senior 65+: 40% off) to attraction entry fees.
*   **En Route Meal Scheduling**: When active, the agent schedules Breakfast, Lunch, and Dinner breaks en route and updates the budget breakdown accordingly.
*   **Official Transit Pass Recommendations**: Analyzes the destination and budget to recommend official transit cards (e.g. *Paris Visite Pass*, *Kolkata Metro Smart Card*) with clickable direct booking links.
*   **Pacing Guardrail**: Limits the number of daily tourist spots (Relaxed = 2/day, Moderate = 3/day, Hasty = 4-5/day) to fit the user's preferred pace.

---

### 2. System Architecture & Decision Loop
The application uses a hybrid architecture combining LLM planning nodes with a deterministic Python verification and guardrail engine:

```mermaid
flowchart TD
    subgraph Client [Web Interface - HTML5 / CSS3 / JS]
        UI[User Inputs: Destination, Budget, Hotel, Ages, Pace, Meals] -->|HTTP POST Payload| API[FastAPI Backend - main.py]
        R_Map[Leaflet Map Render] <---|JSON Response| API
        R_Chart[Chart.js Budget Allocation] <---|JSON Response| API
        R_Timeline[Timeline Schedule & Links] <---|JSON Response| API
    end

    subgraph Backend_Planning [FastAPI Agent Loop - itinerary_agent.py]
        API --> Resolving[Nominatim/Google Geocoder]
        Resolving --> POIs[OpenStreetMap Overpass / Geocoded Fallbacks]
        POIs --> LLM_Node[LLM Planner Node: Gemini 2.5 Flash / Gemma 3]
        
        subgraph Guardrail_Engine [Python Rules & Optimization Guardrails]
            LLM_Node --> G_Hotel[Hotel Round-Trip Wrapper]
            G_Hotel --> G_Meals[Meal Breaks Injector]
            G_Meals --> G_Time[Chronological Time Aligner]
            G_Time --> G_Discount[Age-Based Discount Calculator]
        end

        Guardrail_Engine --> OSRM[OSRM Routing Server - Path Geometry]
    end
```

#### Decision Cycle Details:
1. **POI Querying (Tools)**: Resolves coordinates and queries OSM Overpass for local attractions. If the API limits out or returns empty results, the agent runs a custom geocoded grid fallback to distribute 8 valid local POIs around the target city.
2. **AI Agent Planning**: Google Gemini 2.5 Flash (or local Ollama Gemma 3) arranges POIs by spatial proximity to minimize travel transit overhead.
3. **Sequential Guardrail Parser (Validator)**: Adjusts times sequentially starting at the user's selected hour, injects eating stops, calculates age-based entry fee multipliers, and forces the daily loops to return to the hotel.
4. **OSRM Route Optimizer**: Queries OSRM API to compute path geometry segments connecting waypoints, which are rendered as dashed colored lines on Leaflet.

---

### 3. Core Tech Stack
*   **Frontend**: Leaflet.js (Map Visualization), Chart.js (Budget Allocation Chart), Vanilla HTML5/CSS3.
*   **Backend**: Python 3.11, FastAPI, Uvicorn, Pydantic, Requests.
*   **Models & SDKs**: `google-genai` (Google Gemini 2.5 Flash) / Local Ollama (Gemma 3).

---

### 4. Key Takeaways
Building **GoAsYouLikeTrip AI** highlighted the importance of post-processing guardrails. While LLMs are excellent at contextual clustering, adding a deterministic rules-based parser to sequence time slots, insert meals, and calculate multipliers guarantees 100% stable user experience without risking hallucinated routes or overlapping schedules.
```

---

## 🎨 License
MIT License. Created by Snehasis as part of the Kaggle AI Agents Capstone Project.
