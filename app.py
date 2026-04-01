import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

# --- 1. 设置 Apple 风格 CSS ---
st.set_page_config(page_title="Alpha Whale Insight", layout="wide")
st.markdown("""
    <style>
    .main { background: #F5F5F7; font-family: -apple-system, sans-serif; }
    .whale-card {
        background: white; border-radius: 24px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03); margin-bottom: 20px;
    }
    .holding-row {
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 0; border-bottom: 1px solid #F5F5F7;
    }
    .logo-img { width: 28px; height: 28px; border-radius: 6px; margin-right: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 加载数据函数 ---
@st.cache_data
def load_whale_data():
    try:
        with open('whale_holdings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

st.title(" Alpha Whale Tracker")
data = load_whale_data()

if data:
    st.caption(f"最新披露快照：{data['last_updated']} (每季度 13F 披露后人工核验)")
    
    # 动态创建列
    cols = st.columns(len(data['holders']))
    
    for i, (whale_name, holdings) in enumerate(data['holders'].items()):
        with cols[i]:
            st.markdown('<div class="whale-card">', unsafe_allow_html=True)
            st.subheader(whale_name)
            
            # 渲染环形图
            df = pd.DataFrame(holdings)
            fig = go.Figure(data=[go.Pie(labels=df['name'], values=df['percent'], hole=.7)])
            fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # 渲染列表（带 Logo）
            for item in holdings:
                logo = f"https://logo.clearbit.com/{item.get('domain', 'apple.com')}"
                st.markdown(f"""
                    <div class="holding-row">
                        <div style="display:flex; align-items:center;">
                            <img src="{logo}" class="logo-img" onerror="this.src='https://www.google.com/s2/favicons?domain={item.get('domain', 'apple.com')}'">
                            <span style="font-size:14px;">{item['name']}</span>
                        </div>
                        <span style="font-weight:600; color:#86868B;">{item['percent']}%</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ 未能加载持仓数据，请确保 whale_holdings.json 已正确上传至 GitHub 仓库。")
