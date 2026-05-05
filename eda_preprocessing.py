import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import plotly.express as px

# Load raw data
df = pd.read_csv('data/raw/subway_ridership.csv')
df['date'] = pd.to_datetime(df['date'])
print('Raw data loaded:', df.shape)
print(df.head())

# Feature Engineering
df['year'] = df['date'].dt.year
df['quarter'] = df['date'].dt.quarter
df['is_holiday'] = 0  # Simplified
df.sort_values('date', inplace=True)
df['lag_7'] = df['ridership'].shift(7)
df['rolling_mean_7'] = df['ridership'].rolling(window=7).mean()

# Encode categoricals
le_day = LabelEncoder()
df['dayofweek_encoded'] = le_day.fit_transform(df['dayofweek'])

# Features and target
features = ['dayofweek_encoded', 'month', 'is_weekend', 'is_peak_season', 'lag_7', 'rolling_mean_7']
X = df[features].dropna()
y = df.loc[X.index, 'ridership']

# Train test split (time series aware)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Save
os.makedirs('data/processed', exist_ok=True)
X_train.to_csv('data/processed/X_train.csv', index=False)
X_test.to_csv('data/processed/X_test.csv', index=False)
np.save('data/processed/y_train.npy', y_train.values)
np.save('data/processed/y_test.npy', y_test.values)
joblib.dump(le_day, 'models/label_encoder.pkl')
os.makedirs('models', exist_ok=True)

print('Processed data saved.')
print('X_train shape:', X_train.shape)
print('Label encoder saved.')
