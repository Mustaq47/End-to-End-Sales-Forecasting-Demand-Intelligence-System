# Build Prompt — Superstore Sales Intelligence Dashboard (Streamlit)

Use this as a direct instruction prompt for an engineer or an AI coding assistant (Claude Code, Cursor, etc.) to build the app. Every parameter below is copied exactly from `Analysis3.ipynb` — do not substitute defaults.

---

## 1. Objective

Build a production-grade, multi-page **Streamlit** web application called **"Superstore Sales Intelligence Dashboard"** that productionizes the analysis from `Analysis3.ipynb` (Tasks 1–6: EDA, decomposition, forecasting, segment forecasting, anomaly detection, clustering). Deploy it live on **Streamlit Community Cloud**.

## 2. Data Source

- File: `train.csv` (Kaggle "Superstore Sales" dataset, `rohitsahoo/sales-forecasting`), 9,800 rows × 18 columns.
- Columns: `Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales`
- Date format: `Order Date` / `Ship Date` are `DD/MM/YYYY` → parse with `pd.to_datetime(..., dayfirst=True)`.
- Derived columns to recreate on load: `Year`, `Month`, `Week_Number` (`.dt.isocalendar().week`), `Day_of_Week`, `Quarter`, `Season` (Winter=Dec/Jan/Feb, Spring=Mar/Apr/May, Summer=Jun/Jul/Aug, Autumn=Sep/Oct/Nov).

## 3. Architecture

```
project/
├── app.py                      # Home/landing page
├── pages/
│   ├── 1_Sales_Overview.py
│   ├── 2_Forecast_Explorer.py
│   ├── 3_Anomaly_Report.py
│   └── 4_Product_Demand_Segments.py
├── utils/
│   ├── data_loader.py          # cached CSV load + feature engineering
│   ├── forecasting.py          # Prophet + SARIMA + XGBoost logic
│   ├── anomaly.py              # Isolation Forest + Z-score logic
│   └── clustering.py           # KMeans + PCA logic
├── models/                     # optional: pre-trained pickles to avoid retraining on every load
├── data/train.csv
├── requirements.txt
└── README.md
```

Use `st.cache_data` for data loading/feature engineering and `st.cache_resource` for trained models, so the app doesn't retrain on every interaction. Use `st.set_page_config(layout="wide")` and Streamlit's native multipage app structure (`pages/` folder with numeric prefixes for ordering).

## 4. Page 1 — Sales Overview Dashboard

- **Total sales by year**: bar chart, `df.groupby('Year')['Sales'].sum()`.
- **Monthly sales trend**: line chart of `df.groupby(pd.Grouper(key='Order Date', freq='ME'))['Sales'].sum()`, optionally overlay a 3-month centered rolling average (matches notebook Task 2 style).
- **Sales by region and category**: interactive filters (`st.multiselect` or `st.selectbox` for Region, Category, Segment, and a date range) driving a grouped bar chart of `df.groupby(['Region','Category'])['Sales'].sum()`.
- Use Plotly (`plotly.express`) instead of static Matplotlib for interactivity (hover tooltips, zoom).

## 5. Page 2 — Forecast Explorer

**Reproduce Task 4 exactly** (segment-level Prophet forecasting), not a generic model.

- Dropdown to select `Category` or `Region` as the grouping dimension, then a second dropdown for the specific value (e.g. Furniture, Technology, Office Supplies / West, East, South, Central).
- Build the monthly series for the selected segment:
  ```python
  ts = df[df[col] == val].set_index('Order Date').resample('ME')['Sales'].sum()
  ```
- **Forecast horizon slider**: 1, 2, or 3 months ahead (`st.select_slider` or `st.slider` with `options=[1,2,3]`).
- **Model: Facebook Prophet**, fit with these exact hyperparameters (from the notebook):
  ```python
  Prophet(
      yearly_seasonality=True,
      weekly_seasonality=False,
      daily_seasonality=False,
      seasonality_mode='additive',
      changepoint_prior_scale=0.05,
      seasonality_prior_scale=10
  )
  ```
- Evaluation protocol: hold out the last `horizon` months as test set, fit on the rest, predict, then compute:
  ```python
  MAE  = mean_absolute_error(test, pred)
  RMSE = sqrt(mean_squared_error(test, pred))
  MAPE = mean(|(true-pred)/true|) * 100   # exclude zero-sales rows
  ```
  Display MAE and RMSE (as in the task spec) below the chart, formatted as currency.
- Then refit Prophet on the **full** series and forecast the next `horizon` months for the actual display, with `yhat_lower`/`yhat_upper` confidence band shown as a shaded region on the Plotly chart (mirrors `task4_individual.png` / `task4_combined.png`).
- Note: the notebook's overall Task 3 model bake-off (SARIMA vs Prophet vs XGBoost) selected **Prophet as best model** by lowest MAPE — carry that selection forward here rather than re-deciding at runtime. If you want to preserve the full comparison, add an optional "Show all 3 models" expander using the exact SARIMA order `(1,1,1)x(1,1,1,12)` and XGBoost params below, but Prophet is the primary displayed model.

  XGBoost params (for reference / optional comparison panel):
  ```python
  XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=3,
               subsample=0.8, colsample_bytree=0.8, random_state=42)
  ```
  Features: `lag_1, lag_2, lag_3, rolling_mean_3 (shifted), month, quarter, season`.

  SARIMA params (for reference):
  ```python
  SARIMAX(ts, order=(1,1,1), seasonal_order=(1,1,1,12),
          enforce_stationarity=False, enforce_invertibility=False)
  ```

