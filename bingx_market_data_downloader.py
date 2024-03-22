import requests
import csv
from datetime import datetime, timezone
import os
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ajustes específicos para BingX
API_URL = 'https://open-api.bingx.com/openApi/swap/v3/quote/klines'

def format_time(milliseconds, format_type='human'):
    if format_type == 'human':
        return datetime.fromtimestamp(milliseconds / 1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return str(milliseconds)

def get_market_data(symbol, interval, start_time, end_time, limit=1000):
    # Asegurarse de que el símbolo tenga el formato correcto, agregando el guion si es necesario
    formatted_symbol = symbol.upper().replace("USDT", "-USDT")
    params = {
        'symbol': formatted_symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': limit
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        logging.error(f"Error fetching data: {response.status_code} - {response.text}")
        return []

def write_to_csv(filename, data, date_format):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ["Open Time", "Open", "High", "Low", "Close", "Volume"]
        writer.writerow(headers)
        for line in data:
            writer.writerow([
                format_time(line['time'], date_format), 
                line['open'], line['high'], line['low'], 
                line['close'], line['volume']
            ])

def main():
    # Ejemplo de uso
    symbol = input("Enter symbol (example: BTC-USDT, ETH-USDT): ")  # Símbolo a consultar
    interval = input("Enter interval (examples: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M): ")  # Intervalo de los klines
    start_date_str = input("Start date (YYYY-MM-DD): ")  # Fecha de inicio en formato de fecha
    end_date_str = input("End date (YYYY-MM-DD): ")  # Fecha de fin en formato de fecha
    start_time = int(datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
    end_time = int(datetime.strptime(end_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
    data_folder = 'downloaded_data'  # Carpeta donde se guardarán los datos

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    data = get_market_data(symbol, interval, start_time, end_time)

    if data:
        filename = os.path.join(data_folder, f"{symbol}_{interval}_market_data.csv")
        write_to_csv(filename, data, 'human')
        logging.info(f"Datos guardados en {filename}")
    else:
        logging.error("No se pudieron obtener los datos.")

if __name__ == "__main__":
    main()
