import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# --------------------------
# Config
# --------------------------
API_URL = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")  # Read from env variable
OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_weather(city: str, api_key: str = API_KEY):
    """Fetch 5-day / 3-hour weather forecast data for a given city."""
    if not api_key:
        raise ValueError("API key not found. Please set OPENWEATHER_API_KEY environment variable.")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()


def process_weather_data(data: dict, city: str) -> pd.DataFrame:
    """Convert raw API data into a cleaned DataFrame with daily averages."""
    records = []
    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        weather = entry["weather"][0]["description"]

        records.append({
            "city": city,
            "date": date,
            "temp": temp,
            "humidity": humidity,
            "weather": weather
        })

    df = pd.DataFrame(records)

    # Aggregate by date
    daily_summary = df.groupby(["city", "date"]).agg(
        avg_temp=("temp", "mean"),
        min_temp=("temp", "min"),
        max_temp=("temp", "max"),
        avg_humidity=("humidity", "mean"),
        weather_desc=("weather", lambda x: x.mode()[0] if not x.mode().empty else "unknown")
    ).reset_index()

    return daily_summary


def save_weather_data(df: pd.DataFrame, city: str):
    """Save weather DataFrame as CSV in data/raw/ directory."""
    filename = os.path.join(OUTPUT_DIR, f"{city.lower()}_weather.csv")
    df.to_csv(filename, index=False)
    print(f"✅ Saved weather data for {city} to {filename}")


if __name__ == "__main__":
    cities = ["Delhi", "Mumbai", "Chennai", "Kolkata"]

    for city in cities:
        try:
            raw_data = fetch_weather(city)
            df = process_weather_data(raw_data, city)
            save_weather_data(df, city)
        except Exception as e:
            print(f"❌ Failed to fetch data for {city}: {e}")
