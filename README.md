# Currency Exchange Rate API

A Flask-based web application and API for real-time and historical currency exchange rates, with a modern frontend and comprehensive API documentation.

## Features
- Real-time currency exchange rates
- Historical exchange rates for any date
- Currency conversion between 170+ currencies
- Fast caching for performance
- Modern, responsive frontend (Bootstrap 5)
- API documentation page

## Live Demo
You can deploy this project locally or on any cloud platform. (Replace this section with your live URL if available.)

## Getting Started

### Prerequisites
- Python 3.7+
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/currency-exchange-api.git
   cd currency-exchange-api
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Create a `.env` file and set your ExchangeRate-API key:
   ```env
   EXCHANGE_RATE_API_KEY=your_api_key_here
   ```
   If not set, a demo key is used by default.

4. Run the app:
   ```bash
   python app.py
   ```

5. Visit [http://localhost:5000](http://localhost:5000) in your browser.

## API Endpoints

### 1. Get Latest Rates
- **Endpoint:** `/api/latest`
- **Method:** GET
- **Query Params:**
  - `base` (optional, default: USD)
- **Example:** `/api/latest?base=EUR`

### 2. Get Historical Rates
- **Endpoint:** `/api/historical`
- **Method:** GET
- **Query Params:**
  - `date` (required, format: YYYY-MM-DD)
  - `base` (optional, default: USD)
- **Example:** `/api/historical?date=2023-01-01&base=GBP`

### 3. Convert Currency
- **Endpoint:** `/api/convert`
- **Method:** GET
- **Query Params:**
  - `from` (required)
  - `to` (required)
  - `amount` (optional, default: 1)
- **Example:** `/api/convert?from=USD&to=EUR&amount=100`

### 4. List Currencies
- **Endpoint:** `/api/currencies`
- **Method:** GET
- **Example:** `/api/currencies`

## Frontend
- Main page: `/`
- API documentation: `/docs`

## Running Tests
To run the test suite:
```bash
python -m unittest tests/test_api.py
```

## Project Structure
```
currency-exchange-api/
├── app.py
├── config.py
├── requirements.txt
├── static/
│   ├── css/style.css
│   └── js/script.js
├── templates/
│   ├── index.html
│   └── api_docs.html
├── tests/
│   └── test_api.py
└── cache/
```

## Credits
- Developed by **Molla Samser**
- Contact: [support@rskworld.in](mailto:support@rskworld.in)
- More projects: [RSKWORLD.IN](https://rskworld.in)

## License
This project is licensed under the MIT License.
