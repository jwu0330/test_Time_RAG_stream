# 快速開始指南

**⏱️ 預計時間**: 5 分鐘  
**📅 更新日期**: 2025-10-15  
**✅ 系統版本**: 3.0（K/C/R 三維度分類系統）  
**🔧 環境管理**: Poetry（推薦）

---

## 🚀 三步驟快速啟動

### 步驟 1：安裝依賴（1分鐘）

```bash
# 使用 Poetry 安裝依賴（自動管理虛擬環境）
poetry install
```

**依賴列表**：
- openai >= 1.54.0
- numpy >= 1.24.0
- fastapi >= 0.104.0
- uvicorn >= 0.24.0
- pydantic >= 2.0.0
- python-dotenv >= 1.0.0

**注意**：如果沒有安裝 Poetry，請先安裝：
```bash
# 安裝 Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 或使用 pip
pip install --user poetry
```

### 步驟 2：設定 API Key（1分鐘）

```bash
# 設定環境變數
export OPENAI_API_KEY="your-api-key-here"
```

或創建 `.env` 文件：
```bash
cp .env.example .env
nano .env
# 添加：OPENAI_API_KEY=your-api-key-here
```

### 步驟 3：運行系統（2分鐘）

```bash
# 方式 A：運行主程序
poetry run python main_parallel.py

# 方式 B：啟動 Web 界面
poetry run python web_api.py
# 然後在瀏覽器打開 web/index.html

# 方式 C：進入 Poetry Shell（推薦）
poetry shell
python main_parallel.py
```

---

## ✅ 驗證安裝

### 檢查系統健康

```bash
# 檢查 Python 版本（需要 >= 3.8）
python3 --version

# 檢查 Poetry 版本
poetry --version

# 檢查依賴是否安裝
poetry show | grep -E "openai|fastapi|numpy"

# 檢查 API Key
echo $OPENAI_API_KEY
```

### 預期輸出

**首次啟動**（10-15秒）：
```
🚀 RAG 系統已初始化（K, C, R 三維度分類）

📚 初始化文件向量...
⚠️  首次啟動，需要調用 OpenAI API 生成向量
⏳ 預計需要 10-15 秒，請稍候...
  📄 載入: ml_basics.txt
  📄 載入: deep_learning.txt
  📄 載入: nlp_intro.txt
✅ 已向量化並保存

🔍 處理查詢: 什麼是機器學習？
✅ 並行處理完成（耗時: 0.312s）
```

**第二次啟動**（2-3秒）：
```
🚀 雙線程 RAG 系統已初始化

📚 初始化文件向量...
✅ 已載入 3 個向量
✅ 使用已儲存的向量（快速啟動）
```

---

## 🎯 快速測試

### 測試命令行版本

```bash
poetry run python main_parallel.py

# 或先進入 shell
poetry shell
python main_parallel.py
```

**測試問題**：
1. "什麼是機器學習？"
2. "深度學習和機器學習有什麼區別？"

### 測試 Web 版本

```bash
# 1. 啟動後端
poetry run python web_api.py

# 2. 打開前端（新開終端或瀏覽器）
open web/index.html
# 或訪問: file:///path/to/web/index.html
```

**驗證功能**：
- ✅ 可以輸入問題
- ✅ 顯示 K/C/R 三維度分類
- ✅ 顯示響應時間
- ✅ 顯示匹配的文檔

---

## 📊 系統概覽

### 核心功能

| 功能 | 說明 |
|------|------|
| **RAG 檢索** | 向量搜索匹配相關教材 |
| **K/C/R 三維度分類** | K(知識點數量)、C(正確性)、R(重複性) |
| **12種情境** | 根據 K/C/R 自動匹配情境 |
| **並行處理** | 3個API同時執行（RAG + C值 + 知識點檢測） |
| **精確計時** | 獨立追蹤每個階段的執行時間 |

### 文件結構

```
test_Time_RAG_stream/
├── main_parallel.py        # 主程序（命令行版本）
├── web_api.py              # Web API 後端
├── config.py               # 系統配置
│
├── core/                   # 核心模組
│   ├── vector_store.py     # 向量存儲
│   ├── rag_module.py       # RAG 檢索
│   ├── scenario_classifier.py  # 情境分類（24種）
│   ├── ontology_manager.py     # 本體論管理
│   ├── history_manager.py      # 歷史管理
│   └── timer_utils.py          # 雙線程計時
│
├── data/                   # 數據文件
│   ├── docs/              # 教材（3個 .txt）
│   ├── scenarios/         # 情境配置
│   └── ontology/          # 知識本體論
│
└── web/                    # Web 前端
    ├── index.html         # 主界面
    └── app.js             # JavaScript
```

---

## 🔧 常見問題

### Q1: ModuleNotFoundError

**問題**：`ModuleNotFoundError: No module named 'openai'`

**解決**：
```bash
# 使用 Poetry 安裝依賴
poetry install

# 確保使用 Poetry 運行
poetry run python main_parallel.py
```

### Q2: API Key 錯誤

**問題**：`AuthenticationError: Invalid API key`

**解決**：
```bash
export OPENAI_API_KEY="sk-your-actual-key"
```

### Q3: 首次啟動很慢

**原因**：需要調用 OpenAI API 生成向量（正常現象）

**解決**：等待完成，之後會自動保存到 `vectors.pkl`，第二次啟動只需 2-3 秒

### Q4: Web 界面無法連接

**檢查**：
```bash
# 確認 API 正在運行
curl http://localhost:8000/api/health
```

**解決**：確保 `python3 web_api.py` 正在運行

---

## 📖 下一步

### 了解更多

- **完整系統說明**: [10_SYSTEM_OVERVIEW.md](10_SYSTEM_OVERVIEW.md)
- **詳細安裝指南**: [02_INSTALLATION.md](02_INSTALLATION.md)
- **命令參考**: [20_COMMAND_REFERENCE.md](20_COMMAND_REFERENCE.md)
- **Web 界面指南**: [21_WEB_INTERFACE.md](21_WEB_INTERFACE.md)

### 自定義配置

- **修改教材**: 編輯 `data/docs/` 中的 .txt 文件
- **調整模型**: 修改 `config.py` 中的 `LLM_MODEL`
- **自定義情境**: 編輯 `data/scenarios/scenarios_12.json`

### 故障排除

遇到問題？查看：[31_TROUBLESHOOTING.md](31_TROUBLESHOOTING.md)

---

## 🎉 完成！

恭喜！您的 RAG 系統已經啟動並運行。

**立即嘗試**：
```bash
poetry run python main_parallel.py
```

**或使用 Web 界面**：
```bash
poetry run python web_api.py &
open web/index.html
```

---

**祝您使用愉快！** 🚀
