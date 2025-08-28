import os
import pandas as pd

# --------------------------
# Config
# --------------------------
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)


def summarize_city_weather(city: str):
    """Summarize the weather data for a given city."""
    filename = os.path.join(RAW_DIR, f"{city.lower()}_weather.csv")
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No raw weather data found for {city} at {filename}")

    df = pd.read_csv(filename)

    summary = {
        "city": city,
        "avg_temp": round(df["avg_temp"].mean(), 2),
        "min_temp": round(df["min_temp"].min(), 2),
        "max_temp": round(df["max_temp"].max(), 2),
        "avg_humidity": round(df["avg_humidity"].mean(), 2),
        "common_weather": df["weather_desc"].mode()[0] if not df["weather_desc"].mode().empty else "unknown"
    }

    return summary


def save_summary(city: str, summary: dict):
    """Save summarized weather data into processed directory."""
    filename = os.path.join(PROCESSED_DIR, f"{city.lower()}_summary.csv")
    pd.DataFrame([summary]).to_csv(filename, index=False)
    print(f"✅ Saved summary for {city} to {filename}")


if __name__ == "__main__":
    cities = ["Delhi", "Mumbai", "Chennai", "Kolkata"]

    for city in cities:
        try:
            summary = summarize_city_weather(city)
            save_summary(city, summary)
        except Exception as e:
            print(f"❌ Failed to summarize {city}: {e}")
