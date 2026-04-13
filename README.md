# 台股半導體分析工具（AI + Python）

## 專案簡介
本專案結合生成式 AI（ChatGPT）與 Python，打造一個互動式台股半導體分析工具，協助使用者快速進行技術分析與投資判斷。

透過簡潔的 UI 與即時數據，使用者可以輕鬆完成：
- 單股技術分析
- 多股比較
- 趨勢判讀
- AI 投資建議

---

## 專案目標
建立一套具備以下能力的分析系統：
- 自動抓取台股資料
- 視覺化 K 線圖
- 技術指標分析（MA20）
- AI 輔助投資決策

---

## 核心功能

### 單股分析
- K 線圖（Candlestick）
- 20 日均線（MA20）
- 趨勢判斷（多 / 空）

###多股比較
- 多檔股票同時分析
- Normalization（基準 = 100）
- 績效對比

### 技術分析
- 均線判斷
- 價格 vs MA20 關係

###AI 投資建議
- 根據趨勢自動生成建議
- 提供簡易判讀結果

---

##使用技術

| 類別 | 技術 |
|------|------|
| 語言 | Python |
| UI | Streamlit |
| 資料來源 | yfinance |
| 視覺化 | Plotly |
| 資料處理 | Pandas |
| AI | ChatGPT |
| 版本控制 | Git + GitHub |

---

## 💻 環境需求
- 作業系統：Windows 10 / 11  
- Python：3.12  
- 開發工具：VSCode  

---

## 📦 安裝方式
```bash
pip install -r requirements.txt
```


<img width="2560" height="1528" alt="螢幕擷取畫面 2026-04-13 141020" src="https://github.com/user-attachments/assets/16748eea-0d21-407b-9d1c-227e858a34cf" />

<img width="2560" height="1528" alt="螢幕擷取畫面 2026-04-13 140836" src="https://github.com/user-attachments/assets/fff14a81-0b4d-48ff-a8f1-33a785857e20" />
