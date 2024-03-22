import requests
import time
import hmac
import hashlib

# Configuraciones básicas
API_URL = "https://open-api.bingx.com/openApi/swap/v1/market/historicalTrades"
API_KEY = ""  # Sustituye por tu clave API real
SECRET_KEY = ""  # Sustituye por tu clave secreta real

def generate_signature(secret_key, params):
    """Genera la firma HMAC SHA256 requerida para la autenticación."""
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def get_historical_trades(symbol, limit=100, from_id=None):
    """Obtiene trades históricos para un símbolo específico."""
    params = {
        'symbol': symbol,
        'limit': limit,
        'timestamp': int(time.time() * 1000),
    }
    if from_id:
        params['fromId'] = from_id

    signature = generate_signature(SECRET_KEY, params)
    params['signature'] = signature
    
    headers = {
        'X-BX-APIKEY': API_KEY,
    }

    response = requests.get(API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los datos: {response.status_code}, Respuesta: {response.text}")
        return None

# Ejemplo de uso
symbol = "BTC-USDT"
historical_trades = get_historical_trades(symbol, limit=500)

if historical_trades:
    print(historical_trades)
