import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(base_dir)
import unittest
from main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    def test_home(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json, {"message": "server is up and running, go to /docs for api"})
    # def test_tax_payer_creation(self):
    #     result=self.app.get('/auth/jwt')
    #     print(result.data)
    #     self.assertEqual(result.status_code, 200)
if __name__ == "__main__":
    unittest.main()
