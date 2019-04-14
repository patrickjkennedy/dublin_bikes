from flask_app import application
import unittest

class DublinBikesUnitTests(unittest.TestCase):

    def setUp(self):
        application.testing = True
        self.application = application.test_client()

    def test_stations(self):
        # Request and parse the JSON response
        response = self.application.get('/api/stations').get_json()
        self.assertEqual(len(response),113)

    def test_current_availability(self):
        response = self.application.get('/api/current_availability').get_json()
        self.assertEqual(len(response),113)

    def test_station_occupancy_weekly(self):
        response = self.application.get('/api/station_occupancy_weekly/42').get_json()
        self.assertEqual(len(response),2)

    def test_forecast(self):
        response = self.application.get('/api/forecast').get_json()
        self.assertEqual(len(response),8)
    
    def test_user_input(self):
        response = self.application.get('/user_input?StationselectFrom=2&SelectcollectTime=18%3A20&StationselectTo=2&SelectdropTime=18%3A50').get_json()
        self.assertEqual(response['from_station'], "2")

    def test_current_weather(self):
        response = self.application.get('api/current_weather').get_json()
        self.assertEqual(len(response), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
