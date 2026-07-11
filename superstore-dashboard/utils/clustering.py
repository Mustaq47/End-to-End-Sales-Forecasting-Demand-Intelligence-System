"""Demand-segment clustering with persistent results."""
from pathlib import Path
import pickle

import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
CACHE_FILE = ROOT / "cache" / "cluster_results.pkl"


@st.cache_data
def compute_clusters(df):
    if CACHE_FILE.exists():
        with CACHE_FILE.open("rb") as handle:
            return pickle.load(handle)
    grouped = df.groupby("Sub-Category", observed=True)
    feat_df = pd.DataFrame({"total_sales": grouped["Sales"].sum(), "avg_order_value": grouped["Sales"].mean()})
    monthly = df.groupby(["Sub-Category", pd.Grouper(key="Order Date", freq="ME")], observed=True)["Sales"].sum()
    feat_df["volatility"] = monthly.groupby(level=0).std()
    yearly = df.groupby(["Sub-Category", "Year"], observed=True)["Sales"].sum().unstack()
    feat_df["yoy_growth_pct"] = (yearly.iloc[:, -1] - yearly.iloc[:, 0]) / yearly.iloc[:, 0] * 100
    feat_df = feat_df.dropna()
    values = StandardScaler().fit_transform(feat_df)
    candidates = range(2, min(10, len(feat_df)))
    scores = {k: silhouette_score(values, KMeans(n_clusters=k, random_state=42, n_init=20).fit_predict(values)) for k in candidates}
    optimal_k = max(scores, key=scores.get)
    clusters = KMeans(n_clusters=optimal_k, random_state=42, n_init=20).fit_predict(values)
    feat_df["Cluster"] = clusters
    medians = feat_df[["total_sales", "avg_order_value", "volatility", "yoy_growth_pct"]].median()
    labels, used = {}, set()
    for c, row in feat_df.groupby("Cluster")[["total_sales", "avg_order_value", "volatility", "yoy_growth_pct"]].mean().iterrows():
        hv, gr, vol, aov = row.total_sales > medians.total_sales, row.yoy_growth_pct > medians.yoy_growth_pct, row.volatility > medians.volatility, row.avg_order_value > medians.avg_order_value
        label = ("High Volume, Stable Growth" if hv and gr and not vol else "High Volume, High Volatility" if hv and vol else "Low Volume, Growing Demand" if not hv and gr else "Low Volume, High Volatility" if not hv and not gr and vol else "Niche, High-Value Orders" if aov and not hv else "Mature, Stable Demand" if not gr and not vol else f"Cluster {c}")
        labels[c] = f"{label} ({c})" if label in used else label; used.add(label)
    pca = PCA(n_components=2, random_state=42)
    feat_df[["PCA1", "PCA2"]] = pca.fit_transform(values)
    feat_df["Label"] = feat_df["Cluster"].map(labels)
    cluster_means = feat_df.groupby("Cluster")[["total_sales", "avg_order_value", "volatility", "yoy_growth_pct"]].mean()
    result = {"feat_df": feat_df, "cluster_means": cluster_means, "labels": labels, "pca": pca, "optimal_k": optimal_k}
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_FILE.open("wb") as handle: pickle.dump(result, handle)
    return result
