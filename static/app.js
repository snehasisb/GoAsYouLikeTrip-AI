// Global Variables
let map = null;
let mapMarkers = [];
let routeLines = [];
let budgetChart = null;
let currentPlanData = null;
let activeDayIndex = 0;

// API Credentials
let credentials = {
    geminiApiKey: localStorage.getItem('geminiApiKey') || '',
    googleMapsApiKey: localStorage.getItem('googleMapsApiKey') || ''
};

// Colors for daily route lines
const DAY_COLORS = ['#7c3aed', '#0891b2', '#fbbf24', '#10b981', '#ef4444'];

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    initEventListeners();
    updateModeBadge();
    loadSavedCredentialsInputs();
});

// Initialize Leaflet Map
function initMap() {
    // Center at coordinates (0, 0) initially
    map = L.map('map', {
        zoomControl: false
    }).setView([20, 0], 2);
    
    // Add custom styled dark matter map tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Place zoom control at bottom right
    L.control.zoom({
        position: 'bottomright'
    }).addTo(map);
}

// Set up UI Event Listeners
function initEventListeners() {
    // Interest tags click handler
    const tags = document.querySelectorAll('.interest-tags .tag');
    tags.forEach(tag => {
        tag.addEventListener('click', () => {
            tag.classList.toggle('active');
        });
    });

    // Form Submit
    const planForm = document.getElementById('planForm');
    planForm.addEventListener('submit', handleFormSubmit);

    // Modal Control
    const openSettingsBtn = document.getElementById('openSettingsBtn');
    const closeSettingsBtn = document.getElementById('closeSettingsBtn');
    const settingsModal = document.getElementById('settingsModal');
    const saveKeysBtn = document.getElementById('saveKeysBtn');
    const clearKeysBtn = document.getElementById('clearKeysBtn');

    openSettingsBtn.addEventListener('click', () => {
        settingsModal.classList.remove('hidden');
    });

    closeSettingsBtn.addEventListener('click', () => {
        settingsModal.classList.add('hidden');
    });

    // Close modal on clicking outside
    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.classList.add('hidden');
        }
    });

    // Save API keys
    saveKeysBtn.addEventListener('click', () => {
        const geminiInput = document.getElementById('geminiKeyInput').value.trim();
        const googleMapsInput = document.getElementById('googleMapsKeyInput').value.trim();
        
        credentials.geminiApiKey = geminiInput;
        credentials.googleMapsApiKey = googleMapsInput;
        
        localStorage.setItem('geminiApiKey', geminiInput);
        localStorage.setItem('googleMapsApiKey', googleMapsInput);
        
        updateModeBadge();
        settingsModal.classList.add('hidden');
    });

    // Clear API keys
    clearKeysBtn.addEventListener('click', () => {
        document.getElementById('geminiKeyInput').value = '';
        document.getElementById('googleMapsKeyInput').value = '';
        
        credentials.geminiApiKey = '';
        credentials.googleMapsApiKey = '';
        
        localStorage.removeItem('geminiApiKey');
        localStorage.removeItem('googleMapsApiKey');
        
        updateModeBadge();
        settingsModal.classList.add('hidden');
    });
}

// Update the badge at the top of the sidebar
function updateModeBadge() {
    const badge = document.getElementById('modeBadge');
    const text = badge.querySelector('.text');
    
    if (credentials.geminiApiKey || credentials.googleMapsApiKey) {
        badge.className = 'mode-badge premium';
        let modeText = 'Premium Mode';
        if (credentials.geminiApiKey && credentials.googleMapsApiKey) {
            modeText = 'Cloud Mode (Gemini + Maps)';
        } else if (credentials.geminiApiKey) {
            modeText = 'Gemini Active (OSM Maps)';
        } else {
            modeText = 'Google Maps Active (Ollama AI)';
        }
        text.textContent = modeText;
    } else {
        badge.className = 'mode-badge free';
        text.textContent = 'Local Free Mode (Ollama)';
    }
}

// Load credentials to inputs
function loadSavedCredentialsInputs() {
    document.getElementById('geminiKeyInput').value = credentials.geminiApiKey;
    document.getElementById('googleMapsKeyInput').value = credentials.googleMapsApiKey;
}

