import os
import pandas as pd

# --------------------------
# Config
# --------------------------
PROCESSED_DIR = "data/processed"
REPORTS_DIR = "data/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_city_report(city: str):
    """Generate a plain-text weather report for a city."""
    filename = os.path.join(PROCESSED_DIR, f"{city.lower()}_summary.csv")

    if not os.path.exists(filename):
        raise FileNotFoundError(f"No summary data found for {city} at {filename}")

    df = pd.read_csv(filename)
    summary = df.iloc[0]  # Only one row per summary

    report = (
        f"Weather Report for {summary['city']}\n"
        f"{'-'*40}\n"
        f"Average Temperature: {summary['avg_temp']}°C\n"
        f"Minimum Temperature: {summary['min_temp']}°C\n"
        f"Maximum Temperature: {summary['max_temp']}°C\n"
        f"Average Humidity: {summary['avg_humidity']}%\n"
        f"Most Common Weather: {summary['common_weather']}\n"
    )

    return report


def save_report(city: str, report: str):
    """Save the report into reports directory."""
    filename = os.path.join(REPORTS_DIR, f"{city.lower()}_report.txt")
    with open(filename, "w") as f:
        f.write(report)
    print(f"✅ Saved report for {city} to {filename}")


if __name__ == "__main__":
    cities = ["Delhi", "Mumbai", "Chennai", "Kolkata"]

    for city in cities:
        try:
            report = generate_city_report(city)
            save_report(city, report)
        except Exception as e:
            print(f"❌ Failed to generate report for {city}: {e}")
