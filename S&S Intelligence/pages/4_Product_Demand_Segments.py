import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.data_loader import load_data
from utils.clustering import compute_clusters
from utils.ui import apply_chart_motion, inject_styles, page_heading, render_sidebar

STRATEGIES={'High Volume, Stable Growth':'Maintain availability with planned replenishment and moderate safety stock.','High Volume, High Volatility':'Use frequent monitoring, short replenishment cycles, and adaptive safety stock.','Low Volume, Growing Demand':'Increase test inventory gradually and monitor acceleration.','Low Volume, High Volatility':'Keep lean stock and replenish only from proven demand signals.','Niche, High-Value Orders':'Prioritize service levels and protect margin with selective stocking.','Mature, Stable Demand':'Optimize for efficient, predictable replenishment.'}
st.set_page_config(page_title='Product Demand Segments',layout='wide',page_icon='◇')
inject_styles(); df=load_data(); render_sidebar(df); r=compute_clusters(df); f=r['feat_df'].reset_index(); page_heading('Product Demand Segments',f"Demand-pattern clustering with an optimal {r['optimal_k']}-cluster solution.", 'Demand intelligence')
st.markdown("<div class='top-rule'></div><div class='panel-title'>Demand Distribution Matrix</div><p class='panel-copy'>Sub-categories are positioned by their normalized sales and demand-pattern features.</p>",unsafe_allow_html=True)
left,right=st.columns([2,1]); focus=left.selectbox('Focus demand segment',['All segments']+sorted(f['Label'].unique())); show_labels=right.toggle('Show point labels',value=False)
view=f if focus=='All segments' else f[f['Label']==focus]
fig=px.scatter(view,x='PCA1',y='PCA2',color='Label',size='total_sales',size_max=30,text='Sub-Category' if show_labels else None,hover_name='Sub-Category',hover_data={'total_sales':':$,.0f','avg_order_value':':$,.0f','yoy_growth_pct':':.1f','volatility':':$,.0f','PCA1':False,'PCA2':False},color_discrete_sequence=['#005db6','#DD8452','#55A868','#C44E52','#8172B2'],opacity=.86)
cent=view.groupby('Cluster')[['PCA1','PCA2']].mean();fig.add_scatter(x=cent.PCA1,y=cent.PCA2,mode='markers',marker=dict(symbol='x',size=14,color='#000',line=dict(width=2)),name='Centroids',hovertemplate='Cluster centroid<extra></extra>');fig.update_traces(marker=dict(line=dict(color='#ffffff',width=1)));fig.add_hline(y=0,line_color='#d1d5db',line_width=1);fig.add_vline(x=0,line_color='#d1d5db',line_width=1);fig.update_layout(template='plotly_white',title='Demand landscape',xaxis_title='Demand pattern axis 1',yaxis_title='Demand pattern axis 2');st.plotly_chart(apply_chart_motion(fig),width='stretch')
profile=r['cluster_means'].copy();profile['Label']=profile.index.map(r['labels']);st.markdown("<div class='panel-title'>Cluster Profile</div><p class='panel-copy'>Average commercial characteristics of each identified demand group.</p>",unsafe_allow_html=True);st.dataframe(profile.style.format({'total_sales':'${:,.0f}','avg_order_value':'${:,.0f}','volatility':'${:,.0f}','yoy_growth_pct':'{:.1f}%'}),use_container_width=True)
st.subheader('Stocking Strategy')
for label in r['labels'].values():
    base=label.rsplit(' (',1)[0]
    with st.expander(label): st.write(STRATEGIES.get(base,'Review the cluster profile and use demand-led replenishment.'))
