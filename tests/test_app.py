import unittest
from app import app
from unittest.mock import patch

class TestWeatherApp(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('weather_service.get_weather')
    @patch('weather_service.get_coordinates')
    def test_detailed_weather(self, mock_get_coordinates, mock_get_weather):
        # Mock the coordinates and weather data
        mock_get_coordinates.return_value = ("40.7128", "-74.0060")
        mock_get_weather.return_value = {
            "name": "Mogadishu",
            "sys": {"country": "SO"},
            "main": {
                "temp": 79.86,
                "feels_like": 79.86,
                "humidity": 79
            },
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 13.42}
        }

        # Simulate a GET request to the /weather/<city> route
        response = self.app.get('/weather/Mogadishu?units=imperial')

        # Assert the status code and content type
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        # Parse the JSON response
        data = response.get_json()

        # Assert the data in the response
        self.assertEqual(data['city'], "Mogadishu")
        self.assertEqual(data['temperatures']['temperature'], 79.86)
        self.assertEqual(data['weather_description'], "clear sky")

    # Test for the index route
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html>', response.data)  # Ensure HTML is in the response
        self.assertIn(b'<title>Weather App</title>', response.data)  # Example content check

if __name__ == '__main__':
    unittest.main()
