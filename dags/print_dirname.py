from dotenv import load_dotenv
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
new_script_dir = script_dir.replace("\dags","")

# Build the full path to the .env file in the same directory as the script
env_path = os.path.join(new_script_dir, '.env')

# Load environment variables from the .env file
load_dotenv(env_path)

# Access environment variables
database_url = os.getenv('DB_NAME')
secret_key = os.getenv('API_KEY')

print(f"Database URL: {database_url}")
print(f"Secret Key: {secret_key}")
