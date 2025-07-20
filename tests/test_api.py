import unittest
from app import app
from datetime import datetime, timedelta
import json

class CurrencyExchangeApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Currency Exchange Rate API', response.data)

    def test_docs_page(self):
        response = self.app.get('/docs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'API Documentation', response.data)

    def test_latest_rates(self):
        response = self.app.get('/api/latest?base=USD')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('conversion_rates', data)
        self.assertEqual(data.get('base', 'USD'), 'USD')

    def test_historical_rates_valid(self):
        date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        response = self.app.get(f'/api/historical?date={date}&base=USD')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('conversion_rates', data)
        self.assertEqual(data.get('base', 'USD'), 'USD')

    def test_historical_rates_invalid_date(self):
        response = self.app.get('/api/historical?date=invalid-date')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_historical_rates_missing_date(self):
        response = self.app.get('/api/historical')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_convert_valid(self):
        response = self.app.get('/api/convert?from=USD&to=EUR&amount=10')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('converted_amount', data)
        self.assertEqual(data.get('from_currency'), 'USD')
        self.assertEqual(data.get('to_currency'), 'EUR')

    def test_convert_missing_params(self):
        response = self.app.get('/api/convert?from=USD')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_convert_invalid_amount(self):
        response = self.app.get('/api/convert?from=USD&to=EUR&amount=abc')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_list_currencies(self):
        response = self.app.get('/api/currencies')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('currencies', data)
        self.assertIn('count', data)

if __name__ == '__main__':
    unittest.main()