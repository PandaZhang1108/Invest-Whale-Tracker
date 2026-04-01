import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

# --- 1. 页面配置与 Apple 风格 CSS ---
st.set_page_config(page_title="Alpha Whale Tracker", layout="wide")

st.markdown("""
    <style>
    .main { background: #F5F5F7; font-family: -apple-system, sans-serif; }
    .whale-card {
        background: white; border-radius: 24px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03); margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 加载数据函数 ---
@st.cache_data
def load_whale_data():
    try:
        # 确保你的 GitHub 仓库里有这个文件
        with open('whale_holdings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- 3. 主界面逻辑 ---
st.title("🐋 Alpha Whale Tracker")
data = load_whale_data()

if data:
    st.caption(f"最新披露快照：{data['last_updated']} (数据源：SEC 官方 13F 报表)")
    
    # 动态创建列（根据持有人数量分列，通常是 2 列：巴菲特和段永平）
    holders_dict = data.get('holders', {})
    cols = st.columns(len(holders_dict))
    
    # 【重点修复】：使用 items() 循环，这样 whale_name 才有定义
    for i, (whale_name, holdings) in enumerate(holders_dict.items()):
        with cols[i]:
            st.markdown(f'<div class="whale-card">', unsafe_allow_html=True)
            
            # 标题部分
            st.subheader(f" {whale_name}")
            
            # 将持仓列表转为表格数据
            df_display = pd.DataFrame(holdings)
            
            # 渲染环形图（取前 5 大做视觉展示）
            fig = go.Figure(data=[go.Pie(
                labels=df_display['company'].head(5), 
                values=df_display['percent'].head(5), 
                hole=.7
            )])
            fig.update_layout(showlegend=False, height=200, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # 数据格式化：将原始数值转为带 $ 的千分位格式
            if 'value_usd' in df_display.columns:
                df_display['市值 (USD)'] = df_display['value_usd'].apply(lambda x: f"${x:,.0f}")
            
            df_display['权重'] = df_display['percent'].apply(lambda x: f"{x}%")
            
            # 显示全量持仓表格
            st.markdown(f"**全量持仓清单 ({len(df_display)} 只):**")
            st.dataframe(
                df_display[['company', '市值 (USD)', '权重']], 
                hide_index=True,
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ 未能加载数据。请确认 whale_holdings.json 已上传到 GitHub 项目根目录。")
