import os, sys
from flask import redirect
from apiflask import APIFlask
from database import Database
import utils as app_utils
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Load environment variables (in utils.py) ---
CONFIG = app_utils.load_env_vars() 

# Create Flask app instance
app = APIFlask(
    __name__,
    title=f"{CONFIG.API_TITLE} | {CONFIG.ENVIRONMENT_TYPE}",
    version=CONFIG.VERSION
)

# --- Database configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASE_RESPONSE_SCHEMA'] = app_utils.BaseResponse
app.config['BASE_RESPONSE_DATA_KEY '] = 'data'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
engine = create_engine(CONFIG.SQLALCHEMY_DATABASE_URI)

# --- Routes ---
@app.route("/")
@app.doc(hide=True)
def home():
    return redirect("/docs", code=302)

# Import and configure endpoints
import goals.endpoints as goals_endpoints
goals_endpoints.configure_endpoints(app, engine)

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=CONFIG.API_DEBUG, host=CONFIG.API_HOST, port=CONFIG.API_PORT)
    app_utils.print_with_format(f"API running on {CONFIG.API_HOST}:{CONFIG.API_PORT}", type="info")