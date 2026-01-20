import requests
import pandas as pd
from time import sleep

SYMBOL = 'BTCUSDT'
INTERVAL = '1m'
LIMIT = 1000        

def data_collection_api(retries=5, delay=2):
    url = 'https://api.binance.com/api/v3/klines'
    params = {"symbol": SYMBOL, "interval": INTERVAL, "limit": LIMIT}
    
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # Raises error if status code != 200
            data = response.json()
            
            columns = [
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
            ]
            
            df = pd.DataFrame(data, columns=columns)
            
            numeric_cols = ["open", "high", "low", "close", "volume",
                            "quote_asset_volume", "taker_buy_base_volume", "taker_buy_quote_volume"]
            df[numeric_cols] = df[numeric_cols].astype(float)
            
            df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
            df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
            
            return df
        
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            sleep(delay)
    
    print("Échec de la récupération des données après plusieurs tentatives.")
    return None

df = data_collection_api()

if df is not None:
    df.to_parquet(
        "/media/rachid/d70e3dc6-74e7-4c87-96bc-e4c3689c979a/lmobrmij/Projects/BTC_Prediction_Price/ml/Data/Normal/btc_minute_data.parquet",
        engine="pyarrow",
        index=False,
        coerce_timestamps="ms",
        allow_truncated_timestamps=True
    )
    print("Fichier Parquet sauvegardé")
else:
    print("Aucun fichier sauvegardé.")
