# src/your_project/tools/weather_tool.py

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests
from dotenv import load_dotenv

# Load environment variables (for API key)
load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")


class WeatherToolInput(BaseModel):
    """Input schema for WeatherTool."""
    latitude: float = Field(..., description="Latitude of the location.")
    longitude: float = Field(..., description="Longitude of the location.")


class OpenWeatherMapTool(BaseTool):
    name: str = "OpenWeatherMapTool"
    description: str = (
        "Fetches current weather data (temperature, humidity, rainfall, windspeed) "
        "for the given latitude and longitude using OpenWeatherMap API."
    )
    args_schema: Type[BaseModel] = WeatherToolInput

    def _run(self, latitude: float, longitude: float) -> str:
        """Actual execution logic of the tool."""
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={latitude}&lon={longitude}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            windspeed = data['wind']['speed']
            rainfall = data.get('rain', {}).get('1h', 0)

            return {
                    "latitude": latitude,
                    "longitude": longitude,
                    "temperature": temperature,
                    "humidity": humidity,
                    "windspeed": windspeed,
                    "rainfall": rainfall
            }

        except Exception as e:
            return f"Error fetching weather data: {str(e)}"
