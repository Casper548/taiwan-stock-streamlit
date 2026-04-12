Vibe Coding台股 AI 分析儀表板

##專案目標
使用生成式 AI 與 Python 建立台股半導體分析工具

##功能
- 單股 K 線分析
- 均線判斷
- 多股比較
- AI 投資建議
  
##使用技術
- Python
- Streamlit
- yfinance
- Plotly
- Pandas

##如何執行

pip install -r requirements.txt  
streamlit run all.py

##AI工具鏈整合與任務執行紀錄

本專案以生成式AI ChatGPT作為主要開發輔助工具，負責整體系統設計、程式生成與錯誤修正

##任務分工與 AI 應用紀錄

系統架構設計
使用 ChatGPT 協助設計整體 Streamlit 架構
-規劃三大模組：
-單股分析模組
-多股比較模組
-技術指標判斷模組

##程式碼生成

透過 AI 生成以下核心功能：
-使用 yfinance 抓取台股資料
-使用 Plotly 繪製 K 線圖（Candlestick）
-計算 MA20 移動平均線
-多股票 normalized 比較（以 100 為基準）

##除錯與優化

AI 協助解決以下問題：
-Git 初始化與 push 錯誤（remote / branch 問題）
-Python 套件缺失（streamlit / plotly）
-yfinance 資料格式（MultiIndex 處理）

##使用環境與工具

開發IDE:VSCode
AI 工具:ChatGPT
執行環境:Python 3.x
資料來源:yfinance
視覺化:Plotly
UI 框架:Streamlit
版本控制:Git + GitHub

##Vibe Coding 工作流程

1.以自然語言描述需求（例如：做K線圖分析）
2.AI 生成初版程式碼
3.本地執行測試（Streamlit）
4.錯誤回報給 AI 修正
5.重複優化直到可運行
6.Git commit / push 版本控制

##K線圖繪製與專業數據分析

分析方法:
本系統使用以下技術進行分析：
-K 線圖（Candlestick）顯示價格變化
-20日移動平均線（MA20）判斷趨勢
-收盤價相對均線位置判斷多空

##趨勢判讀規則

當股價 > MA20 → 短期偏多趨勢 
當股價 < MA20 → 短期偏空趨勢 

##組內最終結論

台股半導體族群波動性較高
權值股（如 2330）具有較強支撐性
短期交易可依 MA20 判斷進出方向
本系統可作為初步技術分析輔助工具

##Vibe Coding 流程優化與創新

1. 流程簡化設計
透過 AI 協作，大幅減少傳統開發流程：
-無需手刻完整架構
-直接由自然語言生成程式碼
-即時修正錯誤

2. Prompt 優化方式
使用以下 prompt 策略：
-明確指定功能（例如：K線圖 + MA20）
-分段請求（資料 / UI / 分析分開生成）
-逐步優化而非一次生成完整系統

3.創新點
AI 自動生成金融分析邏輯
多股票標準化比較（Normalization）
即時互動式視覺化分析
將 AI 作為「開發協作者」而非工具
