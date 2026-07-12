"""Weekly anomaly detection with persistent results."""
from pathlib import Path
import pickle

import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest

ROOT = Path(__file__).resolve().parents[1]
CACHE_FILE = ROOT / "cache" / "anomaly_results.pkl"


@st.cache_data
def compute_anomalies(df):
    if CACHE_FILE.exists():
        with CACHE_FILE.open("rb") as handle:
            return pickle.load(handle)
    weekly_ts = df.set_index("Order Date").resample("W")["Sales"].sum()
    features = pd.DataFrame({
        "sales": weekly_ts,
        "rolling_mean": weekly_ts.rolling(4, center=True).mean(),
        "rolling_std": weekly_ts.rolling(4, center=True).std(),
        "lag_1": weekly_ts.shift(1), "lag_2": weekly_ts.shift(2),
    }).bfill().ffill()
    model = IsolationForest(n_estimators=200, contamination=0.07, random_state=42, max_samples="auto")
    iso_labels = model.fit_predict(features)
    iso_scores = model.decision_function(features)
    roll_mean = weekly_ts.rolling(8, center=True).mean()
    roll_std = weekly_ts.rolling(8, center=True).std()
    z_scores = ((weekly_ts - roll_mean) / roll_std).replace([float("inf"), float("-inf")], 0).fillna(0)
    result = {"weekly_ts": weekly_ts, "iso_labels": iso_labels, "iso_scores": iso_scores,
              "z_scores": z_scores, "z_anomaly_mask": z_scores.abs() > 2.0,
              "roll_mean": roll_mean, "roll_std": roll_std}
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_FILE.open("wb") as handle:
        pickle.dump(result, handle)
    return result
