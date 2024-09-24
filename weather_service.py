# Importing required libraries 
import requests 
import os
from dotenv import load_dotenv

load_dotenv('venv/.env')
geo_api_key = os.getenv('GEO_API_KEY')

# Function to get lon and lat from city name:
def get_coordinates(city):
    geocoding_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=2&appid={geo_api_key}'

    try:
        response = requests.get(geocoding_url)
        
        if response.status_code == 200:
            data = response.json()

            if data:
                lat = str(data[0]['lat'])
                lon = str(data[0]['lon'])
                return lat, lon
            else:
                raise Exception(f'{city} not found')
            
     # Handle specific errors like network problems, etc.
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error. Please check your network connection."}
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again later."}
    except requests.exceptions.RequestException as e:
        # Catch any other requests-related exceptions
        return {"error": f"An error occurred: {e}"}
    except Exception as e:
        # Catch any other unexpected exceptions
        return {"error": f"An unexpected error occurred: {e}"}     


# Main function to handle user input and display weather data
def get_weather(lat, lon):
    onecall_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={geo_api_key}'

    try:
        response = requests.get(onecall_url)

        if response.status_code == 200:
            full_weather_data = response.json()
            return full_weather_data
        else:
            return {"error": f"Failed to get detailed weather data. Status code: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}
    

    # Fetch coordinates:
    coordinates = get_coordinates(city)

    # Fetch weather data:
    # weather_data

    # if weather_data:

# print(get_coordinates("Dubaq"))

