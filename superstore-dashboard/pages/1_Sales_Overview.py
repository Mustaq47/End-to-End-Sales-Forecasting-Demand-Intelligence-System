import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.data_loader import load_data
from utils.ui import apply_chart_motion, inject_styles, page_heading, render_sidebar

st.set_page_config(page_title="Sales Overview", layout="wide", page_icon="📊")
inject_styles(); df = load_data(); render_sidebar(df); palette=["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]
page_heading("Sales Overview", "Real-time performance metrics across all operational channels.")
with st.sidebar:
    st.subheader("Global Filters")
    st.button("Refresh live view", type="primary", width="stretch")
    regions=st.multiselect("Region", sorted(df.Region.astype(str).unique()))
    categories=st.multiselect("Category", sorted(df.Category.astype(str).unique()))
    segments=st.multiselect("Segment", sorted(df.Segment.astype(str).unique()))
    dates=st.date_input("Date range", (df['Order Date'].min().date(),df['Order Date'].max().date()))
f=df.copy()
if regions: f=f[f.Region.astype(str).isin(regions)]
if categories: f=f[f.Category.astype(str).isin(categories)]
if segments: f=f[f.Segment.astype(str).isin(segments)]
if len(dates)==2: f=f[f['Order Date'].between(str(dates[0]),str(dates[1])+' 23:59:59')]
if f.empty: st.warning("No data for selected filters."); st.stop()
st.caption(f"LIVE FILTER RESULT · {len(f):,} transactions · {f['Order Date'].min():%d %b %Y} — {f['Order Date'].max():%d %b %Y}")
profit_margin = (f["Profit"].sum() / f["Sales"].sum() * 100) if "Profit" in f.columns and f["Sales"].sum() else None
c1,c2,c3,c4=st.columns(4); c1.metric("Total Sales",f"${f.Sales.sum():,.0f}"); c2.metric("Orders",f"{f['Order ID'].nunique():,}"); c3.metric("Avg. Ticket",f"${f.Sales.mean():,.0f}"); c4.metric("Profit Margin", f"{profit_margin:.1f}%" if profit_margin is not None else "N/A", help="Profit is not included in the supplied source CSV.")
st.markdown("<div class='top-rule'></div>",unsafe_allow_html=True)
year=f.groupby('Year',as_index=False,observed=True).Sales.sum()
year_fig=go.Figure(go.Bar(x=year['Year'].astype(str),y=year['Sales'],marker=dict(color='#005db6',line=dict(width=0)),text=year['Sales'],texttemplate='$%{text:,.0f}',textposition='outside',hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>'))
year_fig.update_layout(title='Annual sales performance',showlegend=False,yaxis_title='Sales'); year_fig.update_yaxes(tickprefix='$',tickformat='~s')
st.plotly_chart(apply_chart_motion(year_fig),width='stretch')

monthly=f.set_index('Order Date').resample('ME').Sales.sum(); trend=monthly.to_frame('Sales'); trend['3-Month Rolling Average']=trend.Sales.rolling(3).mean()
peak_date,peak_sales=trend['Sales'].idxmax(),trend['Sales'].max()
trend_fig=go.Figure()
trend_fig.add_scatter(x=trend.index,y=trend['Sales'],name='Monthly sales',mode='lines+markers',line=dict(color='#005db6',width=3),marker=dict(size=6,color='#005db6'),fill='tozeroy',fillcolor='rgba(0,93,182,0.10)',hovertemplate='%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>')
trend_fig.add_scatter(x=trend.index,y=trend['3-Month Rolling Average'],name='3-month average',mode='lines',line=dict(color='#DD8452',width=2,dash='dash'),hovertemplate='%{x|%b %Y}<br>Average: $%{y:,.2f}<extra></extra>')
trend_fig.add_annotation(x=peak_date,y=peak_sales,text=f'Peak<br>${peak_sales:,.0f}',showarrow=True,arrowhead=2,ax=0,ay=-42,bgcolor='#ffffff',bordercolor='#000000',font=dict(color='#000000'))
trend_fig.update_layout(title='Monthly sales trend',yaxis_title='Sales'); trend_fig.update_yaxes(tickprefix='$',tickformat='~s')
st.plotly_chart(apply_chart_motion(trend_fig),width='stretch')

region_cat=f.groupby(['Region','Category'],as_index=False,observed=True).Sales.sum()
region_fig=px.bar(region_cat,x='Region',y='Sales',color='Category',barmode='group',color_discrete_sequence=palette,category_orders={'Category':sorted(region_cat['Category'].astype(str).unique())},title='Regional category mix')
region_fig.update_traces(marker_line_width=0,hovertemplate='<b>%{x}</b><br>%{fullData.name}: $%{y:,.2f}<extra></extra>'); region_fig.update_yaxes(tickprefix='$',tickformat='~s')
st.plotly_chart(apply_chart_motion(region_fig),width='stretch')
