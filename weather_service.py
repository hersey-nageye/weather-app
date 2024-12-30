# Import required libraries
import requests 
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('venv/.env')
geo_api_key = os.getenv('GEO_API_KEY')

# Validate city name
def validate_city_name(city):
    if not isinstance(city, str):
        raise ValueError("City name must be a string.")
    if city.isdigit(): 
        raise ValueError("City name cannot be a number.")
    if city.strip() == "":
        raise ValueError("City name cannot be blank.")
    return city

# Get latitude and longitude from city name
def get_coordinates(city):
    try:
        # Send request to OpenWeather's Geocoding API
        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=2&appid={geo_api_key}'
        )
        
        if response.status_code == 200:
            data = response.json()

            if data:
                # Extract lat/lon if data is available
                lat = str(data[0]['lat'])
                lon = str(data[0]['lon'])
                return lat, lon
            else:
                raise Exception(f'{city} not found')
            
    # Handle errors
    except ValueError as ve:
        return {"error": str(ve)}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error."}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}     

# Get weather data from lat/lon
def get_weather(lat, lon, units):
    onecall_url = f'https://api.openweathermap.org/data/2.5/weather?units={units}&lat={lat}&lon={lon}&appid={geo_api_key}'

    try:
        # Send request to OpenWeather's Weather API
        response = requests.get(onecall_url)

        if response.status_code == 200:
            return response.json()  # Return weather data
        else:
            return {"error": f"Failed to get data. Status code: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {e}"}
