import pandas as pd

def summarize_weather(input_file="weather.csv", output_file="weather_summary.csv"):
    # Read the CSV into pandas
    df = pd.read_csv(input_file)

    # Convert datetime column to actual datetime
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Extract just the date (not time)
    df["date"] = df["datetime"].dt.date

    # Group by city + date
    summary = df.groupby(["city", "date"]).agg(
        avg_temp=("temp", "mean"),
        min_temp=("temp", "min"),
        max_temp=("temp", "max"),
        avg_humidity=("humidity", "mean"),
        weather_desc=("desc", lambda x: x.mode()[0] if not x.mode().empty else "N/A")
    ).reset_index()

    # Round numbers for readability
    summary["avg_temp"] = summary["avg_temp"].round(1)
    summary["avg_humidity"] = summary["avg_humidity"].round(1)

    # Save summary to CSV
    summary.to_csv(output_file, index=False)

    print(f"✅ Summary saved to {output_file}")

if __name__ == "__main__":
    summarize_weather()
