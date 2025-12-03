import os
import unittest

import dotenv

import process_street

dotenv.load_dotenv("../.local/.env")
PRST_API_KEY = os.getenv("PRST_API_KEY")


class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = process_street.ProcessStreetClient(PRST_API_KEY)

    def test_api_key(self) -> None:
        self.assertEqual(self.client.api_key, PRST_API_KEY)

    def test_get_data_sets(self) -> None:
        response = self.client.get_data_sets()
        self.assertIn("dataSets", response)

    def test_get_test_auth(self) -> None:
        response = self.client.get_test_auth()
        self.assertIn("apiKeyLabel", response)
