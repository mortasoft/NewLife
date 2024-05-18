from flask import redirect
from apiflask import APIFlask
import os
from markupsafe import escape
import utils as app_utils
from dotenv import load_dotenv
load_dotenv()

BASE_DIRECTORY = os.path.dirname(__file__)
CONFIG = app_utils.read_config_file(BASE_DIRECTORY)

# API VERSION 
version = CONFIG.get("version")

app = APIFlask(__name__, title="Mortasoft.xyz API" , version=version)

# BASE URL 
url_base = CONFIG.get("url_base") 

app.config['DOCS_FAVICON'] = CONFIG.get("favicon")
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

# openapi.info.description
app.config['DESCRIPTION'] = CONFIG.get("descripcion_api")
app.config['SERVERS'] = CONFIG.get("servers")

@app.route("/" )
@app.doc(hide=True)
def home():
    return redirect("/docs", code=302)


from lifeapp.endpoints import configure_endpoints; configure_endpoints(app)



app.run(debug=True,host='0.0.0.0',port=os.getenv('API_PORT'))


# https://github.com/apiflask/apiflask/blob/main/examples/basic/app.py
# https://apiflask.com/en/stable/quickstart/
