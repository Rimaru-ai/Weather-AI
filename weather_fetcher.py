import requests
import csv

# Replace with your OpenWeatherMap API key
API_KEY = "8ff5709c094c9427d62769911dac84a5"

# List of cities you want to track
CITIES = ["Delhi", "Mumbai", "Kolkata", "Chennai"]

def fetch_forecast(city):
    """Fetch 5-day / 3-hour forecast data for a city."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "list" not in data:
        print(f"❌ Error fetching data for {city}: {data.get('message', 'Unknown error')}")
        return []

    forecasts = []
    for item in data["list"]:  # Each entry = 3-hour forecast
        forecasts.append({
            "city": city,
            "datetime": item["dt_txt"],
            "temp": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "desc": item["weather"][0]["description"]
        })
    return forecasts

def save_to_csv(data, filename="weather.csv"):
    """Save forecast data to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["city", "datetime", "temp", "humidity", "desc"])
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    all_data = []
    for city in CITIES:
        all_data.extend(fetch_forecast(city))

    if all_data:
        save_to_csv(all_data)
        print("✅ Forecast data saved to weather.csv")
    else:
        print("⚠️ No data fetched.")
