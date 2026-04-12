import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 頁面基本設定
st.set_page_config(page_title="Vibe Coding 台股分析器", layout="wide")
st.title("📈 Vibe Coding - 台股半導體分析儀表板")

# --- 1. 定義初始族群資料 --- [cite: 7, 23]
default_groups = {
    "晶圓代工": ["2330.TW", "2303.TW", "6770.TW"],
    "IC設計": ["2454.TW", "3034.TW", "2379.TW", "3035.TW", "3661.TW"],
    "CoWoS封裝": ["2330.TW", "3711.TW", "3583.TW"]    
}

# --- 2. 數據獲取與處理函數 --- [cite: 6, 22, 24]
@st.cache_data
def load_data(symbol, p):
    try:
        # 為確保滑桿有足夠數據縮放，背景抓取較長區間 [cite: 18, 24]
        df = yf.download(symbol, period="2y", interval="1d")
        if df.empty: return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return None

# --- 3. 側邊欄控制區 --- [cite: 37, 38]
with st.sidebar:
    st.header("⚙️ 全域控制面板")
    
    # 【新增功能】：拖動式時間滑桿控制初始顯示深度 [cite: 24, 42]
    selected_period = st.select_slider(
        "選擇初始分析範圍",
        options=["1mo", "3mo", "6mo", "1y", "2y"],
        value="6mo",
        help="決定載入後預設顯示的時間長度"
    )
    
    st.divider()


# --- 4. 主介面分頁系統 --- [cite: 24, 41]
tab1, tab2 = st.tabs(["🎯 單股深度分析", "⚖️ 多股對比與建議"])

# --- Tab 1: 單股深度分析 --- [cite: 8, 9, 39, 40]
with tab1:
    col_l, col_r = st.columns([1, 3])
    with col_l:
        mode = st.radio("模式", ["產業族群", "自定義輸入"])
        if mode == "產業族群":
            g_name = st.selectbox("選擇族群", list(default_groups.keys()))
            ticker = st.selectbox("選擇股票代號", default_groups[g_name])
        else:
            u_input = st.text_input("輸入代號 (如: 2317)", value="2330")
            ticker = u_input if u_input.endswith((".TW", ".TWO")) else f"{u_input}.TW"

    # 數據獲取
    full_data = load_data(ticker, selected_period)

    if full_data is not None:
        # 根據滑桿選擇過濾顯示數據 [cite: 24]
        period_map = {"1mo": 22, "3mo": 66, "6mo": 132, "1y": 252, "2y": 504}
        data = full_data.tail(period_map[selected_period])

        # K線圖繪製 [cite: 8, 24, 39]
        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'],
            low=data['Low'], close=data['Close'],
            increasing_line_color='red', decreasing_line_color='green'
        )])
        
        # 【優化功能】：加入底部可拖動範圍選擇器 [cite: 24, 41]
        fig.update_layout(
            title=f"{ticker} 互動式 K 線圖 (下方滑桿可自由拖動區間)", 
            template="plotly_white", 
            xaxis_rangeslider_visible=True,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

        # 趨勢判讀結論 [cite: 9, 40]
        st.subheader("💡 專業判讀結論")
        curr_price = data['Close'].iloc[-1]
        ma20 = data['Close'].rolling(window=20).mean().iloc[-1]
        
        if curr_price > ma20:
            st.success(f"【組內結論】{ticker} 目前股價 ({curr_price:.1f}) 高於月線 ({ma20:.1f})，趨勢偏多。")
        else:
            st.warning(f"【組內結論】{ticker} 目前股價 ({curr_price:.1f}) 低於月線 ({ma20:.1f})，短期轉弱。")
    else:
        st.error("無法取得數據。")

# --- Tab 2: 多股對比與建議 --- [cite: 24, 41]
with tab2:
    st.subheader("⚖️ 五股走勢對比 (歸一化分析)")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: t1 = st.text_input("股票 1", "2330", key="t1")
    with c2: t2 = st.text_input("股票 2", "2454", key="t2")
    with c3: t3 = st.text_input("股票 3", "3711", key="t3")
    with c4: t4 = st.text_input("股票 4", "3583", key="t4")
    with c5: t5 = st.text_input("股票 5", "6187", key="t5")
    
    comp_list = [t if t.endswith((".TW", ".TWO")) else f"{t}.TW" for t in [t1, t2, t3, t4, t5]]
    
    if st.button("啟動多股對比分析"):
        # 抓取收盤價進行對比 [cite: 6, 24]
        comp_data = yf.download(comp_list, period=selected_period)['Close']
        if not comp_data.empty:
            # 數據正規化處理 (以第一天為 100%) [cite: 42]
            df_norm = (comp_data / comp_data.iloc[0]) * 100
            
            fig_comp = go.Figure()
            for col in df_norm.columns:
                fig_comp.add_trace(go.Scatter(x=df_norm.index, y=df_norm[col], mode='lines', name=col))
            
            fig_comp.update_layout(title="累積漲跌幅對比 (%)", template="plotly_white")
            st.plotly_chart(fig_comp, use_container_width=True)

            # AI 輔助投資建議 [cite: 11, 40]
            st.write("---")
            st.subheader("🤖 AI 輔助綜合建議")
            returns = ((comp_data.iloc[-1] - comp_data.iloc[0]) / comp_data.iloc[0]) * 100
            cols = st.columns(3)
            for i, tick in enumerate(comp_list):
                with cols[i % 3]:
                    ret = returns[tick]
                    st.metric(tick, f"{comp_data[tick].iloc[-1]:.1f}", f"{ret:.2f}%")
                    if ret > 10: st.write("✅ **表現強勁**：建議續抱。")
                    elif ret > 0: st.write("🟡 **穩健表現**：持股觀望。")
                    else: st.write("❌ **走勢疲軟**：注意風險。")