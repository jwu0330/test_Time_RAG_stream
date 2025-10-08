# 雙線程計時系統說明

**更新時間**: 2025-10-08  
**版本**: 2.0 - 支援雙線程獨立計時

---

## 📊 概述

本系統實現了精確的雙線程計時機制，能夠獨立追蹤 **Thread A（主線：RAG）** 和 **Thread B（分支：情境判定）** 在各個階段的執行時間。

### 計時原則

✅ **後端計時**：所有時間測量在後端進行，不受前端渲染影響  
✅ **精確測量**：使用 `time.perf_counter()` 提供納秒級精度  
✅ **獨立追蹤**：兩個線程的時間分別記錄，互不干擾  
✅ **完整報告**：提供主流程、Thread A、Thread B 的詳細時間分解

---

## 🔄 系統架構與計時點

### 整體流程

```
用戶問題（前端）
    ↓
📥 後端接收（計時起點）
    ↓
┌─────────────────────────────────────┐
│   並行處理階段                        │
│                                     │
│   Thread A (主線)    Thread B (分支) │
│   ├─ RAG檢索        ├─ 獲取歷史      │
│   └─ 草稿生成       └─ 四向度判定    │
│                                     │
└─────────────────────────────────────┘
    ↓
會診合併（整合兩條線的結果）
    ↓
📤 後端轉發（計時終點）
    ↓
前端渲染（不計入後端時間）
```

---

## ⏱️ 計時階段詳解

### 主流程計時

| 階段名稱 | 說明 | 包含內容 |
|---------|------|---------|
| **總流程** | 從開始到結束的總時間 | 所有階段的總和 |
| **並行處理（總時間）** | 兩個線程並行執行的時間 | Thread A 和 B 同時運行的時間 |
| **會診合併** | 合併結果並生成最終答案 | 整合兩條線的結果，生成最終回答 |

### Thread A（主線：RAG）計時

| 階段名稱 | 說明 | 主要操作 |
|---------|------|---------|
| **RAG檢索** | 向量檢索和文檔匹配 | - 向量相似度計算<br>- 檢索 top-k 文檔<br>- 提取知識點 |
| **草稿生成** | 生成初步答案 | - 構建提示詞<br>- 調用 LLM API<br>- 生成草稿回答 |

### Thread B（分支：情境判定）計時

| 階段名稱 | 說明 | 主要操作 |
|---------|------|---------|
| **獲取歷史** | 讀取歷史查詢記錄 | - 從 history.json 讀取<br>- 提取最近 5 筆記錄 |
| **四向度判定** | 分析四個維度 | - D1: 知識點數量<br>- D2: 表達錯誤<br>- D3: 表達詳細度<br>- D4: 重複詢問<br>- 調用 LLM API 判定 |

---

## 📈 計時報告格式

### 控制台輸出格式

```
======================================================================
⏱️  時間分析報告（雙線程）
======================================================================

【主流程】
  總流程                          :  5.234s
  並行處理（總時間）              :  3.456s
  會診合併                        :  1.234s

【Thread A (RAG)】
  RAG檢索                         :  1.234s
  草稿生成                        :  2.123s
  Thread A 小計                   :  3.357s

【Thread B (Scenario)】
  獲取歷史                        :  0.012s
  四向度判定                      :  3.421s
  Thread B 小計                   :  3.433s

----------------------------------------------------------------------
  總計（從後端接收到渲染完成）    :  5.234s
======================================================================
```

### API 響應格式（JSON）

```json
{
  "answer": "最終答案內容...",
  "dimensions": {
    "D1": "一個",
    "D2": "正確",
    "D3": "簡略",
    "D4": "首次"
  },
  "matched_docs": ["ml_basics.txt"],
  "knowledge_points": ["機器學習基礎"],
  "scenario": "第 1 種情境",
  "scenario_number": 1,
  "scenario_description": "...",
  "response_time": 5.234,
  "timing_details": {
    "backend_total": 5.234,
    "stages": {
      "總流程": 5.234,
      "並行處理（總時間）": 3.456,
      "會診合併": 1.234
    },
    "thread_a": {
      "thread_name": "Thread A (RAG)",
      "stages": {
        "RAG檢索": 1.234,
        "草稿生成": 2.123
      },
      "total_time": 3.357
    },
    "thread_b": {
      "thread_name": "Thread B (Scenario)",
      "stages": {
        "獲取歷史": 0.012,
        "四向度判定": 3.421
      },
      "total_time": 3.433
    },
    "timestamp": "2025-10-08T19:10:46.123456"
  }
}
```

---

## 🔍 時間分析要點

### 並行效率

由於 Thread A 和 Thread B 是並行執行的，實際的並行處理時間約等於兩者中較長的那個：

```
並行處理時間 ≈ max(Thread A 時間, Thread B 時間)
```

**範例**：
- Thread A 總時間：3.357s
- Thread B 總時間：3.433s
- 實際並行時間：3.456s（約等於較長的 Thread B）

### 效率提升

如果不使用並行處理，總時間會是：

```
串行總時間 = Thread A 時間 + Thread B 時間
並行總時間 = max(Thread A 時間, Thread B 時間)
效率提升 = (串行總時間 - 並行總時間) / 串行總時間 × 100%
```

