# RAG 流式系統 - 快速開始

## 📂 文件組織規則

⚠️ **重要**：
- 📝 **所有說明文件** 統一放在 `README_ALL/` 目錄
- 🔧 **所有 .sh 腳本** 統一放在 `README_ALL/BASH_ALL/` 目錄
- 💻 **核心程式碼** 放在根目錄或 `core/`, `scripts/` 等目錄

---

## 🚀 快速開始（3 步驟）

### 1. 安裝依賴
```bash
# 方式 A：使用系統 Python（推薦）
python3 -m pip install --user -r requirements.txt

# 方式 B：如果有 pip
sudo apt install python3-pip
pip3 install --user -r requirements.txt
```

### 2. 設定 API Key
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. 運行測試
```bash
python3 scripts/run_test.py
```

---

## 📋 系統功能

- ✅ **四向度分類**：D1(知識點數量)、D2(表達錯誤)、D3(表達詳細度)、D4(重複詢問)
- ✅ **24 種情境**：自動匹配並調整回答策略
- ✅ **並行處理**：多線程分析，提升效率
- ✅ **Web 界面**：可選的圖形化界面

---

## 🎯 日常使用

```bash
# 運行測試
python3 scripts/run_test.py

# 或啟動 Web 界面
python3 web_api.py
# 然後在瀏覽器打開 web_interface.html

# 或直接運行主程序
python3 main_parallel.py
```

---

## 📁 核心文件

| 文件/目錄 | 說明 |
|------|------|
| `main_parallel.py` | 並行處理主程序 |
| `web_api.py` | Web API 服務 |
| `config.py` | 系統配置 |
| `core/` | 核心模組目錄 |
| `data/docs/` | 教材文件 |
| `data/scenarios/` | 24 個情境配置 |
| `data/knowledge_relations.json` | 知識點關聯定義 |
| `scripts/` | 工具腳本 |
| `tests/` | 測試文件 |

---

## 🔧 自定義

### 修改教材
將您的教材放入 `data/docs/` 目錄，並更新 `config.py` 中的知識點映射。

### 調整情境
編輯 `data/scenarios/` 中的 JSON 文件，自定義回答策略和提示詞。

---

## 📖 詳細文檔

查看 `README_FULL.md` 了解完整說明。
