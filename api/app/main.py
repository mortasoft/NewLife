from flask import redirect
from apiflask import APIFlask
import os
import sys
from dotenv import load_dotenv

import utils as app_utils
from database import Database
from hobbies.hobbies import ActivityLog
from health.health import Weight, Nutrition
from goals.goals import Goal, Objective

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
def load_env_vars():
    """Loads environment variables from .env file."""
    if not os.path.exists('.env'):
        app_utils.print_with_format("[MAIN] The .env file does not exist. Creating...", type="error")
        if app_utils.create_env_file():
            app_utils.print_with_format("[MAIN] .env file created. Please fill it with the required variables.")
        else:
            app_utils.print_with_format("[MAIN] Error creating .env file. Exiting...", type="error")
        sys.exit()
    else:
        app_utils.print_with_format("[MAIN] The .env file exists. Loading variables...")
        load_dotenv()


# Get database configuration based on environment
def get_db_config():
    """Returns database configuration based on environment type."""
    env_type = os.getenv("ENVIRONMENT_TYPE")
    app_utils.print_with_format(f"[MAIN] Environment type: {env_type}")

    if env_type == "development":
        return {
            "DB_NAME": os.getenv("DB_HOST_DEV"),
            "DB_USER": os.getenv("DEV_DB_USER"),
            "DB_PASS": os.getenv("DEV_DB_PASS"),
            "DB_HOST": os.getenv("DEV_DB_HOST"),
            "DB_PORT": os.getenv("DEV_DB_PORT")
        }
    elif env_type == "production":
        return {
            "DB_NAME": os.getenv("DB_NAME"),
            "DB_USER": os.getenv("DB_USER"),
            "DB_PASS": os.getenv("DB_PASS"),
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_PORT": os.getenv("DB_PORT")
        }
    else:
        app_utils.print_with_format("[MAIN] Invalid environment type. Exiting...", type="error")
        sys.exit()

# --- Main execution ---
load_env_vars()

# Get API configuration
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
API_DEBUG = os.getenv("API_DEBUG")
API_TITLE = os.getenv("API_TITLE")
API_FAVICON = os.getenv("API_TITLE")  # Assuming this is intentional
BASE_DIRECTORY = os.path.dirname(__file__)
CONFIG = app_utils.read_config_file(BASE_DIRECTORY)
version = CONFIG.get("version")
url_base = CONFIG.get("url_base")

# Create Flask app instance
app = APIFlask(__name__, title=f"{API_TITLE} | {os.getenv('ENVIRONMENT_TYPE')}", version=version)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['DESCRIPTION'] = CONFIG.get("descripcion_api")
app.config['SERVERS'] = CONFIG.get("servers")

# Initialize database connection
db_config = get_db_config()
database = Database(**db_config) 
if not database.state:
    app_utils.print_with_format("[MAIN] Error connecting to the database. Exiting...", type="error")
    sys.exit()


# --- Routes ---
@app.route("/")
@app.doc(hide=True)
def home():
    return redirect("/docs", code=302)

import hobbies.endpoints as hobbies_endpoints
hobbies_endpoints.configure_endpoints(app, database=database)

import health.endpoints as health_endpoints
health_endpoints.configure_endpoints(app, database=database)

import goals.endpoints as goals_endpoints
goals_endpoints.configure_endpoints(app, database=database)

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=API_DEBUG, host=API_HOST, port=API_PORT) 