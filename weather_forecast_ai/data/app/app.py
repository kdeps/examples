import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_extras.let_it_rain import rain
from streamlit_option_menu import option_menu
from geopy.geocoders import Nominatim
import json
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide", page_title="Global Weather Insights 🌍")

# Initialize session state
if 'city' not in st.session_state:
    st.session_state.city = "Amsterdam"
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'coordinates' not in st.session_state:
    st.session_state.coordinates = {'lat': 52.366, 'lon': 4.901}  # Updated from JSON

# Fallback weather data (based on provided JSON)
FALLBACK_WEATHER_DATA = {
    "api": {
        "latitude": 52.366,
        "longitude": 4.901,
        "current_weather": {
            "temperature": 20.0,
            "windspeed": 29.9,
            "winddirection": 246,
            "weathercode": 63
        },
        "hourly": {
            "time": [
                "2025-08-04T00:00", "2025-08-04T01:00", "2025-08-04T02:00", "2025-08-04T03:00",
                "2025-08-04T04:00", "2025-08-04T05:00", "2025-08-04T06:00", "2025-08-04T07:00",
                "2025-08-04T08:00", "2025-08-04T09:00", "2025-08-04T10:00", "2025-08-04T11:00",
                "2025-08-04T12:00", "2025-08-04T13:00", "2025-08-04T14:00", "2025-08-04T15:00",
                "2025-08-04T16:00", "2025-08-04T17:00", "2025-08-04T18:00", "2025-08-04T19:00",
                "2025-08-04T20:00", "2025-08-04T21:00", "2025-08-04T22:00", "2025-08-04T23:00"
            ],
            "temperature_2m": [
                19.4, 19.5, 19.3, 19.1, 18.9, 18.3, 19.0, 19.5, 20.5, 20.6, 20.0, 20.9,
                21.2, 22.4, 23.1, 21.0, 21.2, 22.0, 20.7, 20.0, 19.9, 19.8, 19.7, 19.2
            ],
            "precipitation": [
                0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                0.00, 0.00, 0.00, 0.10, 0.00, 0.00, 0.90, 4.10, 0.60, 0.00, 0.00, 0.00
            ]
        },
        "daily": {
            "time": ["2025-08-04"],
            "temperature_2m_max": [23.1],
            "temperature_2m_min": [18.3],
            "precipitation_sum": [5.70]
        }
    },
    "activities": "Consider indoor activities like visiting museums (e.g., Rijksmuseum) due to rain. For outdoor options, Vondelpark is great with proper rain gear.",
    "dining_recommendations": "Try comfort food at De Kas or Bauta for hearty stews. Café Papeneiland offers a cozy heated terrace.",
    "fitness_options": "Indoor options like Fitness First or Yoga Studio Amsterdam are ideal due to rain.",
    "health_advice": "Wear waterproof clothing and apply SPF 30 for UV protection despite rain.",
    "local_insights": "Visit ice rinks or Jordaan for photogenic spots. Albert Cuyp Market is open daily except Sundays."
}

# Geocoding function
@st.cache_data
def get_coordinates(city):
    try:
        geolocator = Nominatim(user_agent="weather_app_streamlit_2025_contact@example.com")
        time.sleep(1)  # Respect Nominatim rate limits
        location = geolocator.geocode(city, country_codes="nl", timeout=10)
        if location:
            logger.info(f"Geocoded {city}: ({location.latitude}, {location.longitude})")
            return {'lat': location.latitude, 'lon': location.longitude}
        logger.warning(f"No coordinates found for {city}")
        return None
    except Exception as e:
        logger.error(f"Geocoding failed for {city}: {e}")
        st.error(f"⚠️ Geocoding failed: {e}. Try specifying the country (e.g., 'Amsterdam, Netherlands').")
        return None

# Fetch weather function with retries
@st.cache_data
def fetch_weather(city):
    query = f"What is the weather in {city}?"
    try:
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        session.mount("http://", HTTPAdapter(max_retries=retries))
        url = f"http://localhost:3000/api/v1/weather?q={query}"
        res = session.post(url, timeout=15)
        if res.status_code == 200 and res.json().get("success"):
            logger.info(f"Weather data fetched for {city}")
            return res.json()["response"]["data"][0]
        logger.warning(f"No weather data returned for {city}")
        return None
    except Exception as e:
        logger.error(f"Failed to fetch weather data for {city}: {e}")
        st.error(f"🚫 Failed to fetch weather data: {e}. Using fallback data for Amsterdam.")
        return FALLBACK_WEATHER_DATA

