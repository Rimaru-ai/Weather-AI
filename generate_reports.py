import pandas as pd

def generate_reports(input_file="weather_summary.csv", output_file="weather_reports.txt"):
    df = pd.read_csv(input_file)

    reports = []
    for _, row in df.iterrows():
        city = row["city"]
        date = row["date"]
        avg_temp = row["avg_temp"]
        min_temp = row["min_temp"]
        max_temp = row["max_temp"]
        avg_humidity = row["avg_humidity"]
        desc = row["weather_desc"]

        report = (
            f"📍 {city} on {date}: "
            f"average temperature {avg_temp}°C (min {min_temp}°C, max {max_temp}°C), "
            f"average humidity {avg_humidity}%. "
            f"Weather is mostly {desc}."
        )
        reports.append(report)

    # Save to a text file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(reports))

    print(f"✅ Weather reports saved to {output_file}")

if __name__ == "__main__":
    generate_reports()
