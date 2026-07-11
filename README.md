# End-to-End Sales Forecasting & Demand Intelligence System

A production-grade, multi-page Streamlit application and analytics system designed to model, forecast, and analyze retail sales and demand patterns using the Kaggle Superstore Sales dataset.

This repository implements rigorous exploratory data analysis, time-series forecasting (Prophet, SARIMA, XGBoost), weekly anomaly detection (Isolation Forest & Z-Score), and product demand segmentation (K-Means Clustering & PCA).

---

## 📂 Project Structure

```text
├── Analysis3.ipynb              # Jupyter notebook detailing tasks 1–6
├── Charts/                      # Visualizations generated during analysis
├── superstore-dashboard/        # Production Streamlit application
│   ├── app.py                   # Home / landing page
│   ├── requirements.txt         # Application dependencies
│   ├── pages/                   # Multi-page application structure
│   │   ├── 1_Sales_Overview.py  # Sales overview dashboard
│   │   ├── 2_Forecast_Explorer.py # Interactive Prophet forecasting
│   │   ├── 3_Anomaly_Report.py  # Weekly outlier & exception report
│   │   └── 4_Product_Demand_Segments.py # K-Means clustering analysis
│   └── utils/                   # Shared utility modules
│       ├── __init__.py
│       ├── anomaly.py           # Isolation Forest + Z-score implementation
│       ├── clustering.py        # K-Means + PCA pipeline
│       ├── data_loader.py       # Data parser & feature engineer
│       ├── forecasting.py       # Prophet + SARIMA + XGBoost pipelines
│       └── ui.py                # Visual styling & theme settings
└── train.csv                    # Source Kaggle Superstore Sales dataset
```

---

## 🛠️ Installation & Setup

1. **Clone the Repository** (or navigate to the project directory):
   ```bash
   git clone git@github.com:Mustaq47/End-to-End-Sales-Forecasting-Demand-Intelligence-System.git
   cd End-to-End-Sales-Forecasting-Demand-Intelligence-System
   ```

2. **Install Dependencies**:
   Install the required libraries listed in the dashboard requirements:
   ```bash
   pip install -r superstore-dashboard/requirements.txt
   ```

3. **Run the Streamlit Application**:
   Navigate to the dashboard directory and start the Streamlit server:
   ```bash
   cd superstore-dashboard
   streamlit run app.py
   ```

---

## 📊 Application Workspaces

### 1. Sales Overview Dashboard
Provides high-level performance insights including:
- Annual sales summary.
- Interactive monthly sales trends with 3-month rolling averages.
- Multi-select filters for Category, Region, Segment, and Date Range.

### 2. Forecast Explorer
Allows interactive demand projections for specific categories or regions:
- Uses **Facebook Prophet** as the primary forecasting engine.
- Back-tests performance using historical subsets and calculates MAE, RMSE, and MAPE.
- Compares Prophet model against **SARIMA** `(1,1,1)x(1,1,1,12)` and **XGBoost Regressor** models.

### 3. Anomaly Report
Monitors weekly sales fluctuations using complementary outlier detection techniques:
- **Isolation Forest** (detects multi-dimensional anomalies using rolling statistics and lags).
- **Z-Score** (detects threshold violations based on standard deviations).
- Generates a detailed audit log with contextual notes on typical retail seasonal behavior.

### 4. Product Demand Segments
Groups products into demand profiles using **K-Means Clustering** & **Principal Component Analysis (PCA)**:
- Places product sub-categories into behavioral segments based on total sales, average order value, growth rate, and volatility.
- Recommends replenishment and stocking strategies optimized for each segment (e.g. high-volume stable vs high-volatility niche).

---

## 📓 Notebook Analysis
The exploratory work, model configuration searches, and mathematical implementations are fully documented in [Analysis3.ipynb](file:///d:/intership/End-to-End%20Sales%20Forecasting%20&%20Demand%20Intelligence%20System/Analysis3.ipynb). Refer to this notebook for technical background on model parameters, evaluation runs, and outlier threshold selections.
