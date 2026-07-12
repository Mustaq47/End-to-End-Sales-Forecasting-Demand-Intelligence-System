"""Forecasting engines used by the explorer."""
import numpy as np
import pandas as pd
import streamlit as st
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from xgboost import XGBRegressor


def _metrics(actual, predicted):
    actual, predicted = np.asarray(actual), np.asarray(predicted)
    mask = actual != 0
    return {"MAE": float(mean_absolute_error(actual, predicted)), "RMSE": float(np.sqrt(mean_squared_error(actual, predicted))),
            "MAPE": float(np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100) if mask.any() else np.nan}


@st.cache_resource
def forecast_segment(ts, horizon):
    train, test = ts.iloc[:-horizon], ts.iloc[-horizon:]
    model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False,
                    seasonality_mode="additive", changepoint_prior_scale=0.05, seasonality_prior_scale=10)
    prophet_df = train.reset_index().rename(columns={"Date": "ds", "Sales": "y", "Order Date": "ds"})
    model.fit(prophet_df)
    holdout = model.predict(pd.DataFrame({"ds": test.index}))["yhat"].to_numpy()
    metrics = _metrics(test.to_numpy(), holdout)
    full_model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False,
                         seasonality_mode="additive", changepoint_prior_scale=0.05, seasonality_prior_scale=10)
    full_model.fit(ts.reset_index().rename(columns={"Date": "ds", "Sales": "y", "Order Date": "ds"}))
    future = full_model.make_future_dataframe(periods=horizon, freq="ME")
    forecast = full_model.predict(future)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    return {"forecast": forecast, **metrics, "test_dates": test.index, "test_pred": holdout, "test_actual": test.to_numpy()}


def sarima_forecast(ts, horizon):
    train, test = ts.iloc[:-horizon], ts.iloc[-horizon:]
    pred = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), enforce_stationarity=False, enforce_invertibility=False).fit(disp=False).forecast(horizon)
    return _metrics(test, pred)


def xgboost_forecast(ts, horizon):
    frame = pd.DataFrame({"y": ts})
    for lag in (1, 2, 3): frame[f"lag_{lag}"] = frame.y.shift(lag)
    frame["rolling_mean_3"] = frame.y.rolling(3).mean().shift(1)
    frame["month"] = frame.index.month; frame["quarter"] = frame.index.quarter
    frame["season"] = frame.index.month.map({12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3})
    frame = frame.dropna(); train, test = frame.iloc[:-horizon], frame.iloc[-horizon:]
    features = [c for c in frame if c != "y"]
    model = XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=3, subsample=0.8, colsample_bytree=0.8, random_state=42)
    model.fit(train[features], train.y)
    return _metrics(test.y, model.predict(test[features]))
