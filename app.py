import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. Apple 风格 CSS 注入 ---
st.set_page_config(page_title="Alpha Whale Portfolio", layout="wide")

st.markdown("""
    <style>
    /* 全局背景与字体 */
    .main { background-color: #F5F5F7; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    
    /* 苹果风格卡片容器 */
    .whale-card {
        background-color: white;
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        margin-bottom: 30px;
        border: 1px solid #f0f0f0;
    }
    
    /* Logo 样式 */
    .company-logo {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        object-fit: contain;
        margin-right: 12px;
    }
    
    /* 公司列表行 */
    .holding-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #F5F5F7;
    }
    
    .company-info { display: flex; align-items: center; }
    .company-name { font-weight: 500; font-size: 16px; color: #1D1D1F; }
    .percentage { font-weight: 600; color: #86868B; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 增强版数据源 (增加域名用于获取Logo) ---
WHALES = {
    "巴菲特 (Berkshire)": [
        {"name": "苹果", "domain": "apple.com", "percent": 40.2},
        {"name": "美国运通", "domain": "americanexpress.com", "percent": 12.5},
        {"name": "美国银行", "domain": "bankofamerica.com", "percent": 10.1},
        {"name": "可口可乐", "domain": "cocacola.com", "percent": 9.2},
    ],
    "段永平 (H&H)": [
        {"name": "苹果", "domain": "apple.com", "percent": 50.3},
        {"name": "伯克希尔", "domain": "berkshirehathaway.com", "percent": 20.6},
        {"name": "英伟达", "domain": "nvidia.com", "percent": 7.7},
        {"name": "拼多多", "domain": "pinduoduo.com", "percent": 7.5},
    ],
    "佩洛西 (Nancy Pelosi)": [
        {"name": "英伟达", "domain": "nvidia.com", "percent": 19.0},
        {"name": "谷歌", "domain": "google.com", "percent": 16.0},
        {"name": "博通", "domain": "broadcom.com", "percent": 15.0},
        {"name": "Vistra", "domain": "vistracorp.com", "percent": 10.0},
    ]
}

st.title(" Alpha Whale Insight")
st.markdown("### 追踪顶级智囊的资本足迹")

# --- 3. 渲染函数 ---
def render_holding_row(name, domain, percent):
    # 使用 Clearbit API 获取 Logo
    logo_url = f"https://logo.clearbit.com/{domain}"
    st.markdown(f"""
        <div class="holding-row">
            <div class="company-info">
                <img src="{logo_url}" class="company-logo" onerror="this.src='https://cdn-icons-png.flaticon.com/512/684/684908.png'">
                <span class="company-name">{name}</span>
            </div>
            <span class="percentage">{percent}%</span>
        </div>
    """, unsafe_allow_html=True)

# --- 4. 布局渲染 ---
cols = st.columns(3)

for i, (whale_name, holdings) in enumerate(WHALES.items()):
    with cols[i]:
        st.markdown(f'<div class="whale-card">', unsafe_allow_html=True)
        st.subheader(whale_name)
        
        # 绘制迷你环形图
        df = pd.DataFrame(holdings)
        fig = go.Figure(data=[go.Pie(labels=df['name'], values=df['percent'], hole=.7)])
        fig.update_layout(showlegend=False, height=200, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # 渲染公司列表（带Logo）
        for item in holdings:
            render_holding_row(item['name'], item['domain'], item['percent'])
            
        st.markdown('</div>', unsafe_allow_html=True)
