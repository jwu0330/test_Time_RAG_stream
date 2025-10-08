# Web 界面

RAG 流式系統的互動式 Web 界面

---

## 📁 文件結構

```
web/
├── index.html          # 主界面 HTML
├── app.js              # JavaScript 邏輯
└── README.md           # 本文件
```

---

## 🚀 使用方式

### 步驟 1：啟動後端 API

```bash
# 回到專案根目錄
cd ..

# 設定 API Key
export OPENAI_API_KEY="your-key"

# 啟動 API
python3 web_api.py
```

### 步驟 2：打開 Web 界面

```bash
# 方式 A：直接打開
open web/index.html

# 方式 B：使用瀏覽器
# 在瀏覽器中輸入：
file:///home/jim/code/python/test_Time_RAG_stream/web/index.html
```

---

## ✨ 功能特色

- ✅ 即時對話界面
- ✅ 四向度分類顯示
- ✅ 響應時間統計
- ✅ 範例問題快速開始
- ✅ 側邊欄系統資訊
- ✅ 響應式設計（支援手機）

---

## 🎯 範例問題

1. 什麼是機器學習？
2. 深度學習和機器學習有什麼不同？
3. 請詳細解釋 Transformer 架構

---

## 🔧 配置

如果 API 在不同端口，編輯 `app.js`：

```javascript
const API_BASE = 'http://localhost:8000';  // 修改這裡
```

---

## 📊 API 端點

界面使用以下 API 端點：

- `GET /api/health` - 健康檢查
- `POST /api/query` - 發送查詢

---

## 🐛 故障排除

### 無法連接到 API

確保後端正在運行：
```bash
python3 web_api.py
```

### CORS 錯誤

API 已配置 CORS，應該不會有問題。

---

## 📱 響應式設計

- 桌面：顯示側邊欄
- 手機：隱藏側邊欄，全屏聊天

---

**享受你的 Web 界面！** 🎉
