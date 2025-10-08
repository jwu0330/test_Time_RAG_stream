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

```bash
# 1. 安裝依賴
pip3 install --user -r requirements.txt

# 2. 設定 API Key
export OPENAI_API_KEY="your-api-key-here"

# 3. 運行測試
python3 scripts/run_test.py

# 4. 或啟動 Web 界面
python3 web_api.py
open web/index.html
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

```bash
# 運行測試
python3 scripts/run_test.py

# 啟動 Web API
python3 web_api.py

# 運行主程序
python3 main_parallel.py

# 測試 D4 邏輯
python3 tests/test_d4_logic.py

# 生成新情境
python3 scripts/scenario_generator.py
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
- 依賴套件: openai, numpy, fastapi, uvicorn, pydantic

---

## 📦 安裝

```bash
# 如果沒有 pip
sudo apt install python3-pip

# 安裝依賴
pip3 install --user -r requirements.txt

# 或使用安裝腳本
chmod +x README_ALL/BASH_ALL/install_deps.sh
./README_ALL/BASH_ALL/install_deps.sh
```

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
