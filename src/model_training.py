import pandas as pd
import numpy as np
import joblib
import os
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# Load processed data
X_train = pd.read_csv('data/processed/X_train.csv')
X_test = pd.read_csv('data/processed/X_test.csv')
y_train = np.load('data/processed/y_train.npy')
y_test = np.load('data/processed/y_test.npy')

os.makedirs('models', exist_ok=True)

# Models
models = {
    'LinearRegression': LinearRegression(),
    'DecisionTree': DecisionTreeRegressor(random_state=42),
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42)
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    results[name] = {'mae': mae, 'rmse': rmse}
    print(f'{name}: MAE={mae:.2f}, RMSE={rmse:.2f}')
    
    # Save
    joblib.dump(model, f'models/{name.lower()}_model.pkl')

# Best model
best_model_name = min(results, key=lambda k: results[k]['rmse'])
print(f'Best model: {best_model_name}')
joblib.dump(models[best_model_name], 'models/best_ridership_model.pkl')  # Alias

# Update README metrics
with open('README.md', 'r') as f:
    content = f.read()
content = content.replace('~XX', f'{results[best_model]["rmse"]:.0f}')
with open('README.md', 'w') as f:
    f.write(content)

print('Models trained and saved.')

