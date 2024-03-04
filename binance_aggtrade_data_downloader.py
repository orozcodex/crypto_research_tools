import requests
import csv
from datetime import datetime, timedelta
from pathlib import Path

def descargar_aggtrades(symbol, startTime, endTime, limit=500):
    url = "https://api.binance.com/api/v3/aggTrades"
    trades = []
    while True:
        params = {
            "symbol": symbol,
            "limit": limit,
            "startTime": startTime,
            "endTime": endTime
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            new_trades = response.json()
            if not new_trades:
                print("No se encontraron más datos, terminando la paginación.")
                break
            trades.extend(new_trades)
            last_trade_time = int(new_trades[-1]['T'])
            startTime = last_trade_time + 1
        else:
            print(f"Error en la respuesta de la API: {response.status_code}")
            break
    return trades

def guardar_en_csv(datos, directorio, nombre_archivo, modo='a'):
    Path(directorio).mkdir(parents=True, exist_ok=True)
    filepath = Path(directorio) / nombre_archivo
    with open(filepath, modo, newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        if modo == 'w':
            escritor.writerow(['ID', 'Precio', 'Cantidad', 'Primer ID Trade', 'Último ID Trade', 'Timestamp', 'Comprador Market Maker'])
        for trade in datos:
            escritor.writerow([trade['a'], trade['p'], trade['q'], trade['f'], trade['l'], datetime.fromtimestamp(trade['T']/1000).strftime('%Y-%m-%d %H:%M:%S'), trade['m']])

def pedir_periodo():
    formato_fecha = "%Y-%m-%d"
    inicio_str = input(f"Introduce la fecha de inicio (formato {formato_fecha}): ")
    fin_str = input(f"Introduce la fecha de fin (formato {formato_fecha}): ")
    inicio = datetime.strptime(inicio_str, formato_fecha)
    fin = datetime.strptime(fin_str, formato_fecha)
    return inicio, fin

def pedir_agrupacion():
    while True:
        agrupacion = input("Introduce la agrupación (dia/mes): ")
        if agrupacion in ['dia', 'mes']:
            return agrupacion
        else:
            print("Entrada no válida. Por favor, escribe 'dia' o 'mes'.")

def pedir_directorio():
    directorio = input("Introduce el directorio donde guardar el CSV (ej. C:/Users/Teo_w/Documents): ")
    return directorio

def descargar_datos_periodo(symbol, inicio, fin, periodo, directorio, nombre_archivo):
    current_start = inicio
    if periodo == 'dia':
        delta = timedelta(days=1)
    elif periodo == 'mes':
        delta = timedelta(days=30)  # Aproximación para simplificar
    
    while current_start < fin:
        current_end = min(current_start + delta, fin)
        print(f"Descargando datos desde {current_start.strftime('%Y-%m-%d')} hasta {current_end.strftime('%Y-%m-%d')}")
        datos = descargar_aggtrades(symbol, int(current_start.timestamp() * 1000), int(current_end.timestamp() * 1000))
        if datos:
            print(f"Se descargaron {len(datos)} registros.")
            guardar_en_csv(datos, directorio, nombre_archivo)
        else:
            print("No se recibieron datos.")
        current_start += delta
    print("Descarga completada.")

def main():
    symbol = "BTCUSDT"
    print(f"Descargando datos para el símbolo: {symbol}")
    inicio, fin = pedir_periodo()
    agrupacion = pedir_agrupacion()
    directorio = pedir_directorio()
    nombre_archivo = f"{symbol}_aggtrades.csv"
    # Preparar el archivo CSV para nuevos datos
    guardar_en_csv(datos=[], directorio=directorio, nombre_archivo=nombre_archivo, modo='w')  # Aquí creamos el archivo CSV vacío con el encabezado
    descargar_datos_periodo(symbol, inicio, fin, periodo=agrupacion, directorio=directorio, nombre_archivo=nombre_archivo)

if __name__ == "__main__":
    main()


working in progress