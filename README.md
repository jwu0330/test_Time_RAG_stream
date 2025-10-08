# RAG 流式中斷與續寫系統

> 一個支援向量儲存、流式中斷與續寫（Stream Interruption & Resume）的最小可行 RAG 系統

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 專案簡介

這是一個基於 Python 和 OpenAI API 的 RAG (Retrieval-Augmented Generation) 系統，具備以下核心功能：

- ✅ **向量儲存與快速載入**：教材向量化後可持久化儲存
- ✅ **流式中斷與續寫**：支援 Stream Interruption & Resume 機制
- ✅ **情境注入**：四向度情境分類 (D1-D4) 與動態注入
- ✅ **精準時間分析**：詳細記錄各階段耗時
- ✅ **背景任務模擬**：異步執行多個背景任務
- ✅ **可重複測試**：支援快取與增量更新

## 📂 專案結構

```
rag_stream_resume/
├── main.py                 # 主程序
├── vector_store.py         # 向量儲存模組
├── rag_module.py           # RAG 檢索模組
├── scenario_module.py      # 情境判定模組
├── timer_utils.py          # 時間分析模組
├── requirements.txt        # 依賴套件
├── README.md              # 本文檔
├── JIM_README.md          # 完整技術文檔
│
├── docs/                   # 教材資料夾
├── scenarios/              # 情境定義
├── results/                # 測試結果
│
├── test_system.py          # 系統測試
├── quick_start.py          # 快速啟動
├── example_usage.py        # 使用範例
└── setup.sh               # 安裝腳本
```

## 🚀 快速開始

### 1. 安裝依賴

```bash
# 方法 1: 使用安裝腳本（推薦）
chmod +x setup.sh
./setup.sh

# 方法 2: 手動安裝
pip install -r requirements.txt
```

### 2. 設定 API Key

```bash
# 方法 1: 環境變量
export OPENAI_API_KEY="your-api-key-here"

# 方法 2: .env 文件
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 3. 執行測試

```bash
# 系統測試
python test_system.py

# 快速測試
python quick_start.py

# 完整測試
python main.py
```

## 📖 使用指南

### 基本使用

```python
import asyncio
from main import RAGStreamSystem

async def main():
    # 初始化系統
    system = RAGStreamSystem()
    
    # 初始化文件和情境
    await system.initialize_documents("docs")
    await system.load_scenarios("scenarios")
    
    # 處理查詢
    result = await system.process_query("什麼是機器學習？")
    
    # 顯示結果
    system.print_summary(result)
    system.save_result(result)

asyncio.run(main())
```

### 指定情境

```python
# 使用特定情境
result = await system.process_query(
    query="深度學習的優化技巧",
    scenario_ids=["academic", "practical"],
    auto_classify=False
)
```

### 自定義檢索

```python
# 調整檢索參數
results = await system.rag_retriever.retrieve(
    query="神經網絡",
    top_k=5  # 返回前 5 個最相關文件
)

# 使用相似度閾值
results = await system.rag_retriever.retrieve_with_threshold(
    query="神經網絡",
    threshold=0.75,  # 只返回相似度 > 0.75 的文件
    top_k=10
)
```

## 🔧 核心模組

### 1. vector_store.py - 向量儲存

```python
from vector_store import VectorStore

store = VectorStore()

# 添加文件
await store.add_document(
    doc_id="doc1",
    content="文件內容",
    metadata={"category": "ML"}
)

# 儲存與載入
store.save()
store.load()
```

### 2. rag_module.py - RAG 檢索

```python
from rag_module import RAGRetriever

retriever = RAGRetriever(vector_store)

# 檢索相關文件
results = await retriever.retrieve(query, top_k=3)

# 格式化上下文
context = retriever.format_context(results)
```

### 3. scenario_module.py - 情境分類

```python
from scenario_module import ScenarioClassifier

classifier = ScenarioClassifier()
classifier.load_scenarios_from_dir("scenarios")

# 四向度分類
classification = await classifier.classify_scenario(
    query="問題",
    context="上下文"
)
```

### 4. timer_utils.py - 時間分析

```python
from timer_utils import Timer

timer = Timer()

timer.start_stage("階段1")
# ... 執行任務 ...
timer.stop_stage("階段1")

# 生成報告
report = timer.get_report()
timer.print_report()
```

## 📊 工作流程

```
1. 初始化文件
   ├─ 檢查已儲存向量
   ├─ 若無則向量化
   └─ 儲存向量

2. 載入情境
   └─ 讀取 scenarios/ 目錄

3. RAG 檢索
   ├─ 生成查詢向量
   ├─ 計算相似度
   └─ 返回 Top-K

4. 情境分類
   ├─ 四向度評分
   └─ 推薦情境

5. 生成草稿
   ├─ 基於 RAG 上下文
   └─ 暫存不輸出

