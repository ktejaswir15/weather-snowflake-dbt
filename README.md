# Weather Data Pipeline - Snowflake + dbt

End-to-end ELT pipeline that loads live weather data into Snowflake and transforms it with dbt.

## What it does

- Extracts weather data from the Open-Meteo API
- Loads raw records into Snowflake, authenticated via RSA key-pair (secure, password-free access)
- Transforms data through dbt staging and mart layers, including feature engineering (temperature categorization, comfort index, wind classification)
- Automated daily execution via Python scheduler with retry logic

## Tech stack

Python, Snowflake, dbt, Open-Meteo API, RSA key-pair authentication

## How to run

```
python generate_key.py
python extract.py
dbt run
python scheduler.py
```

## Files

| File | Description |
|---|---|
| generate_key.py | Generates RSA key pair for Snowflake auth |
| extract.py | Extracts weather data and loads raw records into Snowflake |
| weather_dbt/ | dbt project: staging and mart models |
| scheduler.py | Automates daily pipeline runs with retry logic |
