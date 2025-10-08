# 五個並行分支架構

**📅 更新日期**: 2025-10-08  
**📚 版本**: 3.0 - 五個並行分支

---

## 🎯 架構概述

### 從雙線程到五個並行分支

**舊版（雙線程）**：
```
Thread A: RAG 檢索
Thread B: 情境判定（單一 API）
```

**新版（五個並行分支）**：
```
Thread A: RAG 檢索
Thread B: D1 知識點數量判定
Thread C: D2 表達錯誤判定
Thread D: D3 表達詳細度判定
Thread E: D4 重複詢問判定
```

---

## 📊 並行架構圖

```
用戶查詢
    │
    ├─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
    │                 │             │             │             │             │
Thread A        Thread B      Thread C      Thread D      Thread E
RAG 檢索        D1 判定       D2 判定       D3 判定       D4 判定
(向量檢索)      (知識點數量)  (表達錯誤)    (詳細度)      (重複詢問)
    │                 │             │             │             │
    │                 └─────────────┴─────────────┴─────────────┘
    │                                   │
    │                            計算情境編號 (1-24)
    │                                   │
    └───────────────────────────────────┘
                    │
            最終回合生成答案
                    │
                返回結果
```

---

## ⏱️ 時間記錄架構

### 主流程時間
- `向量化`: 初始化時的向量化時間
- `並行處理（5個分支）`: 五個分支的總並行時間
- `最終回合生成`: 最終答案生成時間
- `總流程`: 整體處理時間

### Thread A（RAG 檢索）
- `RAG檢索`: 向量檢索時間

### Thread B（D1 判定）
- `D1 API 調用`: D1 知識點數量判定時間

### Thread C（D2 判定）
- `D2 API 調用`: D2 表達錯誤判定時間

### Thread D（D3 判定）
- `D3 API 調用`: D3 表達詳細度判定時間

### Thread E（D4 判定）
- `D4 API 調用`: D4 重複詢問判定時間

---

## 🔄 執行流程

### 1. 初始化階段

```python
system = ResponsesRAGSystem()
await system.initialize_documents()

# 計時器自動注入到所有模組
system.scenario_classifier.set_timer(system.timer)
```

### 2. 第一回合：五個並行分支

```python
# 並行執行
rag_result, scenario_result = await asyncio.gather(
    self.main_thread_rag(query),              # Thread A
    self.parallel_dimension_classification(query)  # Thread B, C, D, E
)

# parallel_dimension_classification 內部並行執行四個 API
results = await asyncio.gather(
    self.classify_d1_knowledge_count(query, history),  # Thread B
    self.classify_d2_has_error(query),                  # Thread C
    self.classify_d3_detail_level(query),               # Thread D
    self.classify_d4_repetition(query, history)         # Thread E
)
```

### 3. 計算情境編號

```python
# 後端自行計算（不依賴 AI）
scenario_number = dimensions_to_scenario_number(dimensions)
# 公式: D1*8 + D2*4 + D3*2 + D4 + 1
```

### 4. 第二回合：最終生成

```python
final_answer = await self.final_round_generate(
    rag_result, 
    scenario_result, 
    query
)
```

---

## 📈 性能分析

### 時間報告示例

```
======================================================================
⏱️  時間分析報告（五個並行分支）
======================================================================

【主流程 - 總體時間】
  向量化                                :  0.000s
  並行處理（5個分支）                   :  0.850s
  最終回合生成                          :  2.150s

【Thread A（RAG 檢索）】
  RAG檢索                              :  0.708s
  ─────────────────────────────────────────────
  小計                                 :  0.708s

【Thread B（D1 知識點數量）】
  D1 API 調用                          :  0.345s
  ─────────────────────────────────────────────
  小計                                 :  0.345s

【Thread C（D2 表達錯誤）】
  D2 API 調用                          :  0.298s
  ─────────────────────────────────────────────
  小計                                 :  0.298s

【Thread D（D3 表達詳細度）】
  D3 API 調用                          :  0.312s
  ─────────────────────────────────────────────
  小計                                 :  0.312s

【Thread E（D4 重複詢問）】
  D4 API 調用                          :  0.276s
  ─────────────────────────────────────────────
  小計                                 :  0.276s

──────────────────────────────────────────────────────────────────────
  並行處理最大時間                      :  0.708s
  若順序執行需要                        :  1.939s
  並行效率提升                          : 63.5%

======================================================================
  🎯 總計時間                          :  3.000s
======================================================================
```

### 性能指標

| 指標 | 順序執行 | 並行執行 | 提升 |
|------|---------|---------|------|
| RAG 檢索 | 0.708s | 0.708s | - |
| D1 判定 | 0.345s | 0.345s | - |
| D2 判定 | 0.298s | 0.298s | - |
| D3 判定 | 0.312s | 0.312s | - |
| D4 判定 | 0.276s | 0.276s | - |
| **總計** | **1.939s** | **0.708s** | **63.5%** |

