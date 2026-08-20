import pandas as pd
import numpy as np

def load_and_clean(filepath):
    df = pd.read_csv(filepath)
    df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
    df = df.sort_values('datetime')
    df.set_index('datetime', inplace=True)
    return df

def add_time_features(df):
    df = df.copy()
    df.index = pd.to_datetime(df.index, utc=True).tz_convert('Europe/Madrid')
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['month'] = df.index.month
    df['dayofyear'] = df.index.dayofyear
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    return df

def add_lags(df):
    df = df.copy()
    df['lag_24h'] = df['value'].shift(24)
    df['lag_168h'] = df['value'].shift(168)
    return df

def mark_blackout(df, start="2025-04-28", end="2025-04-28"):
    df = df.copy()
    df['is_blackout'] = ((df.index.date >= pd.to_datetime(start).date()) &
                          (df.index.date <= pd.to_datetime(end).date())).astype(int)
    return df

def prepare_full_dataset(filepath):
    df = load_and_clean(filepath)
    df = add_time_features(df)
    df = add_lags(df)
    df = mark_blackout(df)
    df.dropna(inplace=True)
    return df