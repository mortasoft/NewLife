from flask import Flask, render_template, jsonify, redirect, request
import utils as app_utils

app = Flask(__name__)
version="2.0.1"
app_name = "NewLife 2.0"

CONFIG = app_utils.load_env_vars()

@app.route('/')
def home():
    configs = {"version": version, "title":"Home", "app_name": app_name}
    return render_template('index.html',configs=configs)


@app.route('/metas')
def metas():
    # Hago llamado al API de las Metas para obtener todas las metas
    # y las metas por cumplir
    data = app_utils.get_request(CONFIG.API_URL + "/goal")
    type(data)
    print(data)
    configs = {"version": version, "title":"Metas", "app_name": app_name, "data": data}
    return render_template('metas/metas.html',configs=configs)

@app.route('/metas/crear', methods=['POST'])
def metas_create():
    # Hago llamado al API de las Metas para crear una nueva meta
    data = request.form
    data = app_utils.post_request(CONFIG.API_URL + "/goal", CONFIG.API_DATA)
    return jsonify(data)


@app.route('/diario')
def diario_dashboard():
    configs = {"version": version, "title":"Diario", "app_name": app_name}
    return render_template('diario/dashboard.html',configs=configs)
    
 
if __name__ == "__main__":
    try:
        app.run(debug=True,host="0.0.0.0",port="5000")
    except Exception as e:
        print(e)