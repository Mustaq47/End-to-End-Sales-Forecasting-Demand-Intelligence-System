"""Data access helpers for the Superstore dashboard."""
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]


@st.cache_data
def load_data():
    df = pd.read_csv(ROOT / "data" / "train.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Week_Number"] = df["Order Date"].dt.isocalendar().week.astype("int16")
    df["Day_of_Week"] = df["Order Date"].dt.day_name()
    df["Quarter"] = df["Order Date"].dt.quarter.astype("int8")
    season_map = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring",
                  5: "Spring", 6: "Summer", 7: "Summer", 8: "Summer", 9: "Autumn",
                  10: "Autumn", 11: "Autumn"}
    df["Season"] = df["Month"].map(season_map).astype("category")
    for column in ["Category", "Sub-Category", "Region", "Segment", "Ship Mode"]:
        df[column] = df[column].astype("category")
    return df


def build_segment_ts(df, col, val):
    return df[df[col] == val].set_index("Order Date").resample("ME")["Sales"].sum()