# Parse weather data for dashboard
def parse_weather_data(data):
    if not data or 'api' not in data:
        return {
            'current_temp': None,
            'wind_speed': None,
            'wind_direction': None,
            'precipitation': None,
            'today_high': None,
            'today_low': None,
            'condition': None,
            'hourly_data': None
        }
    
    api_data = data['api']
    weather_code = api_data['current_weather']['weathercode']
    condition = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain"
    }.get(weather_code, "Unknown")

    hourly_data = []
    for i, time_str in enumerate(api_data['hourly']['time']):
        if datetime.strptime(time_str, "%Y-%m-%dT%H:%M").date() == datetime(2025, 8, 4).date():
            hourly_data.append({
                'time': time_str.split('T')[1][:5],
                'temperature': api_data['hourly']['temperature_2m'][i],
                'precipitation': api_data['hourly']['precipitation'][i]
            })

    return {
        'current_temp': api_data['current_weather']['temperature'],
        'wind_speed': api_data['current_weather']['windspeed'],
        'wind_direction': api_data['current_weather']['winddirection'],
        'precipitation': api_data['daily']['precipitation_sum'][0],
        'today_high': api_data['daily']['temperature_2m_max'][0],
        'today_low': api_data['daily']['temperature_2m_min'][0],
        'condition': condition,
        'hourly_data': hourly_data
    }

# Summarize text for brevity
def summarize_text(text, max_words=50):
    words = text.split()
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + "..."
    return text

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        "Navigation", ["Weather", "Map", "Chart"],
        icons=["cloud", "map", "bar-chart"],
        menu_icon="cast", default_index=0)

    city = st.text_input("Enter a city or country", value=st.session_state.city)
    submit = st.button("Get Weather")

# Handle city submission
if submit:
    if not city.strip():
        st.error("⚠️ Please enter a valid city name.")
    else:
        st.session_state.city = city
        with st.spinner("Fetching weather data..."):
            get_coordinates.clear()
            st.session_state.weather_data = fetch_weather(city)
            coords = get_coordinates(city)
            if coords:
                st.session_state.coordinates = coords
            else:
                st.session_state.coordinates = {'lat': 52.366, 'lon': 4.901}

# Weather Page (Dashboard with Infographic)
if selected == "Weather":
    if st.session_state.weather_data:
        data = st.session_state.weather_data
        metrics = parse_weather_data(data)
        st.title(f"📍 Weather Dashboard for {st.session_state.city}")

        # Weather Metrics
        st.subheader("🌤️ Current Conditions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                label="Temperature 🌡️",
                value=f"{metrics['current_temp']:.1f}°C" if metrics['current_temp'] is not None else "N/A",
                delta=f"{metrics['today_high'] - metrics['current_temp']:.1f}°C to high" if metrics['today_high'] and metrics['current_temp'] else None
            )
        with col2:
            st.metric(
                label="Condition ☁️",
                value=metrics['condition'] if metrics['condition'] else "N/A"
            )
        with col3:
            st.metric(
                label="Wind Speed 💨",
                value=f"{metrics['wind_speed']:.1f} km/h" if metrics['wind_speed'] is not None else "N/A"
            )
        with col4:
            st.metric(
                label="Wind Direction 🧭",
                value=f"{metrics['wind_direction']}°" if metrics['wind_direction'] is not None else "N/A"
            )

        # Precipitation and Map
        st.subheader("🌧️ Precipitation and Location")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric(
                label="Daily Precipitation ☔",
                value=f"{metrics['precipitation']:.1f} mm" if metrics['precipitation'] is not None else "N/A"
            )
        with col2:
            try:
                fmap = folium.Map(
                    location=[st.session_state.coordinates['lat'], st.session_state.coordinates['lon']],
                    zoom_start=12,
                    tiles="OpenStreetMap"
                )
                popup_text = f"{metrics['condition']} at {metrics['current_temp']}°C" if metrics['condition'] and metrics['current_temp'] is not None else "No weather data"
                folium.Marker(
                    [st.session_state.coordinates['lat'], st.session_state.coordinates['lon']],
                    tooltip=st.session_state.city,
                    popup=f"Weather: {popup_text}"
                ).add_to(fmap)
                st_folium(fmap, use_container_width=True)
            except Exception as e:
                st.error(f"⚠️ Failed to render map: {e}")

        # Temperature Chart
        st.subheader("🌡️ Hourly Temperature Forecast")
        if metrics['hourly_data']:
            chart_config = {
                "type": "line",
                "data": {
                    "labels": [entry['time'] for entry in metrics['hourly_data']],
                    "datasets": [{
                        "label": "Temperature (°C)",
                        "data": [entry['temperature'] for entry in metrics['hourly_data']],
                        "borderColor": "#3b82f6",
                        "backgroundColor": "#3b82f6",
                        "fill": False,
                        "tension": 0.1
                    }]
                },
                "options": {
                    "scales": {
                        "y": {
                            "title": {"display": True, "text": "Temperature (°C)"}
                        },
                        "x": {
                            "title": {"display": True, "text": "Time"}
                        }
                    }
                }
            }
            st.markdown("```chartjs\n" + json.dumps(chart_config) + "\n```")
        else:
            st.warning("Insufficient data for temperature chart.")

        # Recommendations
        st.subheader("🛠️ Recommendations")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🏞️ Activities**")
            st.info(summarize_text(data["activities"]))
        with col2:
            st.markdown("**🍽️ Dining**")
            st.success(summarize_text(data["dining_recommendations"]))
        with col3:
            st.markdown("**🏃 Fitness**")
            st.warning(summarize_text(data["fitness_options"]))

        # Additional Insights
        st.subheader("ℹ️ Additional Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**❤️ Health Advice**")
            st.markdown(summarize_text(data["health_advice"]))
        with col2:
            st.markdown("**🧭 Local Insights**")
            st.markdown(summarize_text(data["local_insights"]))

        # Animation
        rain(emoji="☔" if "rain" in metrics['condition'].lower() else "🌤️", font_size=54, falling_speed=5, animation_length="infinite")
    else:
        st.title("🌍 Global Weather Explorer")
        st.markdown("Enter a city or country in the sidebar to get started.")

