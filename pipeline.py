import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- CONFIGURATION ---
CITIES = ["New York", "Chicago", "Los Angeles", "Houston", "Phoenix"]

# --- EXTRACT ---
def extract(cities):
    print("Extracting data...")
    records = []
    for city in cities:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        data = response.json()
        current = data["current_condition"][0]
        records.append({
            "city": city,
            "temperature_f": int(current["temp_F"]),
            "feels_like_f": int(current["FeelsLikeF"]),
            "humidity": int(current["humidity"]),
            "weather": current["weatherDesc"][0]["value"],
            "wind_speed_mph": int(current["windspeedMiles"]),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return records

# --- TRANSFORM ---
def transform(records):
    print("Transforming data...")
    df = pd.DataFrame(records)
    df = df.sort_values("temperature_f", ascending=False)
    df = df.reset_index(drop=True)
    return df

# --- LOAD ---
def load(df):
    print("Loading data...")
    df.to_csv("weather_data.csv", index=False)
    print("✅ Data saved to weather_data.csv")
    print(df)

# --- VISUALIZE ---
def visualize(df):
    plt.figure(figsize=(10, 5))
    plt.bar(df["city"], df["temperature_f"], color="steelblue")
    plt.title("Current Temperature by City (°F)")
    plt.xlabel("City")
    plt.ylabel("Temperature (°F)")
    plt.tight_layout()
    plt.savefig("weather_chart.png")
    print("✅ Chart saved as weather_chart.png")
    plt.show()

# --- RUN PIPELINE ---
if __name__ == "__main__":
    raw_data = extract(CITIES)
    clean_data = transform(raw_data)
    load(clean_data)
    visualize(clean_data)
    print("🎉 Pipeline complete!")