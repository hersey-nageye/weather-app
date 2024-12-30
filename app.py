from flask import Flask, jsonify, render_template, request
import weather_service
app = Flask(__name__)
app.json.sort_keys = False


# Custom error handler for handling exceptions
@app.errorhandler(Exception)
def handle_validation_exception(e):
    return jsonify({"Error": f"{e}"}), 400  # Return 400 for validation errors

# Home route to serve the HTML page
@app.route("/")
def index():
    return render_template('index.html')

# Route to get detailed weather by city name
@app.route("/weather/<city>")
def detailed_weather(city):

    try:
        # Validate the city name
        valid_city = weather_service.validate_city_name(city)

        # Get units from the query parameter (default to 'imperial' if not provided)
        units = request.args.get('units', 'celsius')
        
        # Get coordinates (lat, lon) for the city
        coordinates = weather_service.get_coordinates(valid_city)

        # Return error if coordinates retrieval failed
        if isinstance(coordinates, dict) and "error" in coordinates:
            return jsonify(coordinates), 400  # Bad request
        
        # Unpack lat and lon
        lat, lon = coordinates

        # Get detailed weather using lat and lon
        detailed_weather_data = weather_service.get_weather(lat, lon, units)

        # Return specific weather details
        return {
            "city": detailed_weather_data["name"],
            "country": detailed_weather_data["sys"]["country"],
            "weather_description": detailed_weather_data["weather"][0]["description"],
            "temperatures": {
                "temperature": detailed_weather_data["main"]["temp"],
                "feels_like": detailed_weather_data["main"]["feels_like"],
            "humidity": detailed_weather_data["main"]["humidity"],
            "wind" : {
                "speed": detailed_weather_data["wind"]["speed"]
            }
            }
        }

    except ValueError as e:
        # Handle validation errors
        return handle_validation_exception(e)
    
    except Exception as e:
        # Handle other errors with 500 response
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)

