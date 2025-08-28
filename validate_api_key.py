import requests
MY_KEY = "9bc1ca2570772439fcfa5174d5d4e716"


API_KEY = MY_KEY  # put your key here


def validate_key(api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q=Delhi&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        print("✅ API key is valid! You can fetch weather data.")
    else:
        print(f"❌ Invalid API key or not active yet. (Status: {response.status_code})")
        print("Response:", response.json())


if __name__ == "__main__":
    validate_key(API_KEY)
