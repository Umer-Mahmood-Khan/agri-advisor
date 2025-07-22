# src/mycrewaiproject/app.py

import streamlit as st  # type: ignore
import os
import sys
from dotenv import load_dotenv

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from mycrewaiproject.crew import create_crew
from mycrewaiproject.tools.weather_tool import OpenWeatherMapTool  # ✅ Directly use tool

# Load environment variables
load_dotenv()


# Function to fetch structured weather data
def fetch_weather_data(latitude: float, longitude: float) -> dict:
    weather_tool = OpenWeatherMapTool()
    return weather_tool._run(latitude=latitude, longitude=longitude)


# Function to generate the weather report using CrewAI
def generate_weather_report(crop_type: str, weather_data: dict) -> str:
    crew = create_crew()
    result = crew.kickoff(inputs={
        "crop_type": crop_type,
        "weather_data": str(weather_data)  # Pass weather data as string summary
    })
    return result


# ===========================
# STREAMLIT DASHBOARD UI
# ===========================

st.set_page_config(page_title="AI-powered Agricultural Advisor", page_icon="🌾")

st.title("🌾 AI-powered Agricultural Advisor")
st.subheader("Get AI-powered farming insights based on real-time weather & soil data.")

# Crop Type Selection
crop_type = st.selectbox(
    "Select your crop type:",
    options=["cotton", "wheat", "maize", "rice", "other"]
)

if crop_type == "other":
    crop_type = st.text_input("Enter your custom crop type:")

if st.button("🔍 Generate Weather Report"):
    if not crop_type.strip():
        st.warning("Please select or enter a crop type.")
    else:
        with st.spinner("Fetching weather data and generating report..."):
            try:
                # Step 1: Fetch real-time weather data
                weather_data = fetch_weather_data(
                    latitude=33.6996,
                    longitude=73.0362
                )

                st.subheader("🌦️ Current Weather Conditions")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("🌡️ Temperature", f"{weather_data['temperature']} °C")
                    st.metric("💧 Humidity", f"{weather_data['humidity']} %")
                with col2:
                    st.metric("💨 Windspeed", f"{weather_data['windspeed']} m/s")
                    st.metric("🌧️ Rainfall", f"{weather_data['rainfall']} mm")

                # Step 2: Generate AI-based advisory report
                report = generate_weather_report(crop_type, weather_data)

                st.success("✅ Weather report generated successfully!")

                st.subheader("📄 AI-Generated Weather Report")
                st.markdown(report)

                st.download_button(
                    label="📥 Download Full Report",
                    data=report,
                    file_name=f"{crop_type.lower()}_weather_report.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
