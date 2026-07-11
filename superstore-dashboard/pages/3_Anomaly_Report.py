import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.data_loader import load_data
from utils.anomaly import compute_anomalies
from utils.ui import apply_chart_motion, inject_styles, page_heading, render_sidebar

REASONS={1:"Post-holiday returns and inventory reconciliation.",2:"Short trading month and promotional resets.",3:"Spring demand replenishment.",4:"Seasonal campaign activity.",5:"Mid-year purchasing cycles.",6:"Summer demand shifts.",7:"Holiday event timing can change weekly volume.",8:"Back-to-school and late-summer activity.",9:"Autumn inventory build.",10:"Early holiday procurement.",11:"Black Friday and holiday promotion effects.",12:"Holiday peak and year-end close."}
st.set_page_config(page_title="Anomaly Report",layout="wide",page_icon="⚠")
inject_styles(); df=load_data(); render_sidebar(df); r=compute_anomalies(df); page_heading("System Health & Anomalies", "Weekly sales monitoring with complementary outlier detection methods.", "Real-time monitoring"); mode=st.radio("Show anomalies from",["Isolation Forest","Z-Score","Both (high confidence)"],horizontal=True)
weekly=r['weekly_ts']; iso=pd.Series(r['iso_labels']==-1,index=weekly.index); z=r['z_anomaly_mask']; mask=iso if mode=="Isolation Forest" else z if mode=="Z-Score" else iso & z
detail=pd.DataFrame({'Sales':weekly,'Expected':r['roll_mean'],'Z-Score':r['z_scores'],'Isolation Score':r['iso_scores'],'Isolation Forest':iso,'Z-Score Flag':z})
detail['Deviation (%)']=((detail['Sales']-detail['Expected'])/detail['Expected']*100).replace([float('inf'),float('-inf')],0).fillna(0)
detail['Method']=detail.apply(lambda row:'Both' if row['Isolation Forest'] and row['Z-Score Flag'] else 'Isolation Forest' if row['Isolation Forest'] else 'Z-Score' if row['Z-Score Flag'] else 'Normal',axis=1)
selected=detail[mask]
c1,c2,c3=st.columns(3); c1.metric('Selected events',f'{len(selected):,}'); c2.metric('Largest deviation',f"{selected['Deviation (%)'].abs().max():.1f}%" if not selected.empty else '0.0%'); c3.metric('High-confidence events',f'{int((iso & z).sum()):,}')
st.markdown("<div class='top-rule'></div><div class='panel-title'>Weekly Sales Monitor</div><p class='panel-copy'>Crimson markers identify selected anomaly events against the rolling expected range.</p>", unsafe_allow_html=True)
fig=go.Figure();fig.add_scatter(x=weekly.index,y=r['roll_mean']+2*r['roll_std'],line=dict(width=0),showlegend=False,hoverinfo='skip');fig.add_scatter(x=weekly.index,y=r['roll_mean']-2*r['roll_std'],fill='tonexty',fillcolor='rgba(0,93,182,.12)',line=dict(width=0),name='Expected range',hoverinfo='skip');fig.add_scatter(x=weekly.index,y=r['roll_mean'],name='4-week mean',line=dict(color='#6b7280',width=2,dash='dot'),hovertemplate='%{x|%d %b %Y}<br>Expected: $%{y:,.2f}<extra></extra>');fig.add_scatter(x=weekly.index,y=weekly,name="Weekly sales",line=dict(color="#005db6",width=3),hovertemplate='%{x|%d %b %Y}<br>Sales: $%{y:,.2f}<extra></extra>');fig.add_scatter(x=selected.index,y=selected['Sales'],mode='markers',marker=dict(symbol='triangle-down',size=13,color='#ba1a1a',line=dict(color='#000',width=1)),customdata=selected[['Expected','Deviation (%)','Z-Score','Isolation Score','Method']],name='Selected anomaly',hovertemplate='<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.2f}<br>Expected: $%{customdata[0]:,.2f}<br>Deviation: %{customdata[1]:.1f}%<br>Z-score: %{customdata[2]:.2f}<br>Isolation score: %{customdata[3]:.3f}<br>Method: %{customdata[4]}<extra></extra>');fig.update_layout(template='plotly_white',title='Weekly sales anomaly monitor');fig.update_yaxes(tickprefix='$',tickformat='~s');st.plotly_chart(apply_chart_motion(fig),width='stretch')
rows=[]
for date,row in selected.iterrows(): rows.append({'Date':date,'Sales ($)':row['Sales'],'Expected ($)':row['Expected'],'Deviation (%)':row['Deviation (%)'],'Method':row['Method'],'Z-Score':row['Z-Score'],'Isolation Score':row['Isolation Score'],'Explanation':REASONS[date.month]})
table=pd.DataFrame(rows);st.markdown("<div class='panel-title'>Detection Log</div><p class='panel-copy'>Each event includes its expected level, deviation, model scores, and a month-based business context.</p>",unsafe_allow_html=True);st.dataframe(table.style.apply(lambda row:['background-color:#ffdad6' if row.Method=='Both' else '' for _ in row],axis=1).format({'Sales ($)':'${:,.0f}','Expected ($)':'${:,.0f}','Deviation (%)':'{:.1f}%','Z-Score':'{:.2f}','Isolation Score':'{:.3f}'}),width='stretch')
