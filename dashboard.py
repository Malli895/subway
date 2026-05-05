import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from datetime import datetime, timedelta

st.set_page_config(page_title="Subway Ridership Predictor", layout="wide")

with open('dashboard.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        url = 'https://raw.githubusercontent.com/Malli895/subway/main/data/raw/subway_ridership.csv'
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_model():
    try:
        url = 'https://raw.githubusercontent.com/Malli895/subway/main/models/best_ridership_model.pkl'
        import requests
        response = requests.get(url)
        from io import BytesIO
        return joblib.load(BytesIO(response.content))
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

df = load_data()
model = load_model()

if df.empty or model is None:
    st.error("Failed to load required data or model. Please check the files.")
    st.stop()

st.title("🛤️ Subway Ridership Prediction Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Historical Trends")
    fig_trend = px.line(df, x='date', y='ridership', title='Daily Ridership')
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("📊 Weekly Patterns")
    fig_week = px.box(df, x='dayofweek', y='ridership', title='Ridership by Day of Week')
    st.plotly_chart(fig_week, use_container_width=True)

# Prediction Section
tab1, tab2 = st.tabs(["🔮 Single Prediction", "📅 Date Range Prediction"])

with tab1:
    date_input = st.date_input("Select Date", value=datetime.now().date() + timedelta(days=1))
    dayofweek = date_input.strftime('%A')
    month = date_input.month
    is_weekend = date_input.weekday() >= 5
    is_peak_season = month in [6,7,8]

    lag_7 = df['ridership'].tail(7).mean()
    rolling_mean_7 = lag_7
    day_mapping = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}
    day_encoded = day_mapping[dayofweek]
    input_features = np.array([[day_encoded, month, is_weekend, is_peak_season, lag_7, rolling_mean_7]])
    prediction = model.predict(input_features)[0]
    st.metric("Predicted Ridership", f"{prediction:.0f}")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        from_date = st.date_input("From Date", value=datetime.now().date())
    with col2:
        to_date = st.date_input("To Date", value=datetime.now().date() + timedelta(days=30))
    
    if st.button("Generate Range Predictions"):
        if from_date > to_date:
            st.error("From date must be before To date")
        else:
            predictions = []
            current_lag = df['ridership'].tail(7).mean()
            current_rolling = current_lag
            current_date = from_date
            
            while current_date <= to_date:
                dayofweek = current_date.strftime('%A')
                month = current_date.month
                is_weekend = current_date.weekday() >= 5
                is_peak_season = month in [6,7,8]
                day_encoded = day_mapping[dayofweek]
                
                input_features = np.array([[day_encoded, month, is_weekend, is_peak_season, current_lag, current_rolling]])
                pred = model.predict(input_features)[0]
                predictions.append({'date': current_date, 'predicted_ridership': pred})
                
                # Update for next day
                current_lag = (current_lag * 6 + pred) / 7  # Rolling 7-day
                current_rolling = pred  # Simple rolling
                current_date += timedelta(days=1)
            
            pred_df = pd.DataFrame(predictions)
            st.dataframe(pred_df)
            
            # Plot
            fig_range = px.line(pred_df, x='date', y='predicted_ridership', title='Range Predictions')
            st.plotly_chart(fig_range, use_container_width=True)

st.subheader("Model Performance")
st.info("Trained on 2 years data. Best model metrics shown in README.")

st.caption("Data: Simulated NYC Subway ridership patterns.")

