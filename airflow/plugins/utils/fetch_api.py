import requests
import pandas as pd

def data_collection_api(LIMIT, INTERVAL, SYMBOL):
    response = requests.get(
        "https://api.binance.com/api/v3/klines",
        params={"symbol": SYMBOL, "interval": INTERVAL, "limit": LIMIT},
    )
    data = response.json()

    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ]

    df = pd.DataFrame(data, columns=columns)
    numeric_cols = [
        "open", "high", "low", "close", "volume",
        "quote_asset_volume", "taker_buy_base_volume",
        "taker_buy_quote_volume"
    ]
    df[numeric_cols] = df[numeric_cols].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    return df
