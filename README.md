# Crypto Research Tools

Este repositorio, `crypto_research_tools`, está dedicado a proporcionar herramientas útiles para la investigación y análisis del mercado de criptomonedas. Aquí encontrarás scripts y módulos diseñados para facilitar la recopilación de datos, el análisis y más, específicamente dirigidos a entusiastas de las criptomonedas, investigadores y traders.

## Herramientas Disponibles

### Binance Market Data Downloader

- **Descripción**: Un módulo de Python para descargar datos históricos del mercado de Binance, incluidos klines (candlesticks), para cualquier símbolo de trading y intervalo de tiempo. Los datos se guardan en archivos CSV para facilitar su análisis.
- **Características Principales**:
  - Descarga de datos de mercado para cualquier símbolo disponible en Binance.
  - Soporte para múltiples intervalos de tiempo.
  - Opción para agrupar los datos por mes o año.
  - Guardado de datos en formato CSV.
- **Cómo Usar**: Consulta la sección [Uso de Binance Market Data Downloader](#uso-de-binance-market-data-downloader) más abajo.

## Requisitos Previos

Para utilizar las herramientas en este repositorio, necesitarás Python 3.6 o superior. Cada herramienta puede tener sus propias dependencias adicionales, que se detallan en sus respectivos directorios o documentación.

## Instalación

Para instalar las dependencias necesarias para las herramientas de este repositorio, ejecuta el comando apropiado de `pip install -r requirements.txt` desde el directorio de cada herramienta. Por ejemplo, para `binance_market_data_downloader`:

```bash
cd binance_market_data_downloader
pip install -r requirements.txt
```

## Uso de Binance Market Data Downloader

1. Navega al directorio `binance_market_data_downloader`.
2. Ejecuta el script con el comando `python binance_market_data_downloader.py`.
3. Sigue las instrucciones en la terminal para introducir los parámetros requeridos (símbolo de trading, intervalo de tiempo, fechas, etc.).

## Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para nuevas herramientas o mejoras en las existentes, no dudes en abrir un issue o un pull request.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

## Autores

- [@orozcodex](https://github.com/orozcodex) - Creador del proyecto y contribuidor principal.
```

Este `README.md` proporciona una visión general del propósito del repositorio, instrucciones sobre cómo utilizar las herramientas proporcionadas, cómo instalar dependencias y cómo contribuir al proyecto. Es importante personalizar cada sección según las necesidades específicas de tu proyecto y actualizarlo a medida que el repositorio crezca con más herramientas o funcionalidades.
