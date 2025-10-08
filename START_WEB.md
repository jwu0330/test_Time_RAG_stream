# 🌐 Web 界面啟動指南

## 快速啟動

### 1. 安裝依賴（如果尚未安裝）

```bash
pip install -r requirements.txt
```

### 2. 啟動後端 API 服務器

```bash
python web_api.py
```

服務器將在 `http://localhost:8000` 啟動

### 3. 打開前端界面

在瀏覽器中打開 `web_interface.html` 文件：

```bash
# 方法 1: 直接打開文件
open web_interface.html  # macOS
xdg-open web_interface.html  # Linux
start web_interface.html  # Windows

# 方法 2: 使用 Python 簡單 HTTP 服務器
python -m http.server 8080
# 然後訪問 http://localhost:8080/web_interface.html
```

## 使用說明

### 界面功能

1. **輸入問題**
   - 在文本框中輸入您的問題
   - 支持 Ctrl+Enter 快捷鍵提交

2. **查看結果**
   - **最終答案**: 系統生成的完整回答
   - **四向度分析**: 
     - D1: 知識點數量（零個/一個/多個）
     - D2: 表達錯誤（有錯誤/無錯誤）
     - D3: 表達詳細度（非常詳細/粗略/未談及重點）
     - D4: 重複詢問（重複狀態/正常狀態）
   - **匹配的知識點**: 顯示相關的知識領域
   - **時間分析報告**: 各階段的精準執行時間（後端計時）

### 時間報告說明

**重要**: 顯示的時間是**後端實際運作時間**，不包含：
- 前端渲染時間
- 網絡傳輸延遲
- 瀏覽器處理時間

這確保了時間分析的精準性，您看到的是系統真實的處理效能。

## API 端點

### 查詢端點
```
POST /api/query
```

請求體：
```json
{
  "query": "什麼是機器學習？",
  "scenario_ids": null,
  "auto_classify": true
}
```

響應：
```json
{
  "query": "什麼是機器學習？",
  "final_answer": "...",
  "dimensions": {
    "D1": "一個",
    "D2": "無錯誤",
    "D3": "粗略",
    "D4": "正常狀態"
  },
  "time_report": {
    "stages": {
      "RAG檢索": 0.718,
      "四向度分類": 1.234,
      ...
    },
    "total_time": 6.340
  }
}
```

### 歷史記錄端點
```
GET /api/history?limit=10
```

### 配置端點
```
GET /api/config
```

### 四向度定義端點
```
GET /api/dimensions
```

## API 文檔

啟動服務器後，訪問以下 URL 查看完整 API 文檔：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 故障排除

### 問題 1: 無法連接到 API

**解決方案**:
1. 確認後端服務器正在運行
2. 檢查端口 8000 是否被占用
3. 查看控制台錯誤信息

### 問題 2: CORS 錯誤

**解決方案**:
如果直接打開 HTML 文件遇到 CORS 問題，使用 HTTP 服務器：
```bash
python -m http.server 8080
```

### 問題 3: API Key 錯誤

**解決方案**:
確保已設定 OPENAI_API_KEY 環境變量：
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 配置修改

### 修改 API 端口

編輯 `config.py`:
```python
API_PORT = 8000  # 改為您想要的端口
```

### 修改模型

編輯 `config.py`:
```python
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-3.5-turbo"
CLASSIFIER_MODEL = "gpt-3.5-turbo"
```

### 修改歷史記錄數量

編輯 `config.py`:
```python
HISTORY_SIZE = 10  # 改為您想要的數量
```

## 進階使用

### 使用 curl 測試 API

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "什麼是深度學習？", "auto_classify": true}'
```

### 使用 Python 調用 API

```python
import requests

response = requests.post(
    "http://localhost:8000/api/query",
    json={
        "query": "什麼是機器學習？",
        "auto_classify": True
    }
)

result = response.json()
print(f"答案: {result['final_answer']}")
print(f"總耗時: {result['time_report']['total_time']}s")
```

## 生產部署建議

1. **使用 Gunicorn 或 uWSGI**
```bash
gunicorn web_api:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **配置 Nginx 反向代理**

3. **使用 Docker 容器化**

4. **設定環境變量**
   - 不要在代碼中硬編碼 API Key
   - 使用 .env 文件或環境變量

5. **啟用 HTTPS**

---

**享受使用 RAG 流式系統！** 🚀
