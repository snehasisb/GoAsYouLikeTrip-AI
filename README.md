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

Below is a template draft you can copy and submit to the **Kaggle Discussion Forum** or submission box to finish your capstone project and earn your course badge:

```markdown
# Capstone Project Submission: GoAsYouLikeTrip AI
**Course:** 5-Day AI Agents Intensive Course with Google

### 1. Project Overview
GoAsYouLikeTrip AI is a concierge travel agent application that helps travelers generate day-by-day itineraries tailored to their specific budget, preferences, and transport modes. 

### 2. Agent Workflow & Decision Loop
The core agent operates in three stages:
1. **POI Retrieval & Geocoding**: The agent geocodes the target city using Nominatim/Google Maps and queries OpenStreetMap Overpass/Google Places for nearby museums, historic landmarks, and dining locations.
2. **Clustering & Schedule Generation**: The LLM (local Gemma 3 or cloud Gemini 2.5) clusters POIs based on spatial proximity to minimize travel times, schedules them into morning/afternoon/evening slots, and matches them against open hours.
3. **Constraint Solver & Budget Optimizer**: The agent aggregates total costs (entry fees + transport + food). If they exceed the user's budget, the agent replaces expensive sights with free alternatives, explaining its reasoning to the user.
4. **Path Polyline Mapping**: The backend queries OSRM for street-by-street path polylines and returns them to the frontend Leaflet map.

### 3. Technologies Used
- **Frontend**: Leaflet.js (Map Visualization), Chart.js (Budget Breakdown), Vanilla HTML5/CSS (Glassmorphism layout).
- **Backend**: FastAPI, Python.
- **AI Models**: Local Ollama (Gemma 3) or Google Gemini 2.5 Flash.

### 4. Key Takeaways from the Course
This project allowed me to implement core course principles, such as combining LLM planning with external API tools (Overpass API and OSRM), handling budget constraints dynamically, and building a responsive web GUI using vibe coding principles.
```

---

## 🎨 License
MIT License. Created by Snehasis as part of the Kaggle AI Agents Capstone Project.
