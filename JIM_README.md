# 🚀 RAG 流式中斷與續寫系統 - Jim 完整文檔

## 📋 目錄
1. [系統概述](#系統概述)
2. [專案結構](#專案結構)
3. [核心功能](#核心功能)
4. [技術架構](#技術架構)
5. [安裝與配置](#安裝與配置)
6. [使用指南](#使用指南)
7. [模組詳解](#模組詳解)
8. [工作流程](#工作流程)
9. [測試與驗證](#測試與驗證)
10. [效能分析](#效能分析)
11. [常見問題](#常見問題)
12. [進階功能](#進階功能)

---

## 🎯 系統概述

這是一個**最小可行的 RAG (Retrieval-Augmented Generation) 系統**，具備以下核心特性：

### 主要特點
- ✅ **向量儲存與快速載入**：教材向量化後可持久化儲存，避免重複計算
- ✅ **流式中斷與續寫**：支援 Stream Interruption & Resume 機制
- ✅ **情境注入**：四向度情境分類 (D1-D4) 與動態注入
- ✅ **精準時間分析**：使用 `time.perf_counter()` 記錄各階段耗時
- ✅ **背景任務模擬**：異步執行顏色標籤、快取標註等任務
- ✅ **可重複測試**：支援多輪測試與效能比較

### 設計原則
- 🎯 **最小測試範圍**：專注核心功能，避免過度設計
- ⏱️ **精準時間分析**：每個階段都有獨立計時
- 🔄 **可重複執行**：支援快取與增量更新
- 🐛 **可偵錯修正**：清晰的日誌與錯誤處理

---

## 📂 專案結構

```
rag_stream_resume/
├── main.py                 # 主程序 - 系統入口與流程編排
├── vector_store.py         # 向量儲存模組 - embeddings 生成與管理
├── rag_module.py           # RAG 檢索模組 - 相似度計算與文件檢索
├── scenario_module.py      # 情境判定模組 - 四向度分類與注入
├── timer_utils.py          # 時間分析模組 - 精準計時工具
├── requirements.txt        # Python 依賴套件
├── JIM_README.md          # 本文檔
│
├── docs/                   # 📚 教材上傳資料夾
│   ├── doc1.txt
│   ├── doc2.txt
│   └── doc3.txt
│
├── scenarios/              # 🎭 情境 JSON/TXT 檔案
│   ├── scenario1.json
│   ├── scenario2.json
│   └── scenario3.txt
│
├── results/                # 📊 測試結果輸出
│   └── result_20251008_122638.json
│
├── vectors.pkl             # 💾 向量儲存文件 (pickle 格式)
└── vectors.json            # 📄 向量元數據 (JSON 格式)
```

---

## 🔧 核心功能

### 1️⃣ 向量化與儲存 (Step 1-3)
- 使用 OpenAI `text-embedding-3-small` 模型生成向量
- 支援 pickle 和 JSON 兩種儲存格式
- 自動檢測已存在的向量文件，避免重複計算
- 快速載入與相似度比對

### 2️⃣ LLM 通用草案 (Step 4)
- 基於 RAG 檢索結果生成初步回答
- 草稿暫存於記憶體，不直接輸出
- 模擬 Stream Pause 機制

### 3️⃣ 情境注入與續寫 (Step 5)
- 四向度情境分類：
  - **D1**: 時間敏感性 (Time Sensitivity)
  - **D2**: 情境複雜度 (Context Complexity)
  - **D3**: 專業領域 (Domain Expertise)
  - **D4**: 互動模式 (Interaction Mode)
- 動態注入情境後續寫最終答案
- 支援流式輸出 (Stream Mode)

### 4️⃣ 時間記錄與報告 (Step 6)
- 使用 `time.perf_counter()` 精準計時
- 記錄各階段耗時：
  - 向量化
  - RAG 檢索
  - 情境分類
  - LLM 草稿生成
  - 情境注入與續寫
  - 背景任務
- 輸出 JSON 格式報告

### 5️⃣ 背景任務模擬 (Step 7)
- 異步執行多個背景任務：
  - 顏色標籤更新
  - 快取標註儲存
  - 活動日誌記錄
- 使用 `asyncio.gather()` 並行執行

### 6️⃣ 測試回合 (Step 8)
- 支援多次測試輸入
- 計算平均耗時與差異
- 生成效能比較分析

---

## 🏗️ 技術架構

### 技術棧
| 模組 | 技術 | 說明 |
|------|------|------|
| **向量生成** | OpenAI Embeddings API | `text-embedding-3-small` 模型 |
| **向量儲存** | Pickle / JSON | 本地持久化儲存 |
| **相似度計算** | NumPy | 餘弦相似度 (Cosine Similarity) |
| **LLM 調用** | OpenAI Chat Completions | GPT-3.5-turbo / GPT-4 |
| **異步處理** | asyncio | 並行執行與流程編排 |
| **時間測量** | time.perf_counter() | 高精度計時 |
| **數據格式** | JSON | 結果輸出與情境定義 |

### 系統架構圖

```
┌─────────────────────────────────────────────────────────┐
│                    RAGStreamSystem                       │
│                      (主系統類)                          │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ VectorStore  │   │ RAGRetriever │   │  Scenario    │
│              │   │              │   │  Classifier  │
│ - 向量生成   │   │ - 相似度計算 │   │ - 四向度分類 │
│ - 儲存/載入  │   │ - Top-K 檢索 │   │ - 情境注入   │
│ - 快取管理   │   │ - 快取機制   │   │ - 續寫提示   │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │    Timer     │
                    │              │
                    │ - 階段計時   │
                    │ - 報告生成   │
                    └──────────────┘
```

---

## 🛠️ 安裝與配置

### 1. 環境需求
- Python 3.8+
- OpenAI API Key

### 2. 安裝步驟

```bash
# 1. 克隆或進入專案目錄
cd /home/jim/code/py/test_Time_RAG_stream

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定 OpenAI API Key
export OPENAI_API_KEY="your-api-key-here"

# 或創建 .env 文件
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 3. 目錄準備

```bash
# 創建必要的目錄
mkdir -p docs scenarios results
```

---

## 📖 使用指南

### 快速開始

#### 1️⃣ 準備教材文件

在 `docs/` 目錄下放置 3 份教材文件：

```bash
# 範例：創建測試教材
cat > docs/ml_basics.txt << 'EOF'
機器學習是人工智慧的一個分支，它使計算機能夠從數據中學習並改進性能。
主要類型包括：
1. 監督式學習 - 使用標記數據訓練模型
2. 非監督式學習 - 從未標記數據中發現模式
3. 強化學習 - 通過獎勵機制學習最佳策略
EOF

cat > docs/deep_learning.txt << 'EOF'
深度學習是機器學習的子領域，使用多層神經網絡處理複雜數據。
關鍵概念：
- 神經網絡架構（CNN、RNN、Transformer）
- 反向傳播算法
- 梯度下降優化
- 正則化技術（Dropout、Batch Normalization）
EOF

cat > docs/nlp_intro.txt << 'EOF'
自然語言處理 (NLP) 是讓計算機理解和生成人類語言的技術。
主要任務：
- 文本分類
- 命名實體識別
- 機器翻譯
- 情感分析
- 問答系統
常用模型：BERT、GPT、T5
EOF
```

#### 2️⃣ 準備情境文件

在 `scenarios/` 目錄下創建情境文件：

```bash
# 範例：創建情境 JSON
cat > scenarios/academic.json << 'EOF'
{
  "id": "academic",
  "name": "學術研究情境",
  "dimensions": {
    "D1": 2,
    "D2": 4,
    "D3": 5,
    "D4": 2
  },
  "content": "這是一個學術研究場景，需要提供深入的技術細節和引用來源。回答應該專業、嚴謹，包含相關理論基礎。"
}
EOF

cat > scenarios/practical.json << 'EOF'
{
  "id": "practical",
  "name": "實務應用情境",
  "dimensions": {
    "D1": 4,
    "D2": 3,
    "D3": 3,
    "D4": 3
  },
  "content": "這是一個實務應用場景，需要提供可操作的步驟和實際範例。回答應該簡潔明瞭，注重實用性。"
}
EOF

cat > scenarios/beginner.txt << 'EOF'
這是一個初學者學習情境。
使用者可能是第一次接觸這個主題，需要：
- 簡單易懂的解釋
- 避免過多專業術語
- 提供類比和實例
- 循序漸進的說明
EOF
```

#### 3️⃣ 執行系統

```bash
# 直接執行主程序
python main.py
```

### 自定義使用

```python
import asyncio
from main import RAGStreamSystem

async def custom_usage():
    # 初始化系統
    system = RAGStreamSystem(api_key="your-api-key")
    
    # 初始化文件和情境
    await system.initialize_documents("docs")
    await system.load_scenarios("scenarios")
    
    # 處理單個查詢
    result = await system.process_query(
        query="什麼是深度學習？",
        scenario_ids=["academic"],  # 指定情境
        auto_classify=False  # 不自動分類
    )
    
    # 打印結果
    system.print_summary(result)
    system.save_result(result)

# 執行
asyncio.run(custom_usage())
```

---

## 🔍 模組詳解

### 1. timer_utils.py - 時間分析模組

#### 核心類別

**TimerRecord**
```python
@dataclass
class TimerRecord:
    name: str           # 階段名稱
    start_time: float   # 開始時間
    end_time: float     # 結束時間
    duration: float     # 持續時間
```

**Timer**
```python
class Timer:
    def start_stage(stage_name: str)  # 開始計時
    def stop_stage(stage_name: str)   # 停止計時
    def get_report() -> TimerReport   # 生成報告
    def print_report()                # 打印報告
```

#### 使用範例

```python
from timer_utils import Timer

timer = Timer()

timer.start_stage("資料處理")
# ... 執行任務 ...
timer.stop_stage("資料處理")

timer.start_stage("模型推理")
# ... 執行任務 ...
timer.stop_stage("模型推理")

# 生成報告
report = timer.get_report()
print(report.to_dict())
```

---

### 2. vector_store.py - 向量儲存模組

#### 核心類別

**VectorStore**
```python
class VectorStore:
    async def create_embedding(text: str) -> List[float]
    async def add_document(doc_id: str, content: str, metadata: dict)
    async def batch_add_documents(documents: List[Dict])
    def save()                        # 儲存向量
    def load() -> bool                # 載入向量
    def export_to_json(json_path: str)
```

#### 使用範例

```python
from vector_store import VectorStore

# 初始化
store = VectorStore(storage_path="vectors.pkl")

# 添加文件
await store.add_document(
    doc_id="doc1",
    content="這是一份關於機器學習的文件",
    metadata={"category": "ML"}
)

# 儲存
store.save()

# 載入
store.load()
```

#### 相似度計算

```python
from vector_store import cosine_similarity

vec1 = [0.1, 0.2, 0.3, ...]
vec2 = [0.15, 0.25, 0.28, ...]

similarity = cosine_similarity(vec1, vec2)
print(f"相似度: {similarity:.3f}")
```

---

### 3. rag_module.py - RAG 檢索模組

#### 核心類別

**RAGRetriever**
```python
class RAGRetriever:
    async def retrieve(query: str, top_k: int) -> List[Dict]
    async def retrieve_with_threshold(query: str, threshold: float)
    def format_context(retrieved_docs: List[Dict]) -> str
    def get_matched_doc_ids(retrieved_docs: List[Dict]) -> List[str]
```

**RAGCache**
```python
class RAGCache:
    def get(query: str) -> List[Dict] | None
    def put(query: str, results: List[Dict])
    def get_stats() -> Dict
```

#### 使用範例

```python
from rag_module import RAGRetriever, RAGCache

# 初始化檢索器
retriever = RAGRetriever(vector_store)

# 檢索相關文件
results = await retriever.retrieve(
    query="什麼是機器學習？",
    top_k=3
)

# 格式化上下文
context = retriever.format_context(results)

# 使用快取
cache = RAGCache()
cached_results = cache.get(query)
if not cached_results:
    results = await retriever.retrieve(query)
    cache.put(query, results)
```

---

### 4. scenario_module.py - 情境判定模組

#### 核心類別

**ScenarioClassifier**
```python
class ScenarioClassifier:
    DIMENSIONS = {
        "D1": "時間敏感性",
        "D2": "情境複雜度",
        "D3": "專業領域",
        "D4": "互動模式"
    }
    
    def load_scenarios_from_dir(scenarios_dir: str)
    async def classify_scenario(query: str, context: str) -> Dict
    def get_scenario_by_dimensions(classification: Dict) -> List[str]
    def get_scenario_content(scenario_id: str) -> str
```

**ScenarioInjector**
```python
class ScenarioInjector:
    def create_injection_prompt(
        draft_response: str,
        scenario_context: str,
        original_query: str
    ) -> str
```

#### 四向度說明

| 向度 | 名稱 | 說明 | 評分標準 (1-5) |
|------|------|------|----------------|
| **D1** | 時間敏感性 | 是否需要即時回應 | 1=不急 → 5=極急 |
| **D2** | 情境複雜度 | 問題複雜程度 | 1=簡單 → 5=複雜 |
| **D3** | 專業領域 | 專業知識需求 | 1=通用 → 5=專業 |
| **D4** | 互動模式 | 互動類型 | 1=單次 → 5=多輪 |

#### 使用範例

```python
from scenario_module import ScenarioClassifier, ScenarioInjector

# 初始化分類器
classifier = ScenarioClassifier()
classifier.load_scenarios_from_dir("scenarios")

# 分類情境
classification = await classifier.classify_scenario(
    query="如何優化深度學習模型？",
    context="相關技術文件..."
)

# 結果範例
{
  "D1": {"score": 2, "reason": "非緊急問題"},
  "D2": {"score": 4, "reason": "需要深入技術理解"},
  "D3": {"score": 5, "reason": "專業深度學習知識"},
  "D4": {"score": 3, "reason": "可能需要多輪對話"}
}

# 獲取推薦情境
scenarios = classifier.get_scenario_by_dimensions(classification)
```

---

### 5. main.py - 主程序

#### 核心類別

**RAGStreamSystem**
```python
class RAGStreamSystem:
    async def initialize_documents(docs_dir: str)
    async def load_scenarios(scenarios_dir: str)
    async def generate_draft(query: str, context: str) -> str
    async def resume_with_scenario(query: str, scenario_ids: List[str]) -> str
    async def process_query(query: str, scenario_ids: List[str]) -> Dict
    async def run_background_tasks()
    def save_result(result: Dict, output_dir: str)
    def print_summary(result: Dict)
```

#### 完整流程

```python
async def main():
    # 1. 初始化系統
    system = RAGStreamSystem()
    
    # 2. 初始化文件和情境
    await system.initialize_documents()
    await system.load_scenarios()
    
    # 3. 處理查詢
    result = await system.process_query("什麼是機器學習？")
    
    # 4. 輸出結果
    system.print_summary(result)
    system.save_result(result)
```

---

## 🔄 工作流程

### 完整執行流程圖

```
開始
  │
  ▼
┌─────────────────────┐
│ Step 1: 初始化文件  │
│ - 檢查 vectors.pkl  │
│ - 若無則向量化      │
│ - 儲存向量          │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Step 2: 載入情境    │
│ - 讀取 scenarios/   │
│ - 解析 JSON/TXT     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Step 3: RAG 檢索    │
│ - 生成查詢向量      │
│ - 計算相似度        │
│ - 返回 Top-K        │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Step 4: 情境分類    │
│ - 四向度評分        │
│ - 推薦情境          │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Step 5: 生成草稿    │
│ - 基於 RAG 上下文   │
│ - 暫存不輸出        │
│ - 模擬 Stream Pause │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Step 6: 情境注入    │
│ - 注入情境上下文    │
│ - Resume Stream     │
│ - 生成最終答案      │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Step 7: 背景任務    │
│ - 顏色標籤更新      │
│ - 快取標註儲存      │
│ - 活動日誌記錄      │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Step 8: 輸出結果    │
│ - 生成時間報告      │
│ - 儲存 JSON         │
│ - 打印摘要          │
└─────────────────────┘
  │
  ▼
結束
```

### 時間線分析

```
時間軸 (秒)
0.0 ────────────────────────────────────────────────────────> 6.2
│         │        │       │        │          │        │
│ 向量化  │ RAG    │ 情境  │ 草稿   │ 續寫     │ 背景   │
│ 0.5s    │ 0.7s   │ 0.8s  │ 1.2s   │ 2.5s     │ 0.5s   │
│         │        │       │        │          │        │
└─────────┴────────┴───────┴────────┴──────────┴────────┘
  初始化    檢索     分類    暫停     注入       任務
```

---

## 🧪 測試與驗證

### 單元測試範例

創建 `test_system.py`：

```python
import asyncio
import pytest
from main import RAGStreamSystem

@pytest.mark.asyncio
async def test_vector_store():
    """測試向量儲存功能"""
    system = RAGStreamSystem()
    
    # 測試向量化
    await system.vector_store.add_document(
        doc_id="test_doc",
        content="測試文件內容"
    )
    
    # 驗證儲存
    assert "test_doc" in system.vector_store.get_all_documents()
    
    # 測試儲存與載入
    system.vector_store.save()
    system.vector_store.clear()
    assert system.vector_store.load() == True

@pytest.mark.asyncio
async def test_rag_retrieval():
    """測試 RAG 檢索功能"""
    system = RAGStreamSystem()
    await system.initialize_documents()
    
    # 測試檢索
    results = await system.rag_retriever.retrieve(
        query="機器學習",
        top_k=3
    )
    
    assert len(results) <= 3
    assert all("score" in r for r in results)

@pytest.mark.asyncio
async def test_full_pipeline():
    """測試完整流程"""
    system = RAGStreamSystem()
    await system.initialize_documents()
    await system.load_scenarios()
    
    result = await system.process_query("什麼是深度學習？")
    
    assert "final_answer" in result
    assert "time_report" in result
    assert result["time_report"]["total_time"] > 0
```

### 執行測試

```bash
# 安裝 pytest
pip install pytest pytest-asyncio

# 執行測試
pytest test_system.py -v
```

### 手動測試腳本

創建 `manual_test.py`：

```python
import asyncio
from main import RAGStreamSystem

async def manual_test():
    """手動測試腳本"""
    
    print("🧪 開始手動測試...")
    
    # 初始化
    system = RAGStreamSystem()
    await system.initialize_documents()
    await system.load_scenarios()
    
    # 測試案例
    test_cases = [
        {
            "query": "什麼是機器學習？",
            "expected_docs": ["ml_basics.txt"],
            "expected_scenario": ["beginner"]
        },
        {
            "query": "如何優化深度學習模型的訓練速度？",
            "expected_docs": ["deep_learning.txt"],
            "expected_scenario": ["practical", "academic"]
        },
        {
            "query": "BERT 模型在 NLP 中的應用",
            "expected_docs": ["nlp_intro.txt"],
            "expected_scenario": ["academic"]
        }
    ]
    
    results = []
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"測試案例 {i}: {case['query']}")
        print(f"{'='*60}")
        
        result = await system.process_query(case["query"])
        results.append(result)
        
        # 驗證結果
        print(f"\n✅ 驗證:")
        print(f"  匹配文件: {result['matched_docs']}")
        print(f"  使用情境: {result['scenario_used']}")
        print(f"  總耗時: {result['time_report']['total_time']}s")
        
        system.save_result(result)
    
    # 統計分析
    print(f"\n{'='*60}")
    print("📊 測試統計")
    print(f"{'='*60}")
    
    avg_time = sum(r['time_report']['total_time'] for r in results) / len(results)
    print(f"平均耗時: {avg_time:.3f}s")
    
    print("\n✅ 測試完成！")

if __name__ == "__main__":
    asyncio.run(manual_test())
```

---

## 📊 效能分析

### 時間分析報告格式

```json
{
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
```

### 效能優化建議

#### 1. 向量快取
```python
# 使用已儲存的向量，避免重複計算
if vector_store.load():
    print("✅ 使用快取向量")
else:
    await vector_store.batch_add_documents(docs)
    vector_store.save()
```

#### 2. RAG 快取
```python
# 快取檢索結果
cache = RAGCache(max_size=100)
results = cache.get(query)
if not results:
    results = await retriever.retrieve(query)
    cache.put(query, results)
```

#### 3. 並行處理
```python
# 並行執行獨立任務
results = await asyncio.gather(
    rag_retriever.retrieve(query),
    scenario_classifier.classify_scenario(query),
    background_task_1(),
    background_task_2()
)
```

#### 4. 模型選擇
```python
# 使用較小的模型加速
classifier = ScenarioClassifier(use_small_model=True)  # gpt-3.5-turbo
```

### 效能基準

| 階段 | 預期耗時 | 優化目標 |
|------|----------|----------|
| 向量化 (首次) | 2-5s | 使用快取 → <0.1s |
| RAG 檢索 | 0.5-1s | 使用快取 → <0.1s |
| 情境分類 | 0.8-1.5s | 使用小模型 |
| LLM 草稿 | 1-2s | 減少 max_tokens |
| 情境續寫 | 2-4s | 流式輸出 |
| 背景任務 | 0.3-0.6s | 並行執行 |
| **總計** | **6-10s** | **<5s** |

---

## ❓ 常見問題

### Q1: 如何設定 OpenAI API Key？

**方法 1: 環境變量**
```bash
export OPENAI_API_KEY="sk-..."
```

**方法 2: .env 文件**
```bash
echo "OPENAI_API_KEY=sk-..." > .env
pip install python-dotenv
```

**方法 3: 代碼中設定**
```python
system = RAGStreamSystem(api_key="sk-...")
```

### Q2: 向量文件太大怎麼辦？

**解決方案：**
1. 使用較小的 embedding 模型
2. 分批處理文件
3. 使用向量資料庫 (如 Pinecone, Weaviate)

```python
# 分批處理
batch_size = 10
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    await vector_store.batch_add_documents(batch)
    vector_store.save()
```

### Q3: 如何自定義情境向度？

**修改 `scenario_module.py`：**
```python
class ScenarioClassifier:
    DIMENSIONS = {
        "D1": "自定義向度1",
        "D2": "自定義向度2",
        "D3": "自定義向度3",
        "D4": "自定義向度4",
        "D5": "新增向度5"  # 可擴展
    }
```

### Q4: 如何處理大量文件？

**使用增量更新：**
```python
# 只向量化新文件
existing_docs = vector_store.get_all_documents()
new_docs = [d for d in documents if d["id"] not in existing_docs]

if new_docs:
    await vector_store.batch_add_documents(new_docs)
    vector_store.save()
```

### Q5: 如何調整檢索精度？

**調整參數：**
```python
# 增加 top_k
results = await retriever.retrieve(query, top_k=5)

# 使用相似度閾值
results = await retriever.retrieve_with_threshold(
    query=query,
    threshold=0.75,  # 只返回相似度 > 0.75 的文件
    top_k=10
)
```

### Q6: 如何減少 API 調用成本？

**優化策略：**
1. 使用快取機制
2. 選擇較小的模型
3. 減少 max_tokens
4. 批量處理請求

```python
# 使用 gpt-3.5-turbo 替代 gpt-4
classifier = ScenarioClassifier(use_small_model=True)

# 減少輸出長度
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens=300  # 減少 token 使用
)
```

---

## 🚀 進階功能

### 1. 自定義向量模型

```python
class CustomVectorStore(VectorStore):
    def __init__(self, model_name="text-embedding-3-large"):
        super().__init__()
        self.embedding_model = model_name  # 使用更大的模型
```

### 2. 多語言支援

```python
async def multilingual_retrieve(query: str, language: str = "zh"):
    """支援多語言檢索"""
    if language != "zh":
        # 翻譯查詢
        query = await translate(query, target_lang="zh")
    
    results = await retriever.retrieve(query)
    return results
```

### 3. 流式輸出優化

```python
async def stream_with_callback(query: str, callback):
    """帶回調的流式輸出"""
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[...],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            await callback(content)  # 實時回調
```

### 4. 分散式向量儲存

```python
# 整合 Pinecone
import pinecone

class PineconeVectorStore(VectorStore):
    def __init__(self, index_name: str):
        pinecone.init(api_key="...")
        self.index = pinecone.Index(index_name)
    
    async def add_document(self, doc_id: str, content: str):
        embedding = await self.create_embedding(content)
        self.index.upsert([(doc_id, embedding, {"content": content})])
```

### 5. 實時監控

```python
class MonitoredRAGSystem(RAGStreamSystem):
    def __init__(self):
        super().__init__()
        self.metrics = {
            "total_queries": 0,
            "avg_response_time": 0,
            "cache_hit_rate": 0
        }
    
    async def process_query(self, query: str):
        self.metrics["total_queries"] += 1
        result = await super().process_query(query)
        
        # 更新指標
        self.update_metrics(result)
        return result
```

---

## 📝 結語

這個系統提供了一個**最小可行的 RAG 流式中斷與續寫**實現，具備以下優勢：

✅ **模組化設計**：每個模組職責清晰，易於擴展  
✅ **精準計時**：詳細的時間分析，便於效能優化  
✅ **可重複測試**：支援快取與增量更新  
✅ **靈活配置**：支援自定義情境、向度和參數  
✅ **生產就緒**：完整的錯誤處理和日誌記錄  

### 下一步建議

1. **整合向量資料庫**：使用 Pinecone、Weaviate 或 Qdrant
2. **添加 Web 界面**：使用 Streamlit 或 Gradio
3. **實現用戶反饋**：收集並優化回答質量
4. **部署到雲端**：使用 Docker + Kubernetes
5. **監控與告警**：整合 Prometheus + Grafana

### 聯繫與支援

- **作者**: Jim
- **版本**: 1.0.0
- **更新日期**: 2025-10-08

---

**Happy Coding! 🚀**
