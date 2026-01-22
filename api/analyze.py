import json
import requests
from http.server import BaseHTTPRequestHandler

API_KEY = "your_api_key_here"  # Replace with your actual key
BASE_URL = "https://financialmodelingprep.com/api/v3"

# Modular criteria functions - easy to add more!
def calculate_roe(stock_data):
    """Calculate ROE from financial data"""
    try:
        return stock_data.get('roe', 0)
    except:
        return None

def calculate_rsi(stock_data):
    """Placeholder for RSI calculation"""
    # Add RSI logic here when needed
    pass

def calculate_debt_to_capital(stock_data):
    """Placeholder for Debt-to-Capital calculation"""
    # Add debt-to-capital logic here when needed
    pass

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get NASDAQ stocks
            nasdaq_url = f"{BASE_URL}/stock-screener?marketCapMoreThan=1000000000&exchange=NASDAQ&limit=100&apikey={API_KEY}"
            response = requests.get(nasdaq_url)
            stocks = response.json()
            
            # Filter and calculate ROE
            stock_data = []
            for stock in stocks[:50]:  # Limit to avoid API throttling
                symbol = stock['symbol']
                
                # Get detailed metrics
                metrics_url = f"{BASE_URL}/key-metrics/{symbol}?apikey={API_KEY}"
                metrics_response = requests.get(metrics_url)
                
                if metrics_response.status_code == 200:
                    metrics = metrics_response.json()
                    if metrics and len(metrics) > 0:
                        roe = metrics[0].get('roe')
                        if roe and roe > 0:  # Valid ROE
                            stock_data.append({
                                'symbol': symbol,
                                'name': stock.get('companyName', symbol),
                                'roe': round(roe * 100, 2),  # Convert to percentage
                                'price': stock.get('price', 0),
                                'marketCap': stock.get('marketCap', 0)
                            })
            
            # Sort by ROE (lowest first) and get top 10
            sorted_stocks = sorted(stock_data, key=lambda x: x['roe'])[:10]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(sorted_stocks).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
```

**requirements.txt:**
```
requests==2.31.0
