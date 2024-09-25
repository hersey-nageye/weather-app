from flask import Flask
import weather_service
app = Flask(__name__)

# Test API Route:
@app.route("/")
def index():
    return "Hello World!"

@app.route("/weather/<city>")
def detailed_weather(city):
    # First, we retrieve lat and lon figures from the 'get_coordinates' function:
    lat,lon = weather_service.get_coordinates(city)

    # Next, we use the lat and lon figures to call OpenWeather's API for Current Weather.
    detailed_weather_data = weather_service.get_weather(lat, lon)

    # Returning specific data:
    city = detailed_weather_data["name"]
    country = detailed_weather_data["sys"]["country"]
    temp = detailed_weather_data["main"]["temp"]
    feels_like = detailed_weather_data["main"]["feels_like"]
    humidity = detailed_weather_data["main"]["humidity"]
    weather_description = detailed_weather_data["weather"][0]["description"]

    return {
        "city": city,
        "country": country,
        "weather_description": weather_description,
        "temperatures": {
            "temperature": temp,
            "humidity": humidity,
            "feels_like": feels_like
        }
    }


if __name__ == '__main__':
    app.run(debug=True)