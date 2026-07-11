import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.data_loader import load_data, build_segment_ts
from utils.forecasting import forecast_segment, sarima_forecast, xgboost_forecast
from utils.ui import apply_chart_motion, inject_styles, page_heading, render_sidebar

st.set_page_config(page_title="Forecast Explorer", layout="wide", page_icon="↗")
inject_styles(); df=load_data(); render_sidebar(df); page_heading("Forecast Explorer", "Historical performance versus algorithmic projection with 95% confidence intervals.")
a,b,c=st.columns(3); col=a.selectbox("Group by",["Category","Region"]); val=b.selectbox("Segment",sorted(df[col].astype(str).unique())); horizon=c.slider("Forecast horizon (months)",1,3,1)
ts=build_segment_ts(df,col,val)
if len(ts)<24: st.warning("This segment needs at least 24 months of sales history."); st.stop()
with st.spinner("Running Prophet forecast..."): result=forecast_segment(ts,horizon)
st.markdown("<div class='top-rule'></div><div class='panel-title'>Sales Forecast Analysis</div><p class='panel-copy'>The observed history, forecast trajectory, and uncertainty band are shown below.</p>", unsafe_allow_html=True)
fc=result['forecast']; future=fc[fc.ds>ts.index.max()]
test_dates, test_actual, test_pred = result['test_dates'], result['test_actual'], result['test_pred']
fig=go.Figure()
fig.add_scatter(x=ts.index,y=ts.values,name="Actual sales",line=dict(color="#000",width=3),hovertemplate='%{x|%b %Y}<br>Actual: $%{y:,.2f}<extra></extra>')
fig.add_scatter(x=test_dates,y=test_pred,name="Back-test prediction",mode="lines+markers",line=dict(color="#DD8452",width=2,dash="dot"),marker=dict(size=8),hovertemplate='%{x|%b %Y}<br>Back-test: $%{y:,.2f}<extra></extra>')
fig.add_scatter(x=future.ds,y=future.yhat,name="Future forecast",line=dict(color="#005db6",dash="dash",width=3),hovertemplate='%{x|%b %Y}<br>Forecast: $%{y:,.2f}<extra></extra>')
fig.add_scatter(x=list(future.ds)+list(future.ds[::-1]),y=list(future.yhat_upper)+list(future.yhat_lower[::-1]),fill="toself",fillcolor="rgba(0,93,182,.14)",line=dict(color="rgba(0,0,0,0)"),name="95% confidence range",hoverinfo='skip')
fig.add_vline(x=ts.index.max(),line_dash="dot",line_color="#000",annotation_text='Forecast start',annotation_font_color='#000')
fig.update_layout(template="plotly_white",title=f"{val} demand outlook",margin=dict(l=20,r=20,t=50,b=20),hovermode='x unified')
fig.update_yaxes(tickprefix='$',tickformat='~s')
st.plotly_chart(apply_chart_motion(fig),width='stretch')
m1,m2,m3=st.columns(3); m1.metric("MAE",f"${result['MAE']:,.0f}");m2.metric("RMSE",f"${result['RMSE']:,.0f}");m3.metric("MAPE",f"{result['MAPE']:.1f}%")
with st.expander("Show all 3 models"):
    rows=[{"Model":"Prophet",**{k:result[k] for k in ('MAE','RMSE','MAPE')}},{"Model":"SARIMA",**sarima_forecast(ts,horizon)},{"Model":"XGBoost",**xgboost_forecast(ts,horizon)}]; st.dataframe(pd.DataFrame(rows).style.format({'MAE':'${:,.0f}','RMSE':'${:,.0f}','MAPE':'{:.1f}%'}),use_container_width=True)
