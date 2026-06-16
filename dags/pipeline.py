import requests
import pandas as pd
import sqlite3
from datetime import datetime

CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]

def extract(**kwargs):
    """Fetch weather data from wttr.in API"""
    records = []
    for city in CITIES:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        current = data['current_condition'][0]
        records.append({
            'city': city,
            'temp_c': int(current['temp_C']),
            'temp_f': int(current['temp_F']),
            'humidity': int(current['humidity']),
            'feels_like_c': int(current['FeelsLikeC']),
            'weather_desc': current['weatherDesc'][0]['value'],
            'extracted_at': datetime.now().isoformat()
        })
    
    df = pd.DataFrame(records)
    df.to_csv('/tmp/raw_weather.csv', index=False)
    print(f"Extracted {len(records)} records")

def transform(**kwargs):
    """Clean and enrich the data"""
    df = pd.read_csv('/tmp/raw_weather.csv')
    
    def categorize_temp(temp_c):
        if temp_c < 0: return 'Freezing'
        elif temp_c < 10: return 'Cold'
        elif temp_c < 20: return 'Mild'
        elif temp_c < 30: return 'Warm'
        else: return 'Hot'
    
    df['temp_category'] = df['temp_c'].apply(categorize_temp)
    df['comfort_index'] = round((df['temp_c'] * 0.7) - (df['humidity'] * 0.3), 2)
    df = df.sort_values('temp_c', ascending=False)
    df['transformed_at'] = datetime.now().isoformat()