**並行時間 = max(所有分支時間) = 0.708s**

---

## 💡 並行效率計算

### 公式

```python
並行處理最大時間 = max(Thread A, Thread B, Thread C, Thread D, Thread E)
若順序執行需要 = sum(Thread A, Thread B, Thread C, Thread D, Thread E)
並行效率提升 = (1 - 並行處理最大時間 / 若順序執行需要) * 100%
```

### 示例

```python
並行處理最大時間 = max(0.708, 0.345, 0.298, 0.312, 0.276) = 0.708s
若順序執行需要 = 0.708 + 0.345 + 0.298 + 0.312 + 0.276 = 1.939s
並行效率提升 = (1 - 0.708 / 1.939) * 100% = 63.5%
```

---

## 🔧 代碼實現

### Timer 支持五個線程

```python
class Timer:
    def __init__(self):
        self.thread_a_records = {}  # Thread A: RAG 檢索
        self.thread_b_records = {}  # Thread B: D1 判定
        self.thread_c_records = {}  # Thread C: D2 判定
        self.thread_d_records = {}  # Thread D: D3 判定
        self.thread_e_records = {}  # Thread E: D4 判定
```

### 計時方法

```python
# Thread A
self.timer.start_stage("RAG檢索", thread='A')
# ... RAG 檢索邏輯
self.timer.stop_stage("RAG檢索", thread='A')

# Thread B
self.timer.start_stage("D1 API 調用", thread='B')
# ... D1 判定邏輯
self.timer.stop_stage("D1 API 調用", thread='B')

# Thread C, D, E 同理
```

### 並行執行

```python
# 在 dimension_classifiers.py
async def classify_all_parallel(self, query, history):
    results = await asyncio.gather(
        self.classify_d1_knowledge_count(query, history),
        self.classify_d2_has_error(query),
        self.classify_d3_detail_level(query),
        self.classify_d4_repetition(query, history)
    )
    return {
        "D1": results[0],
        "D2": results[1],
        "D3": results[2],
        "D4": results[3]
    }
```

---

## ✅ 確保真正並行

### 關鍵點

1. **使用 async/await**
   ```python
   async def classify_d1_knowledge_count(self, query, history):
       # 異步函數
   ```

2. **使用 asyncio.gather**
   ```python
   results = await asyncio.gather(
       task1, task2, task3, task4
   )
   ```

3. **獨立計時**
   - 每個線程有獨立的計時記錄
   - 不會互相干擾

4. **無共享狀態**
   - 每個 API 調用獨立
   - 只讀取歷史，不修改

---

## 📊 JSON 輸出格式

```json
{
  "timestamp": "2025-10-08T22:00:00",
  "stages": {
    "向量化": 0.000,
    "並行處理（5個分支）": 0.850,
    "最終回合生成": 2.150
  },
  "thread_a": {
    "thread_name": "Thread A（RAG 檢索）",
    "stages": {
      "RAG檢索": 0.708
    },
    "total_time": 0.708
  },
  "thread_b": {
    "thread_name": "Thread B（D1 知識點數量）",
    "stages": {
      "D1 API 調用": 0.345
    },
    "total_time": 0.345
  },
  "thread_c": {
    "thread_name": "Thread C（D2 表達錯誤）",
    "stages": {
      "D2 API 調用": 0.298
    },
    "total_time": 0.298
  },
  "thread_d": {
    "thread_name": "Thread D（D3 表達詳細度）",
    "stages": {
      "D3 API 調用": 0.312
    },
    "total_time": 0.312
  },
  "thread_e": {
    "thread_name": "Thread E（D4 重複詢問）",
    "stages": {
      "D4 API 調用": 0.276
    },
    "total_time": 0.276
  },
  "total_time": 3.000
}
```

---

## 🎯 優勢總結

### 1. **精準度提升**
- ✅ 每個向度獨立判定
- ✅ 專門的提示詞優化
- ✅ 後端自行計算情境編號

### 2. **性能優化**
- ✅ 五個分支真正並行
- ✅ 時間 = max(所有分支)
- ✅ 效率提升 60%+

### 3. **時間透明**
- ✅ 每個分支獨立計時
- ✅ 顯示並行效率
- ✅ 易於性能調優

### 4. **可維護性**
- ✅ 每個 API 獨立
- ✅ 易於測試和調試
- ✅ 易於擴展

---

## 📚 相關文檔

- [四向度獨立 API 設計](19_FOUR_DIMENSION_APIS.md)
- [性能優化指南](18_PERFORMANCE_OPTIMIZATION.md)
- [時間記錄更新](17_TIMING_UPDATES.md)

---

**五個並行分支架構完成，確保真正並行，無時間浪費！** ⚡🚀
