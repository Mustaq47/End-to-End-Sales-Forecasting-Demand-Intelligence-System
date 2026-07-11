"""Shared Stitch-inspired visual shell for the Streamlit pages."""
from datetime import datetime
import streamlit as st


def inject_styles():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    :root{--blue:#005db6;--ink:#000;--muted:#262626;--bg:#f9f9fe;--card:#fff;--line:#c4c6d0;--soft:#f1f4f9;--green:#087b52;--red:#ba1a1a}
    @keyframes page-enter{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}@keyframes card-enter{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}@keyframes scroll-reveal{from{opacity:1;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
    /* User-selected accessibility rule: every visible label uses solid black. */
    .stApp,.stApp *,.stSidebar,.stSidebar *,[data-testid=stSidebar],[data-testid=stSidebar] *{color:#000!important}
    html,body,[class*=stApp]{background:var(--bg);color:var(--ink);font-family:Inter,sans-serif}.block-container{max-width:none;padding:46px 48px 60px;animation:page-enter .42s ease-out}.stApp header{background:transparent}.stSidebar{background:#fff;border-right:1px solid var(--line);color:#000}.stSidebar [data-testid=stSidebarContent]{padding:26px 14px}[data-testid=stSidebarNav],.stSidebarNav{display:none}
    h1,h2,h3{font-family:'Hanken Grotesk',sans-serif!important;letter-spacing:-.02em}.stMarkdown h1{font-size:40px!important;font-weight:800!important;margin-bottom:4px}.stCaption,.stSidebar label,[data-testid=stMetricLabel]{font-family:'JetBrains Mono',monospace!important;letter-spacing:.06em;text-transform:uppercase}.stCaption{color:var(--muted)!important;font-size:11px}.stSidebar h2{font-size:22px!important;margin:0}.stSidebar h4{font-family:'JetBrains Mono';font-size:11px;letter-spacing:.16em;color:var(--muted);margin-top:3px}
    [data-testid=stSidebar] a,[data-testid=stSidebar] a *,[data-testid=stSidebar] [data-testid*=PageLink],[data-testid=stSidebar] [data-testid*=PageLink] *{color:#000!important;opacity:1!important;text-shadow:none!important;filter:none!important}[data-testid=stSidebar] a{display:flex!important;align-items:center!important;padding:10px 12px!important;margin:3px 0!important;border-radius:8px!important;font-weight:600!important;transition:background .18s ease,transform .18s ease!important}[data-testid=stSidebar] a:hover{background:#eaf2ff!important;transform:translateX(3px)}
    .stButton>button{min-height:38px;border-radius:7px;border:1px solid var(--line);font-family:Inter;font-weight:700;background:#fff;color:#000;transition:transform .18s ease,background .18s ease}.stButton>button:hover{transform:translateY(-1px);background:#f1f4f9}.stButton>button[kind=primary]{background:#000;color:#fff;border-color:#000}
    [data-testid=stMetric]{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:19px 20px;box-shadow:0 2px 3px rgba(26,28,30,.06);transition:transform .18s ease,box-shadow .18s ease}[data-testid=stMetric]:hover{transform:translateY(-3px);box-shadow:0 8px 18px rgba(26,28,30,.10)}[data-testid=stMetricValue]{font-family:'Hanken Grotesk';font-size:30px;font-weight:800}[data-testid=stMetricDelta]{font-weight:700}.stPlotlyChart{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px;box-shadow:0 2px 3px rgba(26,28,30,.04);transition:box-shadow .18s ease}.stPlotlyChart:hover{box-shadow:0 8px 18px rgba(26,28,30,.08)}
    .stPlotlyChart{content-visibility:visible!important;contain:none!important;opacity:1!important}.stPlotlyChart .main-svg text,.stPlotlyChart .main-svg .legendtext,.stPlotlyChart .main-svg .gtitle,.stPlotlyChart .main-svg .xtick text,.stPlotlyChart .main-svg .ytick text{fill:#000!important;color:#000!important;opacity:1!important;visibility:visible!important}.stPlotlyChart [class*=hoverlayer] text{fill:#000!important;color:#000!important;opacity:1!important}@supports (animation-timeline:view()){[data-testid=stMetric],[data-testid=stDataFrame]{animation:scroll-reveal linear both;animation-timeline:view();animation-range:entry 0% cover 32%}}
    [data-baseweb=select]>div,[data-baseweb=base-input] input,.stDateInput input{background:#fff;border-color:var(--line)!important;border-radius:6px;color:#000!important}.stDataFrame{border:1px solid var(--line);border-radius:8px;overflow:hidden}.section-kicker{font:600 11px 'JetBrains Mono';letter-spacing:.14em;color:var(--blue);text-transform:uppercase;margin-bottom:7px}.page-subtitle{font-size:17px;color:var(--muted);margin:0}.top-rule{border-top:1px solid var(--line);margin:28px 0 22px}.panel-title{font:700 20px 'Hanken Grotesk';margin:0 0 5px}.panel-copy{font-size:14px;color:var(--muted);margin:0 0 14px}.side-brand{padding:2px 10px 22px}.side-brand b{font:800 22px 'Hanken Grotesk'}.side-brand span{display:block;font:500 10px 'JetBrains Mono';letter-spacing:.18em;color:var(--muted);margin-top:4px}.side-footer{font:500 10px/1.6 'JetBrains Mono';letter-spacing:.08em;color:var(--muted);padding:18px 10px 0}.nav-gap{height:10px}
    </style>""", unsafe_allow_html=True)


def render_sidebar(df):
    with st.sidebar:
        st.markdown("<div class='side-brand'><b>F&D Intelligence</b><span>Retail Synthesis Engine</span></div>", unsafe_allow_html=True)
        st.page_link("app.py", label="Intelligence Home")
        st.page_link("pages/1_Sales_Overview.py", label="Sales Overview")
        st.page_link("pages/2_Forecast_Explorer.py", label="Forecast Explorer")
        st.page_link("pages/3_Anomaly_Report.py", label="Anomaly Report")
        st.page_link("pages/4_Product_Demand_Segments.py", label="Product Demand Segments")
        st.markdown("<div class='top-rule'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='side-footer'>DATA RANGE<br>{df['Order Date'].min():%d %b %Y} — {df['Order Date'].max():%d %b %Y}<br><br>LAST REFRESHED<br>{datetime.now():%d %b %Y · %H:%M}</div>", unsafe_allow_html=True)


def page_heading(title, subtitle, kicker="Superstore intelligence"):
    st.markdown(f"<div class='section-kicker'>{kicker}</div><h1>{title}</h1><p class='page-subtitle'>{subtitle}</p>", unsafe_allow_html=True)


def apply_chart_motion(fig):
    """Keep Plotly charts interactive and animate updates from page controls."""
    fig.update_layout(
        transition={"duration": 450, "easing": "cubic-in-out"},
        hovermode="x unified",
        font={"color": "#000000", "family": "Inter, sans-serif"},
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        hoverlabel={"bgcolor": "#ffffff", "font": {"color": "#000000", "family": "Inter, sans-serif"}, "bordercolor": "#000000"},
        title_font={"color": "#000000", "family": "Hanken Grotesk, sans-serif"},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0, "font": {"color": "#000000", "family": "Inter, sans-serif"}},
        margin={"l": 22, "r": 22, "t": 72, "b": 28},
    )
    fig.update_xaxes(gridcolor="#e5e7eb", zerolinecolor="#d1d5db", showline=False, fixedrange=False, visible=True, showticklabels=True, color="#000000", tickfont={"color": "#000000"}, title_font={"color": "#000000"})
    fig.update_yaxes(gridcolor="#e5e7eb", zerolinecolor="#d1d5db", showline=False, fixedrange=False, visible=True, showticklabels=True, color="#000000", tickfont={"color": "#000000"}, title_font={"color": "#000000"})
    fig.update_annotations(font={"color": "#000000"}, arrowcolor="#000000")
    return fig