## 6. Page 3 — Anomaly Report

**Reproduce Task 5 exactly** (weekly sales, two-method anomaly detection).

- Base series: `df.set_index('Order Date').resample('W')['Sales'].sum()`.
- **Method 1 — Isolation Forest**, feature matrix = `[sales, rolling_mean(4,center), rolling_std(4,center), lag_1, lag_2]`, model:
  ```python
  IsolationForest(n_estimators=200, contamination=0.07, random_state=42, max_samples='auto')
  ```
  `-1` = anomaly.
- **Method 2 — Rolling Z-Score**: 8-week centered rolling window, threshold `|z| > 2.0`.
- Display chart: weekly sales line + 4-week rolling mean ±2σ band + anomaly markers (reuse the notebook's visual language: crimson triangle-down for high-confidence/Isolation Forest anomalies). Let the user toggle between Isolation Forest / Z-Score / "Both agree" (intersection) via `st.radio`.
- **Anomaly table**: date, sales value, method flagged (Isolation Forest / Z-Score / Both), and anomaly score/z-score — sortable, matching the notebook's `anomaly_details` structure.
- Optionally surface the notebook's qualitative month-based explanations (holiday season, Q3 close, back-to-school, etc.) as a caption/tooltip.

## 7. Page 4 — Product Demand Segments

**Reproduce Task 6 exactly** (sub-category KMeans clustering).

- Feature matrix per Sub-Category: `total_sales` (sum), `avg_order_value` (mean), `volatility` (std of monthly sales), `yoy_growth_pct` (% change from first to last year of data). Drop NaNs.
- Scale with `StandardScaler`.
- **K selection**: run elbow (inertia) + silhouette score for K in `range(2, 10)`; select K by best silhouette score (`OPTIMAL_K`) — display this chart too if practical, or hardcode the resulting K if you pre-compute it once (recommended for a snappy live app — see §9).
- **Model**: `KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=20)`.
- **Cluster auto-labeling logic** (reuse verbatim): rules based on whether each cluster's centroid is above/below the median on `total_sales`, `yoy_growth_pct`, `volatility`, `avg_order_value` → labels like "High Volume, Stable Growth", "Niche, High-Value Orders", "Low Volume, High Volatility", "Mature, Stable Demand", etc. Ensure uniqueness (append cluster id if labels collide).
- **Visualization**: PCA(2 components) scatter of sub-categories colored by cluster, annotated with sub-category names, centroids marked with an X — recreate `task6_clusters.png` in Plotly for interactivity.
- **Table**: sub-category → cluster label mapping, plus the cluster profile table (avg total sales, avg order value, volatility, YoY growth per cluster).
- Optionally include the stocking-strategy recommendation text per cluster (already written in the notebook) as an info panel.

## 8. Cross-cutting Requirements

- **Styling**: wide layout, consistent color palette across pages (reuse notebook's hex palette: `#4C72B0, #DD8452, #55A868, #C44E52, #8172B2` for category/region colors).
- **Sidebar**: global nav is automatic via Streamlit multipage; add a sidebar footer with data date range and last-refreshed timestamp.
- **Performance**: cache all data loading and model fitting (`st.cache_data` / `st.cache_resource`) keyed on relevant params (e.g. segment name, horizon) so switching dropdowns doesn't refit everything unnecessarily.
- **Error handling**: guard against segments with too few data points to fit Prophet/KMeans; show a friendly `st.warning` instead of crashing.
- **Charts**: use Plotly for all interactive charts (hover, zoom, legend toggle) rather than static Matplotlib PNGs, since this is a live app, not a notebook export.

## 9. Performance Strategy for Deployment (important)

Streamlit Community Cloud has limited CPU/RAM and cold-starts on every session. Prophet and IsolationForest/KMeans fits are cheap on this dataset size (9.8K rows) but still:
- Pre-compute and pickle the Task 5 (anomaly) and Task 6 (clustering) results at build time since they don't depend on user input — load from pickle at runtime instead of refitting per session.
- Only Page 2 (Forecast Explorer) needs to fit live, since it depends on user-selected segment + horizon — keep this fast (Prophet fits in ~1–2s on monthly data) and cache by `(segment, horizon)` key.

## 10. requirements.txt

```
streamlit
pandas
numpy
plotly
prophet
scikit-learn
xgboost
statsmodels
```
(Note: `prophet` on Streamlit Cloud needs `pystan`/`cmdstanpy` build deps — pin a recent `prophet` version and test the deploy early; this is the most common failure point.)

## 11. Deployment Steps

1. Push the repo (with `data/train.csv` or a public download step) to GitHub.
2. Go to share.streamlit.io → "New app" → select repo, branch, and `app.py` as the entry point.
3. Confirm `requirements.txt` builds cleanly (watch for the Prophet/cmdstanpy build step — it's slow, ~5–10 min on first deploy).
4. Test all 4 pages on the live URL, especially Prophet fitting speed on Page 2.
5. Submit the live `*.streamlit.app` URL.

## 12. Acceptance Checklist

- [ ] Page 1: year bar chart, monthly trend line, region×category filtered bar chart
- [ ] Page 2: Category/Region dropdown, 1/2/3-month horizon slider, Prophet forecast chart with CI band, MAE + RMSE shown
- [ ] Page 3: anomaly chart (Isolation Forest + Z-Score), anomaly table with dates/sales/scores
- [ ] Page 4: PCA cluster scatter, sub-category → cluster label table
- [ ] Deployed and reachable at a public Streamlit Cloud URL
