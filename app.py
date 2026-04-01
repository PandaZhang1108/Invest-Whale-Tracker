import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. 科技感 CSS 注入 (磨砂玻璃效果) ---
st.set_page_config(page_title="Alpha Whale Tracker", layout="wide")

st.markdown("""
    <style>
    .main { 
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
        font-family: 'SF Pro Display', -apple-system, sans-serif;
    }
    
    /* 科技感磨砂玻璃卡片 */
    .tech-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 28px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        margin-bottom: 20px;
    }
    
    .holding-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    .logo-img {
        width: 28px; height: 28px; border-radius: 6px; margin-right: 12px;
    }
    
    .company-name { font-weight: 500; color: #1d1d1f; font-size: 14px; }
    .percent-tag { 
        background: rgba(0, 102, 204, 0.1); 
        color: #0066cc; 
        padding: 2px 8px; 
        border-radius: 6px; 
        font-size: 12px; 
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 前十大持仓数据 (最新披露静态快照) ---
WHALE_TOP10 = {
    "巴菲特 (Berkshire)": [
        {"n": "苹果", "d": "apple.com", "p": 40.2}, {"n": "美国运通", "d": "americanexpress.com", "p": 12.5},
        {"n": "美国银行", "d": "bankofamerica.com", "p": 10.1}, {"n": "可口可乐", "d": "cocacola.com", "p": 9.2},
        {"n": "雪佛龙", "d": "chevron.com", "p": 6.8}, {"n": "西方石油", "d": "oxy.com", "p": 4.5},
        {"n": "卡夫亨氏", "d": "kraftheinzcompany.com", "p": 3.8}, {"n": "穆迪", "d": "moodys.com", "p": 2.5},
        {"n": "安达保险", "d": "chubb.com", "p": 2.1}, {"n": "克罗格", "d": "kroger.com", "p": 1.1}
    ],
    "佩洛西 (Nancy Pelosi)": [
        {"n": "英伟达", "d": "nvidia.com", "p": 19.0}, {"n": "谷歌", "d": "google.com", "p": 16.0},
        {"n": "博通", "d": "broadcom.com", "p": 15.0}, {"n": "Vistra", "d": "vistracorp.com", "p": 10.0},
        {"n": "Tempus AI", "d": "tempus.com", "p": 7.0}, {"n": "派拓网络", "d": "paloaltonetworks.com", "p": 7.0},
        {"n": "亚马逊", "d": "amazon.com", "p": 6.0}, {"n": "CrowdStrike", "d": "crowdstrike.com", "p": 4.0},
        {"n": "微软", "d": "microsoft.com", "p": 3.0}, {"n": "其他", "d": "tesla.com", "p": 13.0}
    ],
    "段永平 (H&H)": [
        {"n": "苹果", "d": "apple.com", "p": 50.3}, {"n": "伯克希尔", "d": "berkshirehathaway.com", "p": 20.6},
        {"n": "英伟达", "d": "nvidia.com", "p": 7.7}, {"n": "拼多多", "d": "pinduoduo.com", "p": 7.5},
        {"n": "谷歌", "d": "google.com", "p": 3.3}, {"n": "微软", "d": "microsoft.com", "p": 2.5},
        {"n": "Meta", "d": "meta.com", "p": 2.1}, {"n": "特斯拉", "d": "tesla.com", "p": 1.8},
        {"n": "阿里巴巴", "d": "alibaba.com", "p": 1.5}, {"n": "腾讯", "d": "tencent.com", "p": 1.2}
    ]
}

# --- 3. 渲染逻辑 ---
cols = st.columns(3)
for i, (name, holdings) in enumerate(WHALE_TOP10.items()):
    with cols[i]:
        st.markdown(f'<div class="tech-card">', unsafe_allow_html=True)
        st.subheader(name)
        
        # 顶部总览图
        df = pd.DataFrame(holdings)
        fig = go.Figure(data=[go.Pie(labels=df['n'], values=df['p'], hole=.75)])
        fig.update_layout(showlegend=False, height=180, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # 循环渲染前 10 大
        for h in holdings:
            logo = f"https://logo.clearbit.com/{h['d']}"
            st.markdown(f"""
                <div class="holding-row">
                    <div style="display:flex; align-items:center;">
                        <img src="{logo}" class="logo-img" onerror="this.src='https://www.google.com/s2/favicons?domain={h['d']}'">
                        <span class="company-name">{h['n']}</span>
                    </div>
                    <span class="percent-tag">{h['p']}%</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
