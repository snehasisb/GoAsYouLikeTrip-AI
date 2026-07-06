# GoAsYouLikeTrip AI - Intelligent City Trip Planner Agent

**GoAsYouLikeTrip AI** is an advanced, end-to-end travel concierge application powered by AI agents. Designed as a submission for the *Kaggle 5-Day AI Agents Intensive Course*, the application helps travelers plan optimal, budget-conscious day-by-day travel itineraries. 

By leveraging **local Ollama models (Gemma 3)** for offline utility and **Google Gemini 2.5 Flash** / HIGHER for premium cloud reasoning, the system clusters points of interest (POIs) spatially, tracks schedules, manages transport logistics, and optimizes overall expenses to guarantee compliance with budget bounds.

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

```markdown
# Capstone Submission: GoAsYouLikeTrip AI - Multi-Agent Concierge Travel Planner

*   **🎬 YouTube Video Walkthrough**: https://youtu.be/ud_kqIlqoZk
*   **💻 GitHub Source Code**: https://github.com/snehasisb/GoAsYouLikeTrip-AI
*   **🌐 Live Deployed Application**: https://goasyouliketrip-ai.onrender.com

---

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
