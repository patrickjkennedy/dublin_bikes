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

if __name__ == '__main__':
    unittest.main(verbosity=2)