# Map Page (Simplified Dashboard)
elif selected == "Map":
    st.title(f"🗺️ Weather Dashboard for {st.session_state.city}")

    # Validate coordinates
    if not st.session_state.coordinates or not isinstance(st.session_state.coordinates, dict) or 'lat' not in st.session_state.coordinates or 'lon' not in st.session_state.coordinates:
        st.error("⚠️ Invalid coordinates. Using default location (Amsterdam).")
        st.session_state.coordinates = {'lat': 52.366, 'lon': 4.901}

    # Dashboard Metrics
    st.subheader("📊 Weather at a Glance")
    metrics = parse_weather_data(st.session_state.weather_data)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Temperature 🌡️",
            value=f"{metrics['current_temp']:.1f}°C" if metrics['current_temp'] is not None else "N/A",
            delta=f"{metrics['today_high'] - metrics['current_temp']:.1f}°C to high" if metrics['today_high'] and metrics['current_temp'] else None
        )
    with col2:
        st.metric(
            label="Condition ☁️",
            value=metrics['condition'] if metrics['condition'] else "N/A"
        )
    with col3:
        st.metric(
            label="Wind Speed 💨",
            value=f"{metrics['wind_speed']:.1f} km/h" if metrics['wind_speed'] is not None else "N/A"
        )
    with col4:
        st.metric(
            label="Daily Precipitation ☔",
            value=f"{metrics['precipitation']:.1f} mm" if metrics['precipitation'] is not None else "N/A"
        )

    # Map Section
    st.subheader("📍 Location")
    try:
        fmap = folium.Map(
            location=[st.session_state.coordinates['lat'], st.session_state.coordinates['lon']],
            zoom_start=12,
            tiles="OpenStreetMap"
        )
        popup_text = f"{metrics['condition']} at {metrics['current_temp']}°C" if metrics['condition'] and metrics['current_temp'] is not None else "No weather data"
        folium.Marker(
            [st.session_state.coordinates['lat'], st.session_state.coordinates['lon']],
            tooltip=st.session_state.city,
            popup=f"Weather: {popup_text}"
        ).add_to(fmap)
        st_folium(fmap, use_container_width=True)
    except Exception as e:
        st.error(f"⚠️ Failed to render map: {e}")

# Chart Page
elif selected == "Chart":
    st.title("📈 Weather Forecast Chart")
    if st.session_state.weather_data:
        metrics = parse_weather_data(st.session_state.weather_data)
        if metrics['hourly_data']:
            chart_config = {
                "type": "line",
                "data": {
                    "labels": [entry['time'] for entry in metrics['hourly_data']],
                    "datasets": [
                        {
                            "label": "Temperature (°C)",
                            "data": [entry['temperature'] for entry in metrics['hourly_data']],
                            "borderColor": "#3b82f6",
                            "backgroundColor": "#3b82f6",
                            "fill": False,
                            "tension": 0.1
                        },
                        {
                            "label": "Precipitation (mm)",
                            "data": [entry['precipitation'] for entry in metrics['hourly_data']],
                            "borderColor": "#10b981",
                            "backgroundColor": "#10b981",
                            "fill": False,
                            "tension": 0.1
                        }
                    ]
                },
                "options": {
                    "scales": {
                        "y": {
                            "title": {"display": True, "text": "Value"}
                        },
                        "x": {
                            "title": {"display": True, "text": "Time"}
                        }
                    }
                }
            }
            st.markdown("```chartjs\n" + json.dumps(chart_config) + "\n```")
        else:
            st.warning("Insufficient data for chart.")
    else:
        st.warning("No weather data available. Please fetch weather data from the Weather page.")
