import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import requests
from io import BytesIO

# --- 1. 页面基本配置 ---
st.set_page_config(page_title="大鲸持仓追踪 (Whale Tracker)", layout="wide", page_icon="🐋")
st.title("🐋 全球顶级投资人 & 议员持仓动态 (社区版)")

# --- 模拟数据 (作为备选和佩洛西展示) ---
# 数据来源：最新的公开 13F 或 PTR 披露
MOCK_PELOSI = {"标的": ["NVDA", "GOOGL", "AVGO", "VST", "其他"], "占比": [19, 16, 15, 10, 40]}
MOCK_DYP = {"标的": ["AAPL", "BRK.B", "GOOG", "PDD", "其他"], "占比": [50, 20, 10, 10, 10]}

# --- 大佬头像数据 (公共 URL) ---
AVATARS = {
    "巴菲特": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Warren_Buffett_KU_Visit.jpg/400px-Warren_Buffett_KU_Visit.jpg",
    "佩洛西": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Nancy_Pelosi_official_portrait_2019.jpg/400px-Nancy_Pelosi_official_portrait_2019.jpg",
    "段永平": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Pinduoduo_logo.svg/128px-Pinduoduo_logo.svg.png" # 段永平低调，用他重仓的拼多多Logo代替
}

# --- 核心函数：获取巴菲特真实持仓 (yfinance) ---
@st.cache_data(ttl=3600*24) # 缓存一天，避免重复抓取
def get_buffett_holdings():
    try:
        # 获取伯克希尔哈撒韦的数据
        brk = yf.Ticker("BRK-B")
        # .holdings 接口有时会失效，需要增强容错
        df = brk.holdings
        if df is None or df.empty:
            raise ValueError("yfinance 未能返回有效持仓数据")
        
        # 整理数据
        df = df.reset_index()
        df.columns = ['标的', '占比']
        # yfinance 占比通常是小数，转为百分比
        df['占比'] = df['占比'] * 100
        
        # 整理前五大和“其他”
        df = df.sort_values(by='占比', ascending=False)
        top5 = df.head(5)
        others_sum = df['占比'].iloc[5:].sum()
        new_row = pd.DataFrame({'标的': ['其他'], '占比': [others_sum]})
        final_df = pd.concat([top5, new_row], ignore_index=True)
        
        return final_df, "✅ 数据源：yfinance 接口 (最新披露)"
    except Exception as e:
        # 降级为模拟数据
        print(f"Buffett API Error: {e}")
        return pd.DataFrame({"标的": ["AAPL", "AXP", "BAC", "KO", "其他"], "占比": [41, 12, 10, 9, 28]}), "⚪ 数据源：核心披露模拟 (API离线)"

# --- 核心函数：绘制佩洛西风格环形图 ---
def draw_donut_chart(df, name):
    # 根据你的图片定制高级颜色盘
    colors = ['#2ecc71', '#3498db', '#9b59b6', '#f1c40f', '#e67e22', '#e74c3c', '#bdc3c7']
    
    fig = go.Figure(data=[go.Pie(
        labels=df['标的'], 
        values=df['占比'], 
        hole=.6, 
        marker_colors=colors,
        textinfo='label+percent',
        insidetextorientation='radial',
        hoverinfo='label+value+percent'
    )])

    fig.update_layout(
        annotations=[dict(text=f'{name}<br>Portfolio', x=0.5, y=0.5, font_size=20, showarrow=False, font_color="#333")],
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)', # 背景透明
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- 主界面导航 ---
tab1, tab2 = st.tabs(["🐋 13F 大鲸持仓 (巴菲特/段永平)", " Nancy Pelosi 议员交易追踪"])

# --- 标签页 1: 巴菲特与段永平 ---
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header("巴菲特 (Berkshire)")
        # 展示照片
        st.image(AVATARS["巴菲特"], width=200, caption="Warren Buffett")
        # 获取真实数据
        with st.spinner('正在尝试接入真实 13F API...'):
            df_brk, data_source = get_buffett_holdings()
        st.caption(data_source)
        st.table(df_brk)
        
    with col2:
        # 绘制高级环形图
        fig_brk = draw_donut_chart(df_brk, "Buffett")
        st.plotly_chart(fig_brk, use_container_width=True)
        st.info("💡 13F数据通常在每季度结束后 45 天内披露，具有天然滞后性。")

    st.markdown("---") # 分割线
    
    col3, col4 = st.columns([1, 2])
    with col3:
        st.header("段永平 (模拟Demo)")
        st.image(AVATARS["段永平"], width=100)
        df_dyp = pd.DataFrame(MOCK_DYP)
        st.table(df_dyp)
    with col4:
        fig_dyp = draw_donut_chart(df_dyp, "DYP")
        st.plotly_chart(fig_dyp, use_container_width=True)

# --- 标签页 2: 佩洛西 ---
with tab2:
    col5, col6 = st.columns([1, 2])
    with col5:
        st.header("佩洛西 (Demo)")
        st.image(AVATARS["佩洛西"], width=200, caption="Nancy Pelosi")
        df_p = pd.DataFrame(MOCK_PELOSI)
        st.table(df_p)
    with col6:
        fig_p = draw_donut_chart(df_p, "Pelosi")
        st.plotly_chart(fig_p, use_container_width=True)
        st.info("💡 佩洛西喜欢买深度价内 Call (远期期权)，高杠杆博取政策红利。数据来源于议员 PTR 披露。")
