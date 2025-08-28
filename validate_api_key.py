import os
import requests

# --------------------------
# Config
# --------------------------
LOGS_DIR = "data/logs"
os.makedirs(LOGS_DIR, exist_ok=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Read from environment


def validate_key(api_key: str) -> bool:
    """Validate the OpenWeatherMap API key using a sample API request."""
    if not api_key:
        print("❌ No API key provided. Please set OPENWEATHER_API_KEY.")
        return False

    url = f"http://api.openweathermap.org/data/2.5/forecast?q=Delhi&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        print("✅ API key is valid! You can fetch weather data.")
        return True
    else:
        print(f"❌ Invalid API key or not active yet. (Status: {response.status_code})")
        print("Response:", response.json())
        return False


def save_validation_result(is_valid: bool):
    """Save the validation result to a log file."""
    result_file = os.path.join(LOGS_DIR, "weather_api_key_validation.txt")
    with open(result_file, "w") as f:
        if is_valid:
            f.write("✅ OpenWeatherMap API Key validation successful.\n")
        else:
            f.write("❌ OpenWeatherMap API Key is missing or invalid.\n")
    print(f"Validation result saved at {result_file}")


if __name__ == "__main__":
    is_valid = validate_key(API_KEY)
    save_validation_result(is_valid)
