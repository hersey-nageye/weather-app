from flask import Flask, jsonify
import weather_service
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/weather/<city>")
def detailed_weather(city):
    # First, get the latitude and longitude for the city
    lat,lon = weather_service.get_coordinates(city)

    # Now, use the lat and lon to get detailed weather from the One Call API
    detailed_weather_data = weather_service.get_weather(lat, lon)
    
    return jsonify(detailed_weather_data)


if __name__ == '__main__':
    app.run(debug=True)