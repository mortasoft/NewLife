from flask import redirect
from apiflask import APIFlask
import os,sys
from markupsafe import escape
import utils as app_utils
from dotenv import load_dotenv

# Add the parent directory to the sys.path
sys.path.append('..')

# Check if the .env file exists
if not os.path.exists('.env'):
    app_utils.print_with_format_error("The .env files does not exist. You need to create it. Exiting...")
    sys.exit()
else:
    app_utils.print_with_format("The .env file exists. Loading variables...")
    load_dotenv()
    ENVIRONMENT_TYPE = os.getenv("ENVIRONMENT_TYPE")
    API_DEBUG = os.getenv("API_DEBUG")
    API_HOST= os.getenv("API_HOST")
    API_PORT = os.getenv("API_PORT")
    API_TITLE = os.getenv("API_TITLE") 
    API_FAVICON = os.getenv("API_TITLE")
    BASE_DIRECTORY = os.path.dirname(__file__)
    CONFIG = app_utils.read_config_file(BASE_DIRECTORY)
    version = CONFIG.get("version")
    url_base = CONFIG.get("url_base")
    

# APIFlask instance
app = APIFlask(__name__, title=API_TITLE , version=version)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

# openapi.info.description
app.config['DESCRIPTION'] = CONFIG.get("descripcion_api")
#app.config['SERVERS'] = CONFIG.get("servers")

@app.route("/" )
@app.doc(hide=True)
def home():
    return redirect("/docs", code=302)

# Configure the endpoints
import hobbies.endpoints as hobbies;hobbies.configure_endpoints(app)
import health.endpoints as health;health.configure_endpoints(app)


app.run(debug=True,host=API_HOST,port=API_PORT)


# https://github.com/apiflask/apiflask/blob/main/examples/basic/app.py
# https://apiflask.com/en/stable/quickstart/
