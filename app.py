# 在 app.py 循环中
st.markdown(f"#### {whale_name} 持仓明细")
df_display = pd.DataFrame(holdings)

# 像专业软件一样格式化金额
df_display['市值'] = df_display['value_usd'].apply(lambda x: f"${x:,.0f}")
df_display['权重'] = df_display['percent'].apply(lambda x: f"{x}%")

# 使用 Streamlit 的高级表格组件
st.dataframe(
    df_display[['company', '市值', '权重']], 
    hide_index=True,
    use_container_width=True
)
