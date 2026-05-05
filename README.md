# Subway Ridership Prediction System

## 🚀 One-Command Run (Windows)
Double-click `run.bat` or run in terminal:
```
run.bat
```
This automatically:
- Creates/activates Python venv
- Installs all requirements
- Starts Streamlit dashboard
- Opens Chrome to http://localhost:8501

Works on any Windows system with Python 3.8+ installed.

## Manual Setup (if needed)
1. python -m venv venv
2. venv\Scripts\activate
3. pip install -r requirements.txt
4. streamlit run dashboard.py

## Render Deployment
This repo is ready to deploy on Render as a Python web service.

1. Push the repo to GitHub or GitLab.
2. Create a new web service on https://dashboard.render.com/
3. Use the `render.yaml` file in the repo or set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run dashboard.py --server.port $PORT --server.enableCORS false --server.headless true`

## Features
- ML models (RandomForest best) for daily ridership forecast
- Interactive dashboard with historical viz, single/date-range predictions
- Data: NYC Subway turnstile ridership (daily aggregated)

## Metrics (example)
- RMSE: 1194
- MAE: 914

