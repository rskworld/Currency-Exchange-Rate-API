from flask import Flask, jsonify, request, render_template
import requests
import json
import os
from datetime import datetime, timedelta
from functools import wraps
import pytz
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Ensure cache directory exists
os.makedirs(app.config['CACHE_DIR'], exist_ok=True)

def cache_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_file = os.path.join(app.config['CACHE_DIR'], f"{func.__name__}_{'_'.join(map(str, args))}_{'_'.join(map(str, kwargs.values()))}.json".replace(':', '_').replace(' ', '_'))
        if os.path.exists(cache_file):
            file_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if datetime.now() - file_time < timedelta(seconds=app.config['CACHE_TIME']):
                with open(cache_file, 'r') as f:
                    return json.load(f)
        result = func(*args, **kwargs)
        with open(cache_file, 'w') as f:
            json.dump(result, f)
        return result
    return wrapper

@cache_response
def get_latest_rates(base_currency='USD'):
    url = f"{app.config['BASE_URL']}{app.config['API_KEY']}/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {'error': 'Failed to fetch exchange rates'}

@cache_response
def get_historical_rates(date, base_currency='USD'):
    url = f"{app.config['BASE_URL']}{app.config['API_KEY']}/history/{base_currency}/{date.year}/{date.month}/{date.day}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {'error': 'Failed to fetch historical rates'}

@cache_response
def convert_currency(from_currency, to_currency, amount):
    rates = get_latest_rates(from_currency)
    if 'error' in rates or 'conversion_rates' not in rates:
        return rates
    if to_currency not in rates['conversion_rates']:
        return {'error': 'Invalid target currency'}
    rate = rates['conversion_rates'][to_currency]
    converted_amount = float(amount) * rate
    return {
        'from_currency': from_currency,
        'to_currency': to_currency,
        'amount': amount,
        'converted_amount': round(converted_amount, 4),
        'rate': rate,
        'timestamp': datetime.now(pytz.utc).isoformat()
    }

@app.route('/')
def index():
    return render_template('index.html',
                         site_name="Rskworld.in",
                         developer="Molla Samser",
                         contact_email="support@rskworld.in")

@app.route('/api/latest', methods=['GET'])
def latest_rates():
    base = request.args.get('base', 'USD')
    return jsonify(get_latest_rates(base))

@app.route('/api/historical', methods=['GET'])
def historical_rates():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date parameter is required'}), 400
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    base = request.args.get('base', 'USD')
    return jsonify(get_historical_rates(date, base))

@app.route('/api/convert', methods=['GET'])
def convert():
    from_curr = request.args.get('from')
    to_curr = request.args.get('to')
    amount = request.args.get('amount', '1')
    if not from_curr or not to_curr:
        return jsonify({'error': 'Both "from" and "to" currencies are required'}), 400
    try:
        float(amount)
    except ValueError:
        return jsonify({'error': 'Amount must be a number'}), 400
    return jsonify(convert_currency(from_curr, to_curr, amount))

@app.route('/api/currencies', methods=['GET'])
def list_currencies():
    rates = get_latest_rates()
    if 'error' in rates:
        return jsonify(rates)
    currencies = list(rates['conversion_rates'].keys())
    return jsonify({
        'currencies': currencies,
        'count': len(currencies),
        'timestamp': datetime.now(pytz.utc).isoformat()
    })

@app.route('/docs')
def api_docs():
    return render_template('api_docs.html',
                         site_name="Rskworld.in",
                         developer="Molla Samser",
                         contact_email="support@rskworld.in")

if __name__ == '__main__':
    app.run(debug=True)