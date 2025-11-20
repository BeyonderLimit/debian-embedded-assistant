# src/weather.py
import requests
from requests.adapters import HTTPAdapter, Retry
from rich.console import Console

console = Console()

WEATHER_API = "https://api.open-meteo.com/v1/forecast"
DEFAULT_LAT = 40.7128
DEFAULT_LON = -74.0060

# ---- create a session with retries ----
session = requests.Session()
retries = Retry(total=2, backoff_factor=0.5, status_forcelist=[502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))


def get_weather(lat=DEFAULT_LAT, lon=DEFAULT_LON):
    """Get weather from Open-Meteo API."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "temperature_unit": "fahrenheit",
        "timezone": "America/New_York",  # <-- avoid slow auto-detection
    }

    try:
        response = session.get(WEATHER_API, params=params, timeout=3)
        response.raise_for_status()
        data = response.json()

        current = data.get("current_weather")
        if not current:
            return "❌ Weather data missing"

        temp = current.get("temperature")
        wind = current.get("windspeed") or current.get("wind_speed")
        code = current.get("weathercode")

        weather_codes = {
            0: "Clear", 1: "Mostly Clear", 2: "Partly Cloudy",
            3: "Overcast", 45: "Foggy", 48: "Foggy",
            51: "Light Drizzle", 53: "Drizzle", 55: "Heavy Drizzle",
            61: "Light Rain", 63: "Rain", 65: "Heavy Rain",
            71: "Light Snow", 73: "Snow", 75: "Heavy Snow",
            95: "Thunderstorm"
        }

        condition = weather_codes.get(code, "Unknown")

        return f"🌡️ {temp}°F, {condition}, Wind: {wind} mph"

    except requests.exceptions.Timeout:
        return "⚠️ Weather request timed out"
    except requests.exceptions.RequestException as e:
        return f"❌ Weather unavailable: {e}"
    except Exception as e:
        return f"❌ Error: {e}"
