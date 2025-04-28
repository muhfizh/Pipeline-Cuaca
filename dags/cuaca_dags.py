from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2
import os
from dotenv import load_dotenv

# Load .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Konfigurasi variabel dari environment
API_KEY = os.getenv('API_KEY')
CITY = os.getenv('CITY')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_SCHEMA = os.getenv('DB_SCHEMA')

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def get_cuaca_api():
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def save_to_db(**context):
    data = context['ti'].xcom_pull(task_ids='get_cuaca')
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.cuaca (
            id SERIAL PRIMARY KEY,
            city VARCHAR(50),
            temperature REAL,
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    city = data["location"]["name"]
    temperature = data["current"]["temp_c"]
    description = data["current"]["condition"]["text"]

    cur.execute(f"""
        INSERT INTO {DB_SCHEMA}.cuaca (city, temperature, description)
        VALUES (%s, %s, %s)
    """, (city, temperature, description))

    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id='dag_get_api_cuaca',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['cuaca', 'api', 'postgres']
) as dag:

    get_cuaca = PythonOperator(
        task_id='get_cuaca',
        python_callable=get_cuaca_api
    )

    save_data = PythonOperator(
        task_id='save_to_db',
        python_callable=save_to_db,
        provide_context=True
    )

    get_cuaca >> save_data
