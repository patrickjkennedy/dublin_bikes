from flask_app import app
import unittest

class DublinBikesUnitTests(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_stations(self):
        # Request and parse the JSON response
        response = self.app.get('/api/stations').get_json()
        self.assertEqual(len(response),113)

    def test_current_availability(self):
        response = self.app.get('/api/current_availability').get_json()
        self.assertEqual(len(response),113)

if __name__ == '__main__':
    unittest.main(verbosity=2)
