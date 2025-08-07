import streamlit as st
import requests
import pandas as pd
import altair as alt
from streamlit_extras.let_it_rain import rain

st.set_page_config(layout="wide", page_title="Global Weather Insights 🌍")

# ---------------- Sidebar ---------------- #
st.sidebar.header("🌤️ Weather Query")
city = st.sidebar.text_input("Enter a city or country", value="Amsterdam")
submit = st.sidebar.button("Get Weather")

# ---------------- Helper Functions ---------------- #
def fetch_weather(city):
    query = f"What is the weather in {city}?"
    try:
        url = f"http://localhost:3000/api/v1/weather?q={query}"
        res = requests.post(url)
        if res.status_code == 200 and res.json().get("success"):
            return res.json()["response"]["data"][0]
        else:
            st.error("⚠️ No data returned from API.")
            return None
    except Exception as e:
        st.error(f"🚫 Failed to fetch weather data: {e}")
        return None

# ---------------- Main Display ---------------- #
if submit:
    data = fetch_weather(city)
    if data:
        st.title(f"📍 Weather Insights for {city}")
        st.markdown(f"**{data['weather']}**")

        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🏞️ Activities")
            st.info(data["activities"])

        with col2:
            st.subheader("🍽️ Dining")
            st.success(data["dining_recommendations"])

        with col3:
            st.subheader("🏃 Fitness")
            st.warning(data["fitness_options"])

        st.markdown("---")
        st.subheader("❤️ Health Advice")
        st.markdown(data["health_advice"])

        st.subheader("📊 Historical Weather Trends")
        st.markdown(data["historical_averages"])

        st.subheader("🧭 Local Insights")
        st.markdown(data["local_insights"])

        st.subheader("🧳 Tourism Highlights")
        st.markdown(data["tourism_insights"])

        st.subheader("🚉 Travel Tips")
        st.markdown(data["travel_tips"])

        st.subheader("🔌 Utilities Advice")
        st.markdown(data["utilities_info"])

        rain(emoji="❄️" if "snow" in data["weather"].lower() else "💧", font_size=54, falling_speed=5, animation_length="infinite")

        # Optional: Add mock temp chart if you have time data
        st.markdown("---")
        st.subheader("📈 Simulated Hourly Temperature")
        temp_data = pd.DataFrame({
            "Hour": list(range(0, 24)),
            "Temperature (°C)": [round(-0.4 + (i / 24) * 2.4, 2) for i in range(24)]
        })
        chart = alt.Chart(temp_data).mark_line(point=True).encode(
            x="Hour",
            y="Temperature (°C)",
            tooltip=["Hour", "Temperature (°C)"]
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
else:
    st.title("🌍 Global Weather Explorer")
    st.markdown("Enter a city or country in the sidebar to get started.")

