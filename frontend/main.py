from flask import Flask, render_template

app = Flask(__name__)
version="2.0.1"
app_name = "NewLife 2.0"

@app.route('/')
def home():
    configs = {"version": version, "title":"Home", "app_name": app_name}
    return render_template('index.html',configs=configs)

@app.route('/diario')
def diario_dashboard():
    configs = {"version": version, "title":"Diario", "app_name": app_name}
    return render_template('diario/index.html',configs=configs)
    
 
if __name__ == "__main__":
    try:
        app.run(debug=True,host="0.0.0.0",port="5000")
    except Exception as e:
        print(e)