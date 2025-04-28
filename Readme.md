# Pipeline Cuaca

Pipeline Cuaca is a data pipeline project that fetches weather data, processes it, and stores it in a database. This pipeline helps to monitor and analyze weather data over time. The project demonstrates how to build a simple ETL pipeline using various tools and technologies.

## Features

- Fetches weather data from a public API.
- Processes and cleans data for analysis.
- Stores processed data in a database (e.g., MySQL, PostgreSQL).
- Can be scheduled to run periodically using Airflow or task schedulers.

## Technologies Used

- **Python**: For data processing and interacting with APIs.
- **API**: Weather data is fetched from a weather API (e.g., OpenWeatherMap, WeatherStack).
- **Database**: Data is stored in a relational database (e.g., MySQL, PostgreSQL).
- **ETL**: Extract, Transform, Load (ETL) pipeline for data handling.
- **Airflow** : To schedule the pipeline to run at set intervals.

## Installation

### Prerequisites

- Python 3.x
- Database (e.g., MySQL, PostgreSQL) - Set up a database instance for storing weather data.
- Access to a weather API service (e.g., OpenWeatherMap, WeatherStack). Obtain an API key.

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/muhfizh/Pipeline-Cuaca.git
   cd Pipeline-Cuaca
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:

   - Create a new database in your preferred database service.
   - Modify the database connection settings in the script (`.env` or environment variables).

4. Configure API keys:

   - Add your API key for the weather service in the environment variables or configuration file.

5. Run the pipeline:

   ```bash
   python get_api_cuaca.py
   ```

## for run Airflow

1. go to local enviroment:

```bash
source py_env/bin/activate
```

2. run initial db airflow

```bash
airflow db init
```

3. create new user

```bash
airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email admin@domain.com
```

then input password

4. run webserver airflow

```bash
airflow webserver -p 8080
```

5. run scheduler in difference terminal

```bash
airflow scheduler
```

6. access localhost:8080 in browser

7. input username and password

8. in dags tabs check dags_id of your pipeline

## Example Output

Once the pipeline runs successfully, the weather data will be fetched and stored in your database. You can query the database to analyze the weather data, such as daily temperature averages, humidity levels, etc.

## Contributing

Feel free to fork the repository and submit pull requests with improvements, fixes, or new features. Please make sure to follow best practices for code style and documentation.
