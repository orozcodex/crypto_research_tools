"""
Binance Market Data Downloader

Este script permite descargar datos históricos del mercado de Binance para un
símbolo y intervalo especificados por el usuario. Los datos se guardan en
archivos CSV, con la opción de agrupar por mes o año y seleccionar el formato
de fecha (Unix o humano).

Autor: @orozcodex

Funciones:
- Descarga de klines (candlesticks) de la API de Binance.
- Soporte para múltiples símbolos e intervalos.
- Guarda los datos en CSV, con opciones de agrupación y formato de fecha.
"""

import requests
import csv
from datetime import datetime, timezone
from time import sleep
import logging
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Mensajes en Español e Inglés ajustados
messages = {
    'esp': {
        'symbol_prompt': "Introduce el símbolo (ejemplo: BTCUSDT, ETHUSDT): ",
        'interval_prompt': (
            "Introduce el intervalo (ejemplos: 1m, 3m, 5m, 15m, "
            "30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M): "),
        'start_date_prompt': "Fecha de inicio (YYYY-MM-DD): ",
        'end_date_prompt': "Fecha de fin (YYYY-MM-DD): ",
        'aggregation_prompt': "¿Agrupar datos por Mes o Año? (M/A): ",
        'date_format_prompt': "Formato de fecha (Unix/humano): ",
        'language_prompt': "Idioma (esp/eng): ",
        'date_error': "Error en formato de fecha. Usa YYYY-MM-DD.",
        'data_saved': "Datos guardados para {} intervalo {} selección {}."
    },
    'eng': {
        'symbol_prompt': "Enter symbol (example: BTCUSDT, ETHUSDT): ",
        'interval_prompt': (
            "Enter interval for klines (ex: 1m, 3m, 5m, 15m, "
            "30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M): "),
        'start_date_prompt': "Start date (YYYY-MM-DD): ",
        'end_date_prompt': "End date (YYYY-MM-DD): ",
        'aggregation_prompt': "Group data by Month or Year? (M/Y): ",
        'date_format_prompt': "Date format (Unix/human): ",
        'language_prompt': "Language (esp/eng): ",
        'date_error': "Incorrect date format. Use YYYY-MM-DD.",
        'data_saved': "Market data for {} interval {} saved {}."
    }
}

# Selector de idioma
language = input("Language (esp/eng): ").lower()
lang = 'esp' if language.startswith('esp') else 'eng'
msg = messages[lang]


def timestamp(date_str):
    try:
        return int(datetime.strptime(date_str, "%Y-%m-%d")
                   .replace(tzinfo=timezone.utc).timestamp() * 1000)
    except ValueError:
        logging.error(msg['date_error'])
        exit()


def format_date(ts, format_type):
    dt_format = '%Y-%m-%d %H:%M:%S'
    if format_type == "human":
        return datetime.fromtimestamp(int(ts) / 1000, timezone.utc) \
            .strftime(dt_format)
    else:
        return str(ts)


def write_to_csv(file, data, date_format):
    writer = csv.writer(file)
    for line in data:
        market_data = [
            format_date(line[0], date_format), line[1], line[2],
            line[3], line[4], line[5], format_date(line[6], date_format),
            line[7], line[8], line[9], line[10], line[11]
        ]
        writer.writerow(market_data)


data_folder_input = input("Introduce la ruta para guardar los datos o "
                          "presiona Enter para usar el directorio actual: ")
data_folder = data_folder_input if data_folder_input else "downloaded_data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)


symbol = input(msg['symbol_prompt']).upper()
interval = input(msg['interval_prompt'])
start_date = input(msg['start_date_prompt'])
end_date = input(msg['end_date_prompt'])
aggregation = input(msg['aggregation_prompt']).upper()
date_format_choice = input(msg['date_format_prompt']).lower()

date_format = "unix" if date_format_choice == "unix" else "human"

session = requests.Session()

url = "https://api.binance.com/api/v3/klines"
start_ts = timestamp(start_date)
end_ts = timestamp(end_date)

current_period = None
file = None

try:
    while start_ts < end_ts:
        response = session.get(
            url, params={
                "symbol": symbol, "interval": interval,
                "startTime": start_ts, "limit": 1000
            })
        data = response.json()

        if not data:
            logging.info("No more data found.")
            break

        for line in data:
            date = datetime.fromtimestamp(int(line[0]) / 1000, timezone.utc)
            period_format = '%Y-%m' if aggregation == 'M' else '%Y'
            period = date.strftime(period_format)

            if period != current_period:
                if file:
                    file.close()
                filename = os.path.join(data_folder,
                                        f"{symbol}_{interval}_"
                                        f"market_data_{period}.csv")
                file = open(filename, mode='w', newline='')
                headers = [
                    "Open time", "Open", "High", "Low", "Close",
                    "Volume", "Close time", "Quote asset volume",
                    "Number of trades", "Taker buy base asset volume",
                    "Taker buy quote asset volume", "Ignore"
                ]
                csv.writer(file).writerow(headers)
                current_period = period

            write_to_csv(file, [line], date_format)

        start_ts = int(data[-1][6]) + 1
        sleep(0.5)

except requests.exceptions.RequestException as e:
    logging.error(f"Request error: {e}")

finally:
    if file:
        file.close()

logging.info(msg['data_saved'].format(symbol, interval, aggregation))
