# 🚀 GoAsYouLikeTrip AI: Kaggle Submission Package & Cloud Deployment Guide

This package provides a step-by-step manual checklist, a copy-paste submission writeup template, and deployment instructions to publish your AI Travel Agent in the cloud.

---

## 📋 Part 1: Step-by-Step Manual Action Checklist

Here are the actions you must perform manually (since they require your accounts and authentication):

1. **Step 1: Record a video of the app**
   * Run the app locally: `/home/snehasis/miniforge3/envs/habitat3/bin/python3 main.py`
   * Open `http://localhost:8000`.
   * Use a screen recorder (e.g., OBS Studio, Loom, Zoom, or your OS built-in recorder) to record a **2-3 minute walk-through demo**.
   * Show:
     1. Setting credentials (click keys modal).
     2. Inputting a trip to **Kolkata** (Relaxed pace, 2 days, 150 USD) and showing custom fallback POIs.
     3. Inputting a trip to **Paris** (Moderate, 3 days, 400 USD, Hotel = "Hilton Paris Opera", Ages = "25, 71, 9", Meals checked).
     4. Zooming, clicking attractions on the map, and exploring the budget charts and optimization insights.
   * Upload the video to **YouTube** (as "Unlisted" or "Public").

2. **Step 2: Push code to GitHub**
   * Create a new repository on [GitHub](https://github.com/new) named `GoAsYouLikeTrip-AI`.
   * Initialize git and push your local directory:
     ```bash
     cd /home/snehasis/Code/temp/kaggle
     git init
     git add .
     git commit -m "Initial commit: GoAsYouLikeTrip AI Travel Agent"
     git branch -M main
     git remote add origin https://github.com/YOUR_GITHUB_USERNAME/GoAsYouLikeTrip-AI.git
     git push -u origin main
     ```

3. **Step 3: Deploy to the cloud**
   * Use the **Render** or **Google Cloud Run** guides below to publish the app and get a live public link (e.g., `https://goasyouliketrip.onrender.com`).

4. **Step 4: Submit on Kaggle**
   * Navigate to the **5-Day AI Agents course Kaggle competition page**: [Kaggle Competition](https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google).
   * Click **New Topic** or navigate to the submission thread.
   * Copy the markdown template in **Part 2** below, fill in your YouTube, GitHub, and Live URLs, and submit!

---

## 📝 Part 2: Official Submission Writeup Template

*Copy and paste the markdown content below directly into your Kaggle submission discussion post:*

```markdown
# Capstone Submission: GoAsYouLikeTrip AI - Multi-Agent Travel Planner

I am excited to submit my capstone project **GoAsYouLikeTrip AI**, an intelligent concierge travel planner developed during the Google 5-Day AI Agents Intensive Course.

*   **🎬 YouTube Video Demo**: [Watch the Walkthrough Video](YOUR_YOUTUBE_VIDEO_LINK_HERE)
*   **💻 GitHub Code Repository**: [View Source Code on GitHub](YOUR_GITHUB_REPOSITORY_LINK_HERE)
*   **🌐 Live Try-It-Out Link**: [Try GoAsYouLikeTrip AI Live](YOUR_LIVE_APP_URL_HERE)

---

### 1. Project Overview & Features
**GoAsYouLikeTrip AI** is a tailored city trip planner. It coordinates multi-day itineraries based on traveler demographics, budget constraints, scheduling times, and preferred pacing:
*   **Stay Location (Hotel) Round-trips**: Users can enter their hotel name. The agent geocodes the hotel and schedules each day's route to begin and end at the stay location, drawing a closed path loop on the map.
*   **Multi-Traveler Age Discounts**: Accepts list of traveler ages (e.g., `25, 71, 9`) and dynamically calculates student/youth (12-25), senior (65+), and child (under 12) entry-fee discount factors to optimize group spending.
*   **Optional Meal & Pass Suggestions**: Intersperes custom **Breakfast**, **Lunch**, and **Dinner** breaks en route and automatically recommends public transit passes (e.g., *Paris Visite Pass*, *Kolkata Smart Card*) with live links.
*   **Pacing Guardrails**: Enforces exact attraction count constraints per day (Relaxed: 2 sights/day, Moderate: 3 sights/day, Hasty: 4+ sights/day).

---

### 2. Architecture & Decision Loops
The backend system employs an agentic planning pattern with deterministic verification guardrails:
1. **POI Querying (Tools)**: Uses Nominatim Geocoding and OpenStreetMap Overpass APIs (with dynamic geocoded fallback generation for offline/unmapped areas) to locate highly rated local tourist spots.
2. **LLM Planner Node**: Utilizes **Google Gemini 2.5 Flash** (via the new `google-genai` SDK) or local **Gemma 3 (Ollama)** to compile structured schedule suggestions.
3. **Sequential Guardrail Parser (Validator)**: A python post-processing agent processes the LLM JSON output to filter duplicate hotel markers, inject missing meal breaks, and chronologically align time slots starting at the customer's specified hour.
4. **OSRM Route Optimizer**: Queries OSRM API to compute path geometry segments connecting waypoints, updating the Leaflet map overlay.

---

### 3. Technologies Used
*   **Frontend**: Vanilla HTML5, CSS3 (sleek dark mode design), Leaflet.js (maps), Chart.js (budget breakdown distribution).
*   **Backend**: Python, FastAPI, Uvicorn, Pydantic, requests.
*   **Models**: Google Gemini 2.5 Flash (via Gemini Developer API) / Ollama Gemma 3.

---

### 4. Course Takeaways & Experience
Vibe coding with Google's agent guidelines enabled me to quickly scale up from a simple layout to a robust, containerized, and deployment-ready application. Designing safety and structural guardrails around LLM outputs highlighted how hybrid systems (LLM + rules engine) achieve the highest reliability for client-facing apps.
```

---

## ☁️ Part 3: Deploying to Google AI Cloud (Google Cloud Run)

To publish your app using Google Cloud's serverless platform, follow these steps:

### 1. APIs Used in Google Cloud Run Deployment
When running in Google AI Cloud, the following APIs are activated:
1. **Gemini Developer API**: Used by the backend agent for itinerary generation.
2. **Google Places API / Google Geocoding API**: Optionally replaces OSM geocoding/POI searches for industry-grade performance.
3. **Google Artifact Registry**: Stores container images built for Cloud Run.
4. **Google Cloud Run API**: Provisions serverless instances with public URLs.

### 2. CLI Deployment Commands
First, install the Google Cloud SDK (`gcloud` CLI) on your local system, then run:

```bash
# 1. Log in to your Google Cloud account
gcloud auth login

# 2. Configure a new project
gcloud config set project YOUR_GOOGLE_CLOUD_PROJECT_ID

# 3. Enable necessary cloud services
gcloud services enable run.googleapis.com \
                       containerregistry.googleapis.com \
                       artifactregistry.googleapis.com

# 4. Build and push the container image to Google Artifact Registry
gcloud builds submit --tag gcr.io/YOUR_GOOGLE_CLOUD_PROJECT_ID/goasyouliketrip:latest

# 5. Deploy to Google Cloud Run (as serverless public container)
gcloud run deploy goasyouliketrip \
    --image gcr.io/YOUR_GOOGLE_CLOUD_PROJECT_ID/goasyouliketrip:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="GEMINI_API_KEY=YOUR_GEMINI_API_KEY" \
    --port=8080
```

Once deployment completes, the CLI outputs a **public Service URL** (e.g. `https://goasyouliketrip-xxxx-uc.a.run.app`) that anyone can use.

---

## ⚡ Part 4: 1-Click Alternate Hosting (Render)

If you prefer a simpler, zero-configuration cloud hosting option with a public URL:

1. Push your repository to **GitHub**.
2. Log in to [Render](https://render.com) using your GitHub account.
3. Click **New +** > **Web Service**.
4. Select your `GoAsYouLikeTrip-AI` repository.
5. Configure the following service settings:
   * **Language**: `Docker` (Render automatically detects your project's `Dockerfile`).
   * **Region**: Select closest to your users (e.g., `Oregon (US West)` or `Frankfurt (EU Central)`).
   * **Plan**: `Free`.
6. Add Environment Variables (optional, or users can enter them in the app settings modal):
   * `PORT` = `10000` (Render defaults to this for Docker).
7. Click **Deploy Web Service**.
8. Once built, Render provisions a permanent HTTPS link (e.g., `https://goasyouliketrip-ai.onrender.com`).
