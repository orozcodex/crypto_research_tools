import requests
import csv
from datetime import datetime, timezone
import os
import logging
import time

# Configuración inicial
API_URL = "https://open-api.bingx.com/openApi/swap/v3/quote/klines"

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_FOLDER = 'downloaded_data'

def send_request(method, path, params):
    """Envía la solicitud a la API sin necesidad de autenticación."""
    url = f"{API_URL}{path}?{params}"
    response = requests.request(method, url)
    return response.json()

def parse_params(params_map):
    """Prepara y devuelve la cadena de parámetros ordenados."""
    sorted_keys = sorted(params_map)
    return "&".join(f"{key}={params_map[key]}" for key in sorted_keys)

def write_to_csv(filename, data):
    """Escribe los datos en un archivo CSV."""
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if os.stat(filename).st_size == 0:  # Si el archivo está vacío, añade los encabezados
            writer.writerow(["Open Time", "Open", "High", "Low", "Close", "Volume"])
        for line in data:
            writer.writerow([datetime.fromtimestamp(line['time']/1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), line['open'], line['high'], line['low'], line['close'], line['volume']])

def download_data(symbol, interval, start_time, end_time):
    """Descarga datos del mercado para un intervalo específico y los guarda en CSV."""
    path = '/quote/klines'
    params_map = {
        "symbol": symbol,
        "interval": interval,
        "limit": "1000",
        "startTime": str(start_time),
        "endTime": str(end_time)
    }
    
    params_str = parse_params(params_map)
    data = send_request("GET", path, params_str)

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    filename = os.path.join(DATA_FOLDER, f"{symbol}_{interval}_{start_time}_{end_time}.csv")
    
    if 'data' in data:
        write_to_csv(filename, data['data'])
        logging.info(f"Data saved to {filename}")
    else:
        logging.error("Failed to fetch data")

if __name__ == '__main__':
    symbol = input("Enter symbol (example: BTC-USDT): ")
    interval = input("Enter interval (examples: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M): ")
    start_date_str = input("Start date (YYYY-MM-DD): ")
    end_date_str = input("End date (YYYY-MM-DD): ")
    
    start_time = int(datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
    end_time = int(datetime.strptime(end_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
    
    download_data(symbol.replace('-', '_'), interval, start_time, end_time)
