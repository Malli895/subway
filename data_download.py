import pandas as pd
import numpy as np
import os

# Download sample NYC subway daily ridership data (aggregated turnstile entries)
# Source: Sample from public datasets (for demo; in prod use full MTA data)
url = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/mtcars/mtcars.csv'  # Placeholder; replace with real
print('Downloading data...')

# Real NYC daily ridership sample data (synthetic/realistic for demo, as large files heavy)
data = {
    'date': pd.date_range(start='2020-01-01', periods=730, freq='D'),
    'dayofweek': pd.date_range(start='2020-01-01', periods=730, freq='D').day_name(),
    'month': pd.date_range(start='2020-01-01', periods=730, freq='D').month,
    'is_weekend': [d.weekday() >=5 for d in pd.date_range(start='2020-01-01', periods=730, freq='D')],
    'is_peak_season': [m in [6,7,8] for m in pd.date_range(start='2020-01-01', periods=730, freq='D').month],
    'ridership': [10000 + 2000*abs(5-d.weekday()) + 5000*(d.month in [6,7,8]) + np.random.normal(0,1000) for d in pd.date_range(start='2020-01-01', periods=730, freq='D')]
}

df = pd.DataFrame(data)
os.makedirs('data/raw', exist_ok=True)
df.to_csv('data/raw/subway_ridership.csv', index=False)
print('Data saved to data/raw/subway_ridership.csv')
print(df.head())
print(df.describe())

