import requests
import psycopg2
from dotenv import load_dotenv
import os

#load dari env
load_dotenv()

# konfig
API_KEY = os.getenv('API_KEY')
CITY = os.getenv('CITY')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_SCHEMA = os.getenv('DB_SCHEMA')

# ambil dari Url api
def get_cuaca_api(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    return response.json()

#Simpan ke database
def Save_To_DB(data):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    
    #Buat Tabelnya kalo belum ada
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.cuaca (id SERIAL PRIMARY KEY,
            city VARCHAR(50),
            temperature REAL,
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP) """ )
    
    city = data["location"]["name"]
    temperature = data["current"]["temp_c"]
    description = data["current"]["condition"]["text"]
    
    #masukan ke table
    cur.execute(f"""
        INSERT INTO {DB_SCHEMA}.cuaca (city, temperature, description)
        VALUES (%s, %s, %s)""", (city, temperature, description))
    
    conn.commit()
    cur.close()
    conn.close()
    
#eksekusi
if __name__ == "__main__":
    cuaca_data = get_cuaca_api(CITY)
    Save_To_DB(cuaca_data)
    

    