import unittest
from unittest.mock import patch
import weather_service

class TestWeatherService(unittest.TestCase):

    def test_validate_city_name(self):
        # Valid city name
        self.assertEqual(weather_service.validate_city_name("Mogadishu"), "Mogadishu")

        # Invalid city name cases
        with self.assertRaises(ValueError):
            weather_service.validate_city_name("")  # Empty string
        with self.assertRaises(ValueError):
            weather_service.validate_city_name(123)  # Number as city name
        with self.assertRaises(ValueError):
            weather_service.validate_city_name("   ")  # Blank spaces

    @patch('weather_service.requests.get')
    def test_get_coordinates(self, mock_get):
        # Mock the API response for successful request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"lat": 2.0371, "lon": 45.3379}]

        lat, lon = weather_service.get_coordinates("Mogadishu")
        self.assertEqual(lat, "2.0371")
        self.assertEqual(lon, "45.3379")

        # Mock API response for city not found
        mock_get.return_value.json.return_value = []
        result = weather_service.get_coordinates("Unknown City")
        self.assertIn("error", result)

    @patch('weather_service.requests.get')
    def test_get_weather(self, mock_get):
        # Mock the API response for successful weather request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
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

        weather_data = weather_service.get_weather("2.0371", "45.3379", "imperial")
        self.assertEqual(weather_data["name"], "Mogadishu")
        self.assertEqual(weather_data["sys"]["country"], "SO")
        self.assertEqual(weather_data["main"]["temp"], 79.86)

        # Mock API response for failure
        mock_get.return_value.status_code = 404
        result = weather_service.get_weather("2.0371", "45.3379", "imperial")
        self.assertIn("error", result)

if __name__ == '__main__':
    unittest.main()
