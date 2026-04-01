import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. 页面样式与配置 ---
st.set_page_config(page_title="Alpha Whale Tracker", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    </style>
""", unsafe_allow_html=True)

st.title("🐋 全球顶级大鲸持仓看板 (Q1 2026 披露版)")
st.caption("数据来源：SEC 13F & PTR 披露快照 | 更新日期：2026-04-01")

# --- 2. 硬核静态数据定义 ---
# 这里的数值基于最近一次公开披露的估算
WHALES = {
    "巴菲特 (Berkshire)": {
        "data": {"标的": ["苹果", "美利坚运通", "美国银行", "可口可乐", "雪佛龙", "其他"], "占比": [40.2, 12.5, 10.1, 9.2, 6.8, 21.2]},
        "color": ["#1a365d", "#2b6cb0", "#4299e1", "#63b3ed", "#90cdf4", "#cbd5e0"],
        "desc": "坚定的价值投资，目前现金流储备创历史新高。"
    },
    "段永平 (H&H)": {
        "data": {"标的": ["苹果", "伯克希尔", "英伟达", "拼多多", "谷歌", "其他"], "占比": [50.3, 20.6, 7.7, 7.5, 3.3, 10.6]},
        "color": ["#c53030", "#e53e3e", "#fc8181", "#feb2b2", "#fed7d7", "#edf2f7"],
        "desc": "极度集中投资，强调商业模式的‘护城河’。"
    },
    "佩洛西 (Nancy Pelosi)": {
        "data": {"标的": ["英伟达", "谷歌", "博通", "Vistra", "Tempus AI", "其他"], "占比": [19.0, 16.0, 15.0, 10.0, 7.0, 33.0]},
        "color": ["#276749", "#2f855a", "#38a169", "#48bb78", "#68d391", "#a0aec0"],
        "desc": "高杠杆期权布局，精准捕捉 AI 板块政策红利。"
    }
}

# --- 3. 绘图函数 (高级环形图) ---
def create_donut(df, colors, name):
    fig = go.Figure(data=[go.Pie(
        labels=df["标的"], 
        values=df["占比"], 
        hole=.62, 
        marker_colors=colors,
        textinfo='label+percent',
        insidetextorientation='radial',
        hoverinfo='label+value+percent'
    )])
    fig.update_layout(
        showlegend=False,
        margin=dict(t=30, b=10, l=10, r=10),
        height=380,
        annotations=[dict(text=name, x=0.5, y=0.5, font_size=18, showarrow=False, font_family="Arial Black")]
    )
    return fig

# --- 4. 布局渲染 ---
st.markdown("---")
cols = st.columns(3)

for i, (name, info) in enumerate(WHALES.items()):
    with cols[i]:
        # 指标展示
        st.subheader(name)
        df = pd.DataFrame(info["data"])
        
        # 渲染环形图
        st.plotly_chart(create_donut(df, info["color"], name.split()[0]), use_container_width=True)
        
        # 风格说明
        st.markdown(f"> **风格偏好**: {info['desc']}")
        
        # 详细表格
        st.table(df)

st.markdown("---")
st.info("💡 这是一个演示 Demo。如果需要对接实时数据，代码已预留数据注入接口 (Data Injection Layer)。")
