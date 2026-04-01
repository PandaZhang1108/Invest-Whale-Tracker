import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

# --- 1. 基础配置 ---
st.set_page_config(page_title="Whale Portfolio Pro", layout="wide")

@st.cache_data
def load_data():
    try:
        with open('whale_holdings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

data = load_data()

# --- 2. 页面顶部 ---
st.title("🐋 Alpha Whale Portfolio Tracker")
if not data:
    st.error("数据加载失败，请检查 JSON 文件。")
    st.stop()

st.caption(f"数据源：SEC 官方 13F 披露 | 更新日期：{data['last_updated']}")

# --- 3. 核心：创建选项卡 (Tabs) ---
whale_names = list(data['holders'].keys())
tabs = st.tabs(whale_names) # 动态创建标签页

for i, tab in enumerate(tabs):
    whale_name = whale_names[i]
    holdings = data['holders'][whale_name]
    df = pd.DataFrame(holdings)
    
    with tab:
        # A. 概览指标卡
        total_val = df['value_usd'].sum() if 'value_usd' in df.columns else 0
        m1, m2, m3 = st.columns(3)
        m1.metric("管理总市值", f"${total_val/1e9:.2f} B")
        m2.metric("持有证券数量", f"{len(df)} 只")
        m3.metric("首要重仓", f"{df.iloc[0]['company']}")

        st.divider()

        # B. 左右布局：左边是可视化，右边是详细明细
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            st.write("##### 持仓分布 (Top 10)")
            top_10 = df.head(10)
            fig = go.Figure(data=[go.Pie(labels=top_10['company'], values=top_10['percent'], hole=.6)])
            fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.write("##### 持仓明细表")
            # 格式化数据展示
            df_display = df.copy()
            if 'value_usd' in df_display.columns:
                df_display['市值 ($)'] = df_display['value_usd'].apply(lambda x: f"${x:,.0f}")
            if 'shares' in df_display.columns:
                df_display['持股数'] = df_display['shares'].apply(lambda x: f"{x:,}")
            df_display['权重 (%)'] = df_display['percent'].apply(lambda x: f"{x}%")
            
            # 只展示关键列
            show_cols = ['company', '市值 ($)', '持股数', '权重 (%)']
            available_cols = [c for c in show_cols if c in df_display.columns]
            
            st.dataframe(
                df_display[available_cols],
                hide_index=True,
                use_container_width=True,
                height=400
            )

# --- 4. 底部声明 ---
st.info("注：13F 数据不包含空头头寸、现金及非美国上市资产，具有 45 天左右的披露滞后性。")
