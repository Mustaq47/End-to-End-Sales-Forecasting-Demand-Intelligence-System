# Superstore Sales Intelligence Dashboard

A production-ready multi-page Streamlit application designed for forecasting, demand modeling, exception detection, and segment clustering.

## 🚀 Getting Started

1. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

## 📂 Directory Structure

- `app.py`: Landing page and metrics summary.
- `pages/`: Page modules for sales overview, forecasting models, anomaly logs, and demand clustering.
- `utils/`: Core processing logic (forecasting, data loader, anomaly detection, UI theme).
- `data/`: Contains dataset `train.csv` (when initialized/downloaded).