// Form Submission & Loading state handling
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const city = document.getElementById('cityInput').value.trim();
    const days = parseInt(document.getElementById('daysInput').value);
    const budget = parseFloat(document.getElementById('budgetInput').value);
    
    // Get active tag categories
    const activeTags = [];
    document.querySelectorAll('.interest-tags .tag.active').forEach(tag => {
        activeTags.push(tag.getAttribute('data-value'));
    });
    
    // Get transport mode
    const transport = document.querySelector('input[name="transport"]:checked').value;
    
    // Show Loading
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.classList.remove('hidden');
    
    // Reset loader step classes
    resetLoaderSteps();
    
    try {
        // Step 1: Geocoding
        updateLoaderStep('stepGeocode', 'active');
        await new Promise(r => setTimeout(r, 800)); // micro-interaction delay
        
        // Step 2: POI search
        updateLoaderStep('stepGeocode', 'done');
        updateLoaderStep('stepPOIs', 'active');
        await new Promise(r => setTimeout(r, 1200)); 
        
        // Step 3: Agent planning
        updateLoaderStep('stepPOIs', 'done');
        updateLoaderStep('stepPlan', 'active');
        
        const payload = {
            city: city,
            days: days,
            budget: budget,
            interests: activeTags,
            transport: transport,
            googleMapsApiKey: credentials.googleMapsApiKey || null,
            geminiApiKey: credentials.geminiApiKey || null
        };
        
        // Make request to backend
        const response = await fetch('/api/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`Server returned error: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        // Step 4: Routing
        updateLoaderStep('stepPlan', 'done');
        updateLoaderStep('stepRoutes', 'active');
        await new Promise(r => setTimeout(r, 800));
        
        updateLoaderStep('stepRoutes', 'done');
        
        // Hide welcome screen and load dashboard
        document.getElementById('welcomeScreen').classList.add('hidden');
        document.getElementById('dashboard').classList.remove('hidden');
        
        // Force Leaflet to recalculate size now that container is visible
        if (map) {
            setTimeout(() => {
                map.invalidateSize();
            }, 100);
        }
        
        currentPlanData = result;
        activeDayIndex = 0;
        
        // Set Titles
        document.getElementById('destinationTitle').textContent = `Explore ${result.city_name}`;
        
        // Populate day tabs & itineraries
        renderDayTabs(days);
        renderItineraryForDay(0);
        renderBudgetAllocation(result.plan.budget_summary, budget);
        
        // Hide Loading after a small buffer
        setTimeout(() => {
            loadingOverlay.classList.add('hidden');
        }, 300);
        
    } catch (error) {
        console.error(error);
        alert(`Failed to plan itinerary: ${error.message}. Make sure the FastAPI server is running.`);
        loadingOverlay.classList.add('hidden');
    }
}

// Loader UI controls
function resetLoaderSteps() {
    const steps = ['stepGeocode', 'stepPOIs', 'stepPlan', 'stepRoutes'];
    steps.forEach(s => {
        const el = document.getElementById(s);
        el.className = 'step';
    });
}

function updateLoaderStep(stepId, state) {
    const el = document.getElementById(stepId);
    el.className = `step ${state}`;
}

// Render Day Selector Tabs
function renderDayTabs(daysCount) {
    const container = document.getElementById('dayTabs');
    container.innerHTML = '';
    
    for (let i = 0; i < daysCount; i++) {
        const btn = document.createElement('button');
        btn.className = `tab ${i === 0 ? 'active' : ''}`;
        btn.textContent = `Day ${i + 1}`;
        btn.addEventListener('click', () => {
            // Switch tabs
            document.querySelectorAll('#dayTabs .tab').forEach(t => t.classList.remove('active'));
            btn.classList.add('active');
            activeDayIndex = i;
            renderItineraryForDay(i);
        });
        container.appendChild(btn);
    }
}