**範例計算**：
- 串行總時間：3.357 + 3.433 = 6.790s
- 並行總時間：3.456s
- 效率提升：(6.790 - 3.456) / 6.790 × 100% ≈ **49.1%**

---

## 💻 使用方式

### 1. 命令行模式

```bash
python3 main_parallel.py
```

計時報告會自動打印到控制台。

### 2. Web API 模式

```bash
# 啟動後端
python3 web_api.py

# 發送請求（使用 curl）
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "什麼是機器學習？"}'
```

響應中的 `timing_details` 欄位包含完整計時資訊。

### 3. 前端界面

```bash
# 啟動後端
python3 web_api.py

# 在瀏覽器打開
open web/index.html
```

前端會顯示 `response_time`（後端總處理時間）。

---

## 🛠️ 技術實現

### 計時器類別（timer_utils.py）

```python
class Timer:
    """計時器管理類 - 支援雙線程獨立計時"""
    
    def __init__(self):
        self.records: Dict[str, TimerRecord] = {}
        self.thread_a_records: Dict[str, TimerRecord] = {}  # Thread A
        self.thread_b_records: Dict[str, TimerRecord] = {}  # Thread B
        self.start_time = time.perf_counter()
    
    def start_stage(self, stage_name: str, thread: Optional[str] = None):
        """開始計時，thread='A' 或 'B' 或 None"""
        ...
    
    def stop_stage(self, stage_name: str, thread: Optional[str] = None):
        """停止計時"""
        ...
```

### 使用範例

```python
# 主流程計時
self.timer.start_stage("總流程")

# Thread A 計時
self.timer.start_stage("RAG檢索", thread='A')
# ... 執行 RAG 檢索 ...
self.timer.stop_stage("RAG檢索", thread='A')

# Thread B 計時
self.timer.start_stage("四向度判定", thread='B')
# ... 執行情境判定 ...
self.timer.stop_stage("四向度判定", thread='B')

# 生成報告
report = self.timer.get_report()
```

---

## 📊 性能基準

### 典型時間分布（參考值）

| 階段 | 預期時間 | 說明 |
|-----|---------|------|
| RAG檢索 | 0.5-1.5s | 取決於向量庫大小 |
| 草稿生成 | 1.5-3.0s | 取決於 LLM API 響應速度 |
| 獲取歷史 | 0.01-0.05s | 本地文件讀取，非常快 |
| 四向度判定 | 2.0-4.0s | 取決於 LLM API 響應速度 |
| 會診合併 | 1.0-2.0s | 取決於 LLM API 響應速度 |
| **總計** | **4.0-7.0s** | 端到端處理時間 |

### 優化建議

1. **向量檢索優化**
   - 使用更高效的向量索引（如 FAISS）
   - 減少 top_k 數量

2. **LLM API 優化**
   - 使用更快的模型（如 gpt-3.5-turbo）
   - 減少 max_tokens
   - 使用流式輸出

3. **並行優化**
   - 確保兩個線程的時間盡量平衡
   - 避免一個線程過長導致等待

---

## 🔧 故障排除

### 問題：計時報告顯示 0.000s

**原因**：計時器未正確啟動或停止

**解決**：
```python
# 確保成對調用
self.timer.start_stage("階段名稱", thread='A')
# ... 執行代碼 ...
self.timer.stop_stage("階段名稱", thread='A')
```

### 問題：Thread A 或 B 的報告缺失

**原因**：未使用 `thread` 參數

**解決**：
```python
# 錯誤：缺少 thread 參數
self.timer.start_stage("RAG檢索")

# 正確：指定 thread='A'
self.timer.start_stage("RAG檢索", thread='A')
```

### 問題：並行時間異常長

**原因**：可能存在阻塞操作

**解決**：
- 檢查是否有同步 I/O 操作
- 確保使用 `async/await` 正確處理異步操作
- 使用 `asyncio.gather()` 並行執行

---

## 📝 總結

### 計時系統特點

✅ **精確**：納秒級精度，使用 `time.perf_counter()`  
✅ **獨立**：Thread A 和 B 分別計時，互不干擾  
✅ **完整**：涵蓋所有關鍵階段  
✅ **後端**：不受前端渲染影響  
✅ **詳細**：提供多層次的時間分解

### 關鍵時間點

1. **後端接收**：用戶查詢到達後端（計時起點）
2. **並行處理**：Thread A 和 B 同時執行
3. **會診合併**：整合結果並生成最終答案
4. **後端轉發**：準備發送給前端（計時終點）
5. **前端渲染**：顯示結果（不計入後端時間）

### 時間計算公式

```
後端總時間 = 並行處理時間 + 會診合併時間
並行處理時間 ≈ max(Thread A 時間, Thread B 時間)
Thread A 時間 = RAG檢索 + 草稿生成
Thread B 時間 = 獲取歷史 + 四向度判定
```

---

## 📞 相關文檔

- **系統架構**：[ARCHITECTURE_CHECK.md](ARCHITECTURE_CHECK.md)
- **執行指南**：[EXECUTION_GUIDE.md](EXECUTION_GUIDE.md)
- **Web 界面**：[WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md)
- **完整文檔**：[README_FULL.md](README_FULL.md)

---

**最後更新**: 2025-10-08  
**維護者**: 系統開發團隊
