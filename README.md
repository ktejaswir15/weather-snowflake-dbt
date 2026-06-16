# Weather Data Pipeline with Apache Airflow

An automated ETL pipeline that extracts live weather data for 5 US cities,
transforms it using Pandas, and loads it into a SQLite database —
orchestrated with Apache Airflow and containerized with Docker.

## Architecture
Extract (wttr.in API) → Transform (Pandas) → Load (SQLite DB)
Orchestrated via Apache Airflow DAG with daily scheduling and retry logic.

## Tech Stack
- Apache Airflow 2.8 (DAG orchestration, task scheduling, retries)
- Python, Pandas (transformation, feature engineering)
- SQLite (data storage)
- Docker & Docker Compose (containerization)
- REST API (wttr.in)

## How to Run
docker compose up -d
# Open http://localhost:8080 (admin/admin)
# Trigger weather_etl_pipeline DAG