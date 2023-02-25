from polygon import RESTClient
import pandas as pd
import numpy as np

__all__ = ["get_data", "to_dict", "p2df", "zscore_normalize", "minmax_normalize", "normalize_", "create_window"]

def get_data(api_key, ticker="TSLA", multiplier=1, timespan="day", from_="2021-01-09", to="2023-01-10", limit=5000):
    """Retrieve bar data using the polygon api, you will need an api key""" 
    # load our polygon client
    polygon_client = RESTClient(api_key=api_key)
    return polygon_client.get_aggs(ticker=ticker, multiplier=multiplier, timespan=timespan, from_=from_, to=to, limit=limit)

def to_dict(bar):
    """Convert a polygon bar to a dictionary"""
    return {"timestamp":bar.timestamp, "open": bar.open, "high": bar.high, "low": bar.low, "close": bar.close, "volume": bar.volume, "vwap": bar.vwap, "transactions": bar.transactions}

def p2df(data, convert_timestamp=True):
    """Convert a list of polygon bars to a dataframe"""
    df =  pd.DataFrame([to_dict(bar) for bar in data])
    if convert_timestamp:
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def zscore_normalize(data):
    """Apply z-score normalization to a column of data"""
    mean = np.mean(data)
    std = np.std(data)
    normalized_data = (data - mean) / std
    return normalized_data

# minmax normalize function
def minmax_normalize(data):
    """Apply minmax normalization to a column of data"""
    minimum = np.min(data)
    maximum = np.max(data)
    normalized_data = (data - minimum) / (maximum - minimum)
    return normalized_data

def normalize_(normalization_fn, df, columns=['open', 'high', 'low', 'close', 'volume', 'vwap', 'transactions']):
    """Apply a normalization function to a dataframe"""
    for column in columns: df[column] = normalization_fn(df[column])

# let's create a dataset with 4 week windows
def create_window(df, n=0, window_size=28, columns=['open', 'high', 'low', 'close', 'volume', 'vwap', 'transactions']):
    window_data = df.iloc[n:window_size+n]
    return {"data": window_data[columns].values, "target": window_data["change"].values[-1], "timestamp": window_data["timestamp"].values[-1]}