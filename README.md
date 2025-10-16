# RAG 教學問答系統

**三維度分類 (K/C/R) + 12 種情境 + 並行處理架構**

---

## 📂 重要規則

⚠️ **文件組織規則**：
- 📝 **所有說明文件** → `README_ALL/` 目錄
- 🔧 **所有 .sh 腳本** → `README_ALL/BASH_ALL/` 目錄
- 🌐 **所有 Web 文件** → `web/` 目錄
- 💻 **核心程式碼** → 根目錄或 `core/`, `scripts/` 等目錄

---

## 🚀 快速開始

### 方法 1: 一鍵啟動（最簡單）

```bash
# 1. 設定 API Key
cp .env.example .env
nano .env  # 編輯並添加你的 OPENAI_API_KEY

# 2. 運行（自動安裝依賴）
bash README_ALL/BASH_ALL/poetry_run.sh test    # 運行主程序
bash README_ALL/BASH_ALL/poetry_run.sh web     # 啟動 Web API
bash README_ALL/BASH_ALL/poetry_run.sh shell   # 進入 Poetry Shell
```

### 方法 2: 使用 Poetry（推薦）

```bash
# 1. 安裝依賴（自動管理虛擬環境）
poetry install

# 2. 設定 API Key
export OPENAI_API_KEY="your-api-key-here"

# 3. 運行系統
poetry run python main_parallel.py

# 或進入 Poetry Shell
poetry shell
python main_parallel.py
```

### 注意事項

⚠️ **建議使用 Poetry 管理依賴**，已移除 `requirements.txt`

---

## 📁 專案結構

```
test_Time_RAG_stream/
├── README.md               # 專案說明（你正在看的文件）
├── main_parallel.py        # 主程序（並行處理）
├── web_api.py              # Web API 服務
├── config.py               # 系統配置
├── pyproject.toml          # Poetry 依賴管理
│
├── core/                   # 核心模組
│   ├── tools/              # 維度檢測工具
│   │   ├── correctness_detector.py    # C 值檢測
│   │   ├── knowledge_detector.py      # 知識點檢測
│   │   └── repetition_checker.py      # R 值檢測
│   ├── dimension_classifier.py        # 維度分類器（集中管理器）
│   ├── scenario_classifier.py         # 情境分類器
│   ├── scenario_calculator.py         # 情境編號計算
│   ├── vector_store.py
│   ├── rag_module.py
│   ├── history_manager.py
│   └── timer_utils.py
│
├── data/                   # 數據目錄
│   ├── docs/              # 教材文件
│   ├── scenarios/         # 12 種情境配置
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

- ✅ **三維度分類**: K(知識點數量)、C(正確性)、R(重複性)
- ✅ **12 種情境**: 自動匹配並調整回答策略
- ✅ **並行處理**: RAG 檢索 + API 調用同時執行
- ✅ **模組化架構**: 每個工具獨立封裝，邏輯清晰
- ✅ **Web 界面**: 互動式聊天界面

---

## 📝 常用命令

### 環境管理

```bash
# 安裝/更新依賴
poetry install

# 進入 Poetry Shell
poetry shell

# 退出 Poetry Shell
exit

# 更新套件
poetry update

# 查看已安裝的套件
poetry show
```

### 運行程序

```bash
# 運行主程序
poetry run python main_parallel.py

# 啟動 Web API
poetry run python web_api.py

# 清除歷史記錄
poetry run python clear_history.py

# 或進入 Shell 後運行
poetry shell
python main_parallel.py
```

---

## 🌐 Web 界面

### 啟動方式

```bash
# 1. 啟動後端
poetry run python web_api.py

# 2. 打開界面
open web/index.html
```

### 功能特色

- 💬 即時對話
- 📊 三維度顯示 (K/C/R)
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

### 推薦方式：使用 Poetry

```bash
# 1. 安裝 Poetry（如果還沒有）
curl -sSL https://install.python-poetry.org | python3 -
# 或
pip install --user poetry

# 2. 安裝專案依賴
poetry install

# 3. 運行系統
poetry run python main_parallel.py
```

### 替代方式：使用 venv

```bash
# 1. 創建虛擬環境
python3 -m venv .venv

# 2. 激活虛擬環境
source .venv/bin/activate

# 3. 安裝依賴
pip install -r requirements.txt
```

### ⚠️ 重要提示

- **推薦使用 Poetry**，自動管理虛擬環境和依賴
- 確保 OpenAI SDK 版本 >= 1.54.0（支持 Responses API）
- Poetry 會自動處理依賴衝突和版本管理

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
【並行處理】
├─ Thread A: RAG 檢索（Embedding API）
└─ Thread B: K/C/R 維度判定
    ├─ API #1: C 值檢測（正確性）
    └─ API #2: 知識點檢測
        ↓
    【本地計算】
    ├─ K 值 = len(knowledge_points)
    └─ R 值 = repetition_checker.check_and_update()
        ↓
【計算情境】
scenario_number = k*4 + c*2 + r + 1  (1-12)
    ↓
【生成答案】
API #3: 生成答案（流式輸出）
```

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

## 📄 授權

MIT License
