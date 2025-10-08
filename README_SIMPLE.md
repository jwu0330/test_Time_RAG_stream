# RAG 流式系統 - 快速開始

## 🚀 快速開始（3 步驟）

### 1. 設置環境
```bash
# 創建虛擬環境並安裝依賴
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 設定 API Key
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. 運行測試
```bash
python RUN_TEST.py
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
# 激活環境
source venv/bin/activate

# 運行測試
python RUN_TEST.py

# 或啟動 Web 界面
python web_api.py
# 然後在瀏覽器打開 web_interface.html
```

---

## 📁 核心文件

| 文件 | 說明 |
|------|------|
| `main_parallel.py` | 並行處理主程序 |
| `scenario_matcher.py` | 情境匹配系統 |
| `scenario_module.py` | 四向度分類器 |
| `knowledge_relations.json` | 知識點關聯定義 |
| `scenarios_24/` | 24 個情境配置 |
| `docs/` | 教材文件 |

---

## 🔧 自定義

### 修改教材
將您的教材放入 `docs/` 目錄，並更新 `config.py` 中的知識點映射。

### 調整情境
編輯 `scenarios_24/` 中的 JSON 文件，自定義回答策略和提示詞。

---

## 📖 詳細文檔

查看 `README_FULL.md` 了解完整說明。
