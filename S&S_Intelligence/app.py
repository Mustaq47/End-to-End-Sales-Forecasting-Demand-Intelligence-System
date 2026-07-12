import streamlit as st
from utils.data_loader import load_data
from utils.ui import inject_styles, page_heading, render_sidebar

st.set_page_config(page_title="Superstore Sales Intelligence", layout="wide", page_icon="📊")
inject_styles()
df = load_data()
render_sidebar(df)
page_heading("Superstore Sales Intelligence", "A unified operating view for sales performance, forward demand, exceptions, and product-level decisions.", "Enterprise analytics")
st.markdown("<div class='top-rule'></div>", unsafe_allow_html=True)
c1,c2,c3=st.columns(3)
c1.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
c2.metric("Orders", f"{df['Order ID'].nunique():,}")
c3.metric("Data Coverage", f"{df['Order Date'].min():%Y}–{df['Order Date'].max():%Y}")
st.markdown("<div class='top-rule'></div><div class='panel-title'>Select a workspace</div><p class='panel-copy'>Use the navigation rail to explore the sales overview, forecast models, anomaly monitoring, or demand segmentation.</p>", unsafe_allow_html=True)
