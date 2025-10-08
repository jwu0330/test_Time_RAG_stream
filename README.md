# RAG 流式系統

**四向度分類 + 24 種情境 + 並行處理架構**

---

## 📂 重要規則

⚠️ **文件組織規則**：
- 📝 **所有說明文件** → `README_ALL/` 目錄
- 🔧 **所有 .sh 腳本** → `README_ALL/BASH_ALL/` 目錄
- 🌐 **所有 Web 文件** → `web/` 目錄
- 💻 **核心程式碼** → 根目錄或 `core/`, `scripts/` 等目錄

---

## 🚀 快速開始

### 方法 1: 一鍵測試（推薦）

```bash
# 自動激活虛擬環境並運行測試
bash README_ALL/BASH_ALL/quick_test.sh
```

### 方法 2: 手動步驟

```bash
# 1. 清理並安裝依賴到虛擬環境
bash README_ALL/BASH_ALL/cleanup_and_reinstall.sh

# 2. 激活虛擬環境
source .venv/bin/activate

# 3. 設定 API Key
export OPENAI_API_KEY="your-api-key-here"

# 4. 運行測試
python3 main_parallel.py

# 5. 或啟動 Web API
python3 web_api.py
# 訪問 http://localhost:8000/docs
```

---

## 📁 專案結構

```
test_Time_RAG_stream/
├── README.md               # 專案說明（你正在看的文件）
├── main_parallel.py        # 主程序（並行處理）
├── web_api.py              # Web API 服務
├── config.py               # 系統配置
├── requirements.txt        # Python 依賴
│
├── core/                   # 核心模組
│   ├── vector_store.py
│   ├── rag_module.py
│   ├── scenario_module.py
│   ├── scenario_matcher.py
│   ├── history_manager.py
│   └── timer_utils.py
│
├── data/                   # 數據目錄
│   ├── docs/              # 教材文件
│   ├── scenarios/         # 24 種情境配置
│   └── knowledge_relations.json
│
├── web/                    # 🌐 Web 界面
│   ├── index.html         # 主界面
│   ├── app.js             # JavaScript
│   └── README.md          # Web 使用說明
│
├── tests/                  # 測試文件
│   ├── test_system.py
│   └── test_d4_logic.py
│
├── scripts/                # 工具腳本
│   ├── run_test.py
│   └── scenario_generator.py
│
└── README_ALL/             # 📝 所有說明文件
    ├── 00_README_INDEX.md      # 📑 文檔導航（從這裡開始）
    ├── 01_QUICK_START.md       # 🚀 5分鐘快速開始
    ├── 02_INSTALLATION.md      # 🔧 詳細安裝指南
    ├── 10_SYSTEM_OVERVIEW.md   # 📊 系統完整概述
    ├── TIMING_GUIDE.md         # ⏱️ 雙線程計時系統
    ├── DOC_REORG_SUMMARY.md    # 📋 文檔整理總結
    └── BASH_ALL/               # 🔧 所有 .sh 腳本
```

---

## 🎯 主要功能

- ✅ **四向度分類**: D1(知識點數量)、D2(表達錯誤)、D3(表達詳細度)、D4(重複詢問)
- ✅ **24 種情境**: 自動匹配並調整回答策略
- ✅ **並行處理**: 多線程分析，提升效率
- ✅ **Web 界面**: 互動式聊天界面

---

## 📝 常用命令

### 環境管理

```bash
# 激活虛擬環境
source .venv/bin/activate

# 退出虛擬環境
deactivate

# 重新安裝依賴
bash README_ALL/BASH_ALL/cleanup_and_reinstall.sh
```

### 運行程序（需先激活虛擬環境）

```bash
# 快速測試（自動激活虛擬環境）
bash README_ALL/BASH_ALL/quick_test.sh

# 運行主程序
python3 main_parallel.py

# 啟動 Web API
python3 web_api.py

# 清除歷史記錄
bash README_ALL/BASH_ALL/clear_history.sh
# 或
python3 clear_history.py
```

---

## 🌐 Web 界面

### 啟動方式

```bash
# 1. 啟動後端
python3 web_api.py

# 2. 打開界面
open web/index.html
```

### 功能特色

- 💬 即時對話
- 📊 四向度顯示
- ⏱️ 響應時間統計
- 💡 範例問題
- 📱 響應式設計

詳細說明：`web/README.md`

---

## 📖 詳細文檔

**📑 文檔導航**: [README_ALL/00_README_INDEX.md](README_ALL/00_README_INDEX.md) - **從這裡開始！**

### 快速開始

- **5分鐘上手**: [README_ALL/01_QUICK_START.md](README_ALL/01_QUICK_START.md) ⭐
- **詳細安裝**: [README_ALL/02_INSTALLATION.md](README_ALL/02_INSTALLATION.md)

### 系統說明

- **系統概述**: [README_ALL/10_SYSTEM_OVERVIEW.md](README_ALL/10_SYSTEM_OVERVIEW.md)
- **雙線程計時**: [README_ALL/TIMING_GUIDE.md](README_ALL/TIMING_GUIDE.md)

### 其他文檔

查看完整的文檔索引：[README_ALL/00_README_INDEX.md](README_ALL/00_README_INDEX.md)

---

## 🔧 環境需求

- Python 3.8+
- OpenAI API Key
- 虛擬環境（`.venv/`）
- 依賴套件: 
  - openai >= 1.54.0（支持 Responses API）
  - numpy >= 1.24.0
  - fastapi >= 0.104.0
  - uvicorn >= 0.24.0
  - pydantic >= 2.0.0
  - python-dotenv >= 1.0.0

---

## 📦 安裝

### 推薦方式：使用虛擬環境

```bash
# 一鍵清理並安裝到虛擬環境
bash README_ALL/BASH_ALL/cleanup_and_reinstall.sh
```

### 手動安裝

```bash
# 1. 創建虛擬環境（如果不存在）
python3 -m venv .venv

# 2. 激活虛擬環境
source .venv/bin/activate

# 3. 升級 pip
pip install --upgrade pip

# 4. 安裝依賴
pip install -r requirements.txt
```

### ⚠️ 重要提示

- **請使用虛擬環境**，避免污染全局 Python 環境
- 確保 OpenAI SDK 版本 >= 1.54.0（支持 Responses API）
- 所有腳本都會自動檢查並激活虛擬環境

---

## ⚙️ 配置

編輯 `config.py` 設定：
- LLM 模型
- Embedding 模型
- 歷史記錄大小
- RAG 參數
- 知識點映射

---

## 📊 系統架構

```
用戶問題
    ↓
並行分析（D2、D3、D4 同時執行）
    ↓
RAG 檢索 → D1 分析
    ↓
情境匹配（O(1) 查找）
    ↓
合併到主線程
    ↓
生成最終答案
```

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

## 📄 授權

MIT License
