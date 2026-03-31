import streamlit as st
import yfinance as yf
import pandas as pd
import akshare as ak
import plotly.express as px
import plotly.graph_objects as go

# --- 页面配置 ---
st.set_page_config(page_title="Whale Tracker & Market Pulse", layout="wide")
st.title("📊 投资大鲸追踪 & 市场折溢价看板")

# --- 模拟数据：大佬持仓 (用于简历演示) ---
WHALE_DATA = {
    "段永平 (H&H)": {"AAPL": 50.3, "BRK.B": 20.6, "NVDA": 7.7, "PDD": 7.5, "GOOGL": 3.3, "其他": 10.6},
    "佩洛西 (Nancy Pelosi)": {"NVDA": 19.0, "GOOGL": 16.0, "AVGO": 15.0, "VST": 10.0, "TEM": 7.0, "其他": 33.0},
    "巴菲特 (Berkshire)": {"AAPL": 40.2, "AXP": 12.5, "BAC": 10.1, "KO": 9.2, "CVX": 6.8, "其他": 21.2}
}

# --- 1. 大佬持仓追踪模块 ---
def render_whale_tab():
    st.header("🐋 全球大佬最新持仓观察")
    selected_whale = st.selectbox("选择要观察的持仓对象", list(WHALE_DATA.keys()))
    
    data = WHALE_DATA[selected_whale]
    df_whale = pd.DataFrame(list(data.items()), columns=['标的', '仓位占比'])
    
    col1, col2 = st.columns([1, 1])
    with col1:
        # 模仿你图片里的饼图
        fig = px.pie(df_whale, values='仓位占比', names='标', 
                     title=f"{selected_whale} 核心持仓分布",
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💡 风格总结")
        if "佩洛西" in selected_whale:
            st.markdown("""
            - **“期权女王”**：偏好远期深度价内 Call，高杠杆博取政策红利。
            - **行业聚焦**：高度集中于算力 (NVDA) 和 生物科技。
            """)
        elif "段永平" in selected_whale:
            st.markdown("""
            - **“中国巴菲特”**：极度集中于苹果和具备长效护城河的公司。
            - **现金奶牛**：偏好分红稳定且有强劲现金流的商业模式。
            """)
        st.table(df_whale)

# --- 2. ETF 溢价与限购模块 ---
def render_etf_tab():
    st.header("🎯 跨境 ETF 折溢价 & 限购追踪")
    
    try:
        # 获取 ETF 数据
        df_etf = ak.fund_etf_spot_em()
        targets = ["159612", "513100", "513050", "159941", "513500"] # 核心标的 ID
        
        # 筛选出我们关注的纳指/标普标的
        res = df_etf[df_etf['代码'].isin(targets)].copy()
        
        # 模拟“限购额度”和“申购状态” (因为接口不直接返回，我们根据经验模拟展示)
        res['申购状态'] = ["暂停申购", "限额 100元", "开放申购", "限额 1000元", "暂停申购"]
        res['溢价率'] = -res['折价率'] # 溢价 = -折价
        
        # 样式美化
        def highlight_premium(val):
            color = 'red' if val > 2 else 'green' if val < 0 else 'black'
            return f'color: {color}'

        st.dataframe(res[['代码', '基金简称', '最新价', '溢价率', '申购状态']].style.applymap(highlight_premium, subset=['溢价率']))
        
        # 绘制溢价率对比图
        fig = px.bar(res, x='基金简称', y='溢价率', color='溢价率',
                     title="热门跨境 ETF 溢价率对比",
                     color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"数据加载失败: {e}")

# --- 3. 原有 NVDA/TSLA 策略模块 ---
def render_strategy_tab():
    st.header("🤖 个股量化策略执行")
    # 此处放入你之前的 app.py 核心逻辑代码...
    st.info("此处显示原有的 NVDA/TSLA 均线切换逻辑...")

# --- 主界面导航 ---
tab1, tab2, tab3 = st.tabs(["🐋 大佬持仓", "🎫 ETF 溢价/限购", "📉 个股策略"])

with tab1:
    render_whale_tab()
with tab2:
    render_etf_tab()
with tab3:
    render_strategy_tab()