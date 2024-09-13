from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/weather")
def weather_in_mogadishu():
    return {"Mogadishu": "27 degrees"}