import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd

# --- 0. 頁面基本設定 ---
st.set_page_config(page_title="Vibe Coding 台股分析器", layout="wide")
st.title("📈 Vibe Coding - 台股半導體分析儀表板")

# --- 1. 定義初始族群資料 ---
default_groups = {
    "晶圓代工": ["2330.TW", "2303.TW", "6770.TW"],
    "IC設計": ["2454.TW", "3034.TW", "2379.TW", "3035.TW", "3661.TW"],
    "CoWoS封裝": ["2330.TW", "3711.TW", "3583.TW"]    
}

# --- 2. 數據獲取與處理函數 ---
@st.cache_data
def load_data(symbol, p):
    try:
        # 抓取較長區間確保計算指標穩定
        df = yf.download(symbol, period="2y", interval="1d")
        if df.empty: return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return None

# --- 3. 側邊欄控制區 ---
with st.sidebar:
    st.header("⚙️ 全域控制面板")
    
    # 拖動式時間滑桿控制
    selected_period = st.select_slider(
        "選擇分析範圍",
        options=["1mo", "3mo", "6mo", "1y", "2y"],
        value="6mo",
        help="決定載入後預設顯示的時間長度"
    )
    st.divider()
    st.info("💡 提示：在多股分析中，系統會自動對齊時間軸。")


# --- 4. 主介面分頁系統 ---
tab1, tab2 = st.tabs(["🎯 單股深度分析", "⚖️ 多股對比與建議"])

# --- Tab 1: 單股深度分析 ---
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

    full_data = load_data(ticker, selected_period)

    if full_data is not None:
        period_map = {"1mo": 22, "3mo": 66, "6mo": 132, "1y": 252, "2y": 504}
        data = full_data.tail(period_map[selected_period])

        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'],
            low=data['Low'], close=data['Close'],
            increasing_line_color='red', decreasing_line_color='green'
        )])
        
        fig.update_layout(
            title=f"{ticker} 互動式 K 線圖", 
            template="plotly_white", 
            xaxis_rangeslider_visible=True,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("💡 專業判讀結論")
        curr_price = data['Close'].iloc[-1]
        ma20 = data['Close'].rolling(window=20).mean().iloc[-1]
        
        if curr_price > ma20:
            st.success(f"【結論】{ticker} 股價 ({curr_price:.1f}) 高於月線 ({ma20:.1f})，趨勢偏多。")
        else:
            st.warning(f"【結論】{ticker} 股價 ({curr_price:.1f}) 低於月線 ({ma20:.1f})，短期轉弱。")
    else:
        st.error("無法取得數據。")

# --- Tab 2: 多股對比與建議 ---
with tab2:
    st.subheader("⚖️ 多股深度走勢對比")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: t1 = st.text_input("股票 1", "2330", key="t1")
    with c2: t2 = st.text_input("股票 2", "2454", key="t2")
    with c3: t3 = st.text_input("股票 3", "3711", key="t3")
    with c4: t4 = st.text_input("股票 4", "3583", key="t4")
    with c5: t5 = st.text_input("股票 5", "6770", key="t5")
    
    comp_list = [t if t.endswith((".TW", ".TWO")) else f"{t}.TW" for t in [t1, t2, t3, t4, t5]]
    
    if st.button("啟動多股深度對比分析"):
        with st.spinner("正在獲取多股數據..."):
            # 下載完整 OHLC 數據
            comp_full_data = yf.download(comp_list, period=selected_period)
            
            if not comp_full_data.empty:
                # --- 1. 繪製多股 K 線子圖 ---
                fig_multi_k = sp.make_subplots(
                    rows=5, cols=1, 
                    shared_xaxes=True, 
                    vertical_spacing=0.03,
                    subplot_titles=[f"{tick} K線走勢" for tick in comp_list]
                )

                for i, tick in enumerate(comp_list):
                    try:
                        # 從 MultiIndex 中提取單一股價數據
                        tick_df = pd.DataFrame({
                            'Open': comp_full_data['Open'][tick],
                            'High': comp_full_data['High'][tick],
                            'Low': comp_full_data['Low'][tick],
                            'Close': comp_full_data['Close'][tick]
                        }).dropna()
                        
                        fig_multi_k.add_trace(
                            go.Candlestick(
                                x=tick_df.index,
                                open=tick_df['Open'], high=tick_df['High'],
                                low=tick_df['Low'], close=tick_df['Close'],
                                name=tick,
                                increasing_line_color='red', decreasing_line_color='green',
                                showlegend=False
                            ),
                            row=i+1, col=1
                        )
                    except Exception as e:
                        st.error(f"無法載入 {tick} 的 K 線數據")

                fig_multi_k.update_layout(
                    height=1200, 
                    title_text="多股垂直對比 K 線圖 (同步時間軸)",
                    xaxis_rangeslider_visible=False, 
                    template="plotly_white"
                )
                st.plotly_chart(fig_multi_k, use_container_width=True)

                # --- 2. 歸一化漲跌幅對比 ---
                st.write("---")
                st.subheader("📈 累積漲跌幅對比 (%)")
                close_data = comp_full_data['Close']
                # 正規化處理 (以首日為 100%)
                df_norm = (close_data / close_data.iloc[0].ffill()) * 100
                
                fig_comp = go.Figure()
                for col in df_norm.columns:
                    fig_comp.add_trace(go.Scatter(x=df_norm.index, y=df_norm[col], mode='lines', name=col))
                
                fig_comp.update_layout(
                    title="歸一化走勢 (基準點=100)", 
                    template="plotly_white",
                    hovermode="x unified"
                )
                st.plotly_chart(fig_comp, use_container_width=True)

                # --- 3. AI 輔助投資建議 ---
                st.write("---")
                st.subheader("🤖 AI 輔助綜合建議")
                # 計算該期間報酬率
                returns = ((close_data.iloc[-1] - close_data.iloc[0]) / close_data.iloc[0]) * 100
                cols = st.columns(3)
                for i, tick in enumerate(comp_list):
                    with cols[i % 3]:
                        try:
                            ret = returns[tick]
                            last_p = close_data[tick].iloc[-1]
                            st.metric(tick, f"{last_p:.1f}", f"{ret:.2f}%")
                            if ret > 10: st.write("✅ **表現強勁**：趨勢優於大盤。")
                            elif ret > 0: st.write("🟡 **穩健表現**：目前呈現震盪小漲。")
                            else: st.write("❌ **走勢疲軟**：建議檢查基本面支撐。")
                        except:
                            st.write(f"數據計算錯誤: {tick}")
            else:
                st.error("無法取得多股數據，請檢查代號是否正確。")
