import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import osmnx as ox
from geopy.geocoders import Nominatim
from sklearn.ensemble import RandomForestRegressor

# --- 1. MODEL TRAINING (Simulated for different Franchise Personas) ---
@st.cache_resource
def train_models():
    # Model A: Premium Cafe (Likes High Income, High Traffic, Can tolerate competition)
    # Model B: Budget Tea Stall (Likes High Traffic, Schools, Low Competition)
    
    # Synthetic Training Data
    np.random.seed(42)
    n_samples = 200
    
    data = {
        'competitors': np.random.randint(0, 15, n_samples),
        'drivers': np.random.randint(5, 50, n_samples), # Schools/Offices
        'leisure': np.random.randint(0, 10, n_samples)   # Malls/Parks (Premium indicator)
    }
    df = pd.DataFrame(data)
    
    # Logic for Premium: Revenue driven by Leisure + Drivers, less hurt by competitors
    df['rev_premium'] = 5000 + (df['leisure']*300) + (df['drivers']*100) + (df['competitors']*50)
    
    # Logic for Budget: Revenue driven by Drivers only, hurt badly by competition
    df['rev_budget'] = 2000 + (df['drivers']*150) - (df['competitors']*100)
    
    model_premium = RandomForestRegressor()
    model_premium.fit(df[['competitors', 'drivers', 'leisure']], df['rev_premium'])
    
    model_budget = RandomForestRegressor()
    model_budget.fit(df[['competitors', 'drivers', 'leisure']], df['rev_budget'])
    
    return model_premium, model_budget

model_premium, model_budget = train_models()

# --- 2. GEOCODING FUNCTION (Address -> Lat/Lon) ---
def get_coords_from_address(address):
    try:
        geolocator = Nominatim(user_agent="franchise_scout_app")
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        return None, None

# --- 3. DATA EXTRACTOR (With Leisure added) ---
def get_detailed_data(lat, lon, radius):
    # Expanded tags to catch more data
    tags_competitors = {'amenity': ['cafe', 'fast_food', 'restaurant', 'coffee_shop', 'bar', 'food_court']}
    
    # Added 'building': 'university' and 'landuse': 'education' to catch campuses
    tags_drivers = {
        'amenity': ['school', 'university', 'college', 'library', 'hospital', 'bus_station'], 
        'office': True,
        'building': ['university', 'school', 'office'],
        'landuse': ['education', 'commercial']
    }
    
    tags_leisure = {'leisure': ['park', 'garden', 'playground'], 'shop': ['mall', 'department_store', 'clothes']}

    try:
        # We use a larger default search if radius is small to ensure we hit big buildings
        gdf_comps = ox.features.features_from_point((lat, lon), tags_competitors, dist=radius)
        gdf_drivers = ox.features.features_from_point((lat, lon), tags_drivers, dist=radius)
        gdf_leisure = ox.features.features_from_point((lat, lon), tags_leisure, dist=radius)
        return gdf_comps, gdf_drivers, gdf_leisure
    except:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 4. UI CONFIG ---
st.set_page_config(layout="wide", page_title="Franchise Scout Pro")
st.title("🗽 Franchise Scout: Site Intelligence Pro")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("⚙️ Configuration")
    franchise_type = st.radio("Franchise Persona", ["☕ Premium Cafe", "🍵 Budget Tea Stall"])
    radius = st.slider("Scan Radius (m)", 200, 2000, 500)
    
    st.write("---")
    st.subheader("🔍 Search Location")
    address_input = st.text_input("Enter City or Address (e.g., 'Journal Square, NJ')")
    search_btn = st.button("Search Location")

# --- STATE MANAGEMENT ---
if 'center_coords' not in st.session_state:
    st.session_state['center_coords'] = [40.7282, -74.0776] # Default Jersey City
if 'analyzed_coords' not in st.session_state:
    st.session_state['analyzed_coords'] = None

# --- LOGIC: ADDRESS SEARCH ---
if search_btn and address_input:
    lat, lon = get_coords_from_address(address_input)
    if lat:
        st.session_state['center_coords'] = [lat, lon]
        st.session_state['analyzed_coords'] = (lat, lon) # Auto-analyze on search
        st.success(f"Found: {address_input}")
    else:
        st.error("Address not found. Try adding city/state.")

# --- MAIN LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    # BASE MAP
    m = folium.Map(location=st.session_state['center_coords'], zoom_start=15)
    m.add_child(folium.LatLngPopup())
    
    # If we have analyzed data, draw the circle and pins
    if st.session_state['analyzed_coords']:
        a_lat, a_lon = st.session_state['analyzed_coords']
        
        # Draw Scan Circle
        folium.Circle([a_lat, a_lon], radius=radius, color="blue", fill=True, fill_opacity=0.1).add_to(m)
        folium.Marker([a_lat, a_lon], popup="Target Site", icon=folium.Icon(color="blue", icon="star")).add_to(m)
        
    map_output = st_folium(m, height=600, width='100%', key="main_map")

    # CLICK LISTENER
    if map_output['last_clicked']:
        st.session_state['analyzed_coords'] = (map_output['last_clicked']['lat'], map_output['last_clicked']['lng'])
        st.rerun()

# --- ANALYSIS PANEL ---
with col2:
    if st.session_state['analyzed_coords']:
        lat, lon = st.session_state['analyzed_coords']
        
        # 1. DEFINE THRESHOLDS & MODEL FIRST (To avoid NameError)
        if franchise_type == "☕ Premium Cafe":
            threshold_high = 8000
            threshold_low = 5000
            model = model_premium
        else:
            threshold_high = 4000
            threshold_low = 2500
            model = model_budget

        with st.spinner("🤖 AI Analyzing Site Potential..."):
            comps, drivers, leisure = get_detailed_data(lat, lon, radius)
            
            n_comps = len(comps) if not comps.empty else 0
            n_drivers = len(drivers) if not drivers.empty else 0
            n_leisure = len(leisure) if not leisure.empty else 0
            
            # 2. LOGIC GUARDRAIL
            if n_drivers == 0:
                pred = 0
                st.toast("⚠️ No drivers found! Revenue set to 0.")
            else:
                input_df = pd.DataFrame([[n_comps, n_drivers, n_leisure]], columns=['competitors', 'drivers', 'leisure'])
                pred = model.predict(input_df)[0]

        # DISPLAY METRICS
        st.header(f"Analysis: {franchise_type}")
        st.write(f"📍 Coords: `{lat:.4f}, {lon:.4f}`")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Competitors", n_comps, delta="-Bad" if franchise_type=="🍵 Budget Tea Stall" else "Neutral")
        c2.metric("Drivers", n_drivers, delta="+Good")
        c3.metric("Leisure", n_leisure, delta="+Premium")
        
        st.divider()
        
        # AI VERDICT
        st.subheader("💰 Revenue Forecast")
        st.metric("Est. Monthly Sales", f"${pred:,.0f}")
        
        if pred > threshold_high:
            st.success(f"🚀 **PRIME LOCATION for {franchise_type}**")
            st.markdown(f"High traffic ({n_drivers}) matches your business model perfectly.")
        elif pred > threshold_low:
            st.warning("⚠️ **VIABLE** but requires marketing.")
        else:
            st.error("❌ **AVOID** - Site Metrics too weak.")
            
    else:
        st.info("👈 Search an address or Click the map to start.")