// Render Itinerary Cards & Map routes for active day
function renderItineraryForDay(dayIndex) {
    const dayData = currentPlanData.plan.days[dayIndex];
    const container = document.getElementById('itineraryContent');
    container.innerHTML = '';
    
    // Clear existing map overlays
    clearMapOverlays();
    
    if (!dayData || !dayData.places || dayData.places.length === 0) {
        container.innerHTML = '<div class="place-card"><p>No attractions scheduled for this day.</p></div>';
        return;
    }
    
    const places = dayData.places;
    const waypoints = [];
    
    // Day Color Code
    const color = DAY_COLORS[dayIndex % DAY_COLORS.length];
    
    places.forEach((place, idx) => {
        waypoints.push([place.lat, place.lon]);
        
        // Add Marker to Map
        const markerIcon = L.divIcon({
            className: 'custom-map-marker-container',
            html: `<div class="custom-map-marker" style="background-color: ${color}">${idx + 1}</div>`,
            iconSize: [28, 28],
            iconAnchor: [14, 14]
        });
        
        const mapMarker = L.marker([place.lat, place.lon], { icon: markerIcon }).addTo(map);
        
        // Bind Popup
        mapMarker.bindPopup(`
            <div>
                <h4>${idx + 1}. ${place.name}</h4>
                <p><strong>Time Slot:</strong> ${place.recommended_time_slot}</p>
                <p><strong>Cost:</strong> $${place.cost.toFixed(2)}</p>
                <p>${place.description}</p>
            </div>
        `);
        
        mapMarkers.push(mapMarker);
        
        // Add Itinerary DOM Element
        const card = document.createElement('div');
        card.className = 'timeline-card';
        card.innerHTML = `
            <div class="timeline-badge" style="background-color: ${color}">${idx + 1}</div>
            <div class="place-time">${place.recommended_time_slot}</div>
            <div class="place-card" data-idx="${idx}">
                <div class="place-header">
                    <h4>${place.name}</h4>
                    <span class="place-cost">${place.cost === 0 ? 'Free' : '$' + place.cost.toFixed(2)}</span>
                </div>
                <p>${place.description}</p>
            </div>
        `;
        
        // Marker zoom & highlight link
        const placeCard = card.querySelector('.place-card');
        placeCard.addEventListener('click', () => {
            // Highlight card
            document.querySelectorAll('.place-card').forEach(c => c.classList.remove('selected'));
            placeCard.classList.add('selected');
            
            // Highlight map marker
            mapMarkers.forEach(m => {
                const markEl = m.getElement()?.querySelector('.custom-map-marker');
                if (markEl) markEl.classList.remove('selected');
            });
            
            const selectedMarker = mapMarkers[idx];
            const markerDiv = selectedMarker.getElement()?.querySelector('.custom-map-marker');
            if (markerDiv) markerDiv.classList.add('selected');
            
            // Zoom map to coordinates
            map.setView([place.lat, place.lon], 15, { animate: true });
            selectedMarker.openPopup();
        });
        
        container.appendChild(card);
        
        // Add route step indicator (except for last element)
        if (idx < places.length - 1) {
            const transit = document.createElement('div');
            transit.className = 'transit-step';
            transit.textContent = `Transit to next location...`;
            container.appendChild(transit);
        }
    });
    
    // Draw route polylines
    if (dayData.route_geometry && dayData.route_geometry.length > 0) {
        // Draw precise OSRM routing geometry
        const polyline = L.polyline(dayData.route_geometry, {
            color: color,
            weight: 4,
            opacity: 0.8,
            dashArray: '2, 6' // dashed routing path
        }).addTo(map);
        routeLines.push(polyline);
    } else if (waypoints.length > 1) {
        // Fallback straight lines
        const polyline = L.polyline(waypoints, {
            color: color,
            weight: 4,
            opacity: 0.7,
            dashArray: '5, 10'
        }).addTo(map);
        routeLines.push(polyline);
    }
    
    // Auto fit map bounds around waypoints
    if (waypoints.length > 0) {
        const bounds = L.latLngBounds(waypoints);
        map.fitBounds(bounds, { padding: [50, 50] });
    }
}

// Clear map elements
function clearMapOverlays() {
    mapMarkers.forEach(m => map.removeLayer(m));
    routeLines.forEach(l => map.removeLayer(l));
    mapMarkers = [];
    routeLines = [];
}

// Render Budget Allocation Panel & Chart
function renderBudgetAllocation(summary, totalBudget) {
    const totalSpent = summary.total_spent || 0;
    const attractionCost = summary.total_attraction_cost || 0;
    const transportCost = summary.estimated_transport_cost || 0;
    const foodCost = summary.estimated_food_cost || 0;
    const remaining = Math.max(0, totalBudget - totalSpent);
    
    // Update labels/legend
    const legend = document.getElementById('budgetLegend');
    legend.innerHTML = `
        <div class="legend-item spent">
            <span class="legend-val">$${attractionCost.toFixed(0)}</span>
            <span>🏛️ Attractions</span>
        </div>
        <div class="legend-item food">
            <span class="legend-val">$${foodCost.toFixed(0)}</span>
            <span>🍴 Food</span>
        </div>
        <div class="legend-item transport">
            <span class="legend-val">$${transportCost.toFixed(0)}</span>
            <span>🚇 Transport</span>
        </div>
        <div class="legend-item remaining">
            <span class="legend-val">$${remaining.toFixed(0)}</span>
            <span>💰 Remaining</span>
        </div>
    `;
    
    // Optimization Notes
    const notesEl = document.getElementById('optimizationNotes');
    if (summary.optimization_notes) {
        notesEl.textContent = `💡 AI Agent Insights: ${summary.optimization_notes}`;
        notesEl.classList.remove('hidden');
    } else {
        notesEl.classList.add('hidden');
    }
    
    // Draw/Update Chart.js doughnut
    const ctx = document.getElementById('budgetChart').getContext('2d');
    
    if (budgetChart) {
        budgetChart.destroy();
    }
    
    budgetChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [attractionCost, foodCost, transportCost, remaining],
                backgroundColor: ['#7c3aed', '#0891b2', '#fbbf24', '#10b981'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true }
            }
        }
    });
}