6. 情境注入
   ├─ 注入情境上下文
   └─ 流式生成最終答案

7. 背景任務
   ├─ 顏色標籤更新
   ├─ 快取標註儲存
   └─ 活動日誌記錄

8. 輸出結果
   ├─ 生成時間報告
   └─ 儲存 JSON
```

## 🎭 情境系統

### 四向度定義

| 向度 | 名稱 | 說明 | 評分範圍 |
|------|------|------|----------|
| **D1** | 時間敏感性 | 是否需要即時回應 | 1-5 |
| **D2** | 情境複雜度 | 問題複雜程度 | 1-5 |
| **D3** | 專業領域 | 專業知識需求 | 1-5 |
| **D4** | 互動模式 | 互動類型 | 1-5 |

### 預設情境

- **academic** - 學術研究情境（深入技術探討）
- **practical** - 實務應用情境（可操作步驟）
- **beginner** - 初學者學習情境（簡單易懂）
- **troubleshooting** - 問題排查情境（快速診斷）

## ⏱️ 效能分析

### 典型耗時

| 階段 | 預期耗時 | 優化後 |
|------|----------|--------|
| 向量化（首次） | 2-5s | <0.1s（快取） |
| RAG 檢索 | 0.5-1s | <0.1s（快取） |
| 情境分類 | 0.8-1.5s | - |
| LLM 草稿 | 1-2s | - |
| 情境續寫 | 2-4s | - |
| 背景任務 | 0.3-0.6s | - |
| **總計** | **6-10s** | **<5s** |

### 優化建議

1. **使用向量快取**：避免重複向量化
2. **使用 RAG 快取**：快取檢索結果
3. **並行處理**：使用 `asyncio.gather()`
4. **選擇小模型**：使用 `gpt-3.5-turbo`

## 🧪 測試

### 執行測試套件

```bash
python test_system.py
```

測試項目：
- ✅ 模組導入
- ✅ 計時器功能
- ✅ 向量儲存
- ✅ RAG 快取
- ✅ 情境載入
- ✅ 文件結構

### 執行範例

```bash
python example_usage.py
```

包含 10 個使用範例：
1. 基本使用
2. 指定特定情境
3. 批量處理
4. 快取效果
5. 自定義檢索
6. 情境分類
7. 時間分析
8. 錯誤處理
9. 儲存與載入
10. 背景任務

## 📝 輸出格式

### 結果 JSON

```json
{
  "query": "什麼是機器學習？",
  "final_answer": "機器學習是...",
  "scenario_used": "beginner",
  "matched_docs": ["ml_basics.txt", "deep_learning.txt"],
  "time_report": {
    "timestamp": "2025-10-08T12:26:38+08:00",
    "stages": {
      "向量化": 0.523,
      "RAG檢索": 0.718,
      "情境分類": 0.842,
      "LLM草稿生成": 1.234,
      "情境注入與續寫": 2.567,
      "背景任務": 0.456
    },
    "total_time": 6.340
  }
}
```

## 🔧 自定義配置

### 添加新文件

將文件放入 `docs/` 目錄：

```bash
cp your_document.txt docs/
```

系統會自動向量化新文件。

### 添加新情境

在 `scenarios/` 目錄創建 JSON 或 TXT 文件：

```json
{
  "id": "custom",
  "name": "自定義情境",
  "dimensions": {
    "D1": 3,
    "D2": 4,
    "D3": 3,
    "D4": 2
  },
  "content": "情境描述..."
}
```

### 調整模型

```python
# 使用不同的 embedding 模型
store = VectorStore()
store.embedding_model = "text-embedding-3-large"

# 使用不同的 LLM
classifier = ScenarioClassifier(use_small_model=False)  # 使用 GPT-4
```

## ❓ 常見問題

### Q: 如何設定 API Key？

**A:** 三種方法：
1. 環境變量：`export OPENAI_API_KEY="sk-..."`
2. .env 文件：`echo "OPENAI_API_KEY=sk-..." > .env`
3. 代碼中：`RAGStreamSystem(api_key="sk-...")`

### Q: 向量文件太大怎麼辦？

**A:** 
- 使用較小的 embedding 模型
- 分批處理文件
- 使用向量資料庫（Pinecone、Weaviate）

### Q: 如何減少 API 成本？

**A:**
- 使用快取機制
- 選擇 `gpt-3.5-turbo`
- 減少 `max_tokens`
- 批量處理請求

### Q: 支援哪些文件格式？

**A:** 目前支援 `.txt` 文件。可擴展支援 PDF、Word 等格式。

## 📚 完整文檔

查看 [JIM_README.md](JIM_README.md) 獲取：
- 詳細技術架構
- API 參考文檔
- 進階功能說明
- 故障排除指南
- 最佳實踐建議

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License

## 👤 作者

**Jim**

---

**Happy Coding! 🚀**
