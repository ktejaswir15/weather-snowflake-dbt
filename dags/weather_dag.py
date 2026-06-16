from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import sqlite3

CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]

def extract(**kwargs):
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
    df.to_csv('/tmp/transformed_weather.csv', index=False)
    print(f"Transformed {len(df)} records")

def load(**kwargs):
    df = pd.read_csv('/tmp/transformed_weather.csv')
    conn = sqlite3.connect('/tmp/weather.db')
    df.to_sql('weather_data', conn, if_exists='append', index=False)
    result = pd.read_sql('SELECT COUNT(*) as total FROM weather_data', conn)
    print(f"Total records in DB: {result['total'][0]}")
    conn.close()

default_args = {
    'owner': 'tejaswi',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='weather_etl_pipeline',
    default_args=default_args,
    description='Daily weather ETL pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['weather', 'etl', 'data-engineering'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract_weather_data',
        python_callable=extract,
    )
    transform_task = PythonOperator(
        task_id='transform_weather_data',
        python_callable=transform,
    )
    load_task = PythonOperator(
        task_id='load_to_database',
        python_callable=load,
    )

    extract_task >> transform_task >> load_task