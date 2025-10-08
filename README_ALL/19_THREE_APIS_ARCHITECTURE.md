# 三個 API + 本地計算架構

**📅 更新日期**: 2025-01-09  
**📚 版本**: 3.0 - 簡化版本

---

## 🎯 架構概述

### 從四個 API 到三個 API

**舊版（4個 API）**：
- D1 API - 知識點數量判定
- D2 API - 表達錯誤判定
- D3 API - 表達詳細度判定
- D4 本地邏輯 - 重複判定

**新版（3個 API + 本地計算）**：
- D2 API - 表達錯誤判定
- D3 API - 表達詳細度判定
- D4 API - **知識點檢測**（返回二進制編碼）
- D1 本地計算 - 從 D4 的二進制編碼計算知識點數量
- D4 本地判定 - 從歷史檢查重複

---

## 📊 三個 API 設計

### 1. D2 API - 表達錯誤判定

**輸入**: 當前問題  
**輸出**: `0` (無錯誤) 或 `1` (有錯誤)  
**需要歷史**: ❌ 否

```python
async def classify_d2_has_error(query: str) -> int:
    # 判定問題是否有錯誤或矛盾
    return 0 or 1
```

### 2. D3 API - 表達詳細度判定

**輸入**: 當前問題  
**輸出**: `0` (粗略) 或 `1` (非常詳細)  
**需要歷史**: ❌ 否

```python
async def classify_d3_detail_level(query: str) -> int:
    # 判定問題的詳細程度
    return 0 or 1
```

### 3. D4 API - 知識點檢測

**輸入**: 當前問題  
**輸出**: 二進制字符串（例如 `"1011"`）  
**需要歷史**: ❌ 否

```python
async def classify_d4_knowledge_detection(query: str) -> str:
    # 判定當前問題觸及了哪些知識點
    # 返回二進制編碼，例如 "1011" 表示觸及第0,2,3個知識點
    return "1011"
```

**二進制編碼說明**：
- 位置 0: 機器學習基礎
- 位置 1: 深度學習
- 位置 2: 自然語言處理
- 位置 3: 保留

---

## 🔧 本地計算

### D1 - 知識點數量計算

**輸入**: D4 API 返回的二進制編碼  
**輸出**: `0` (零個), `1` (一個), `2` (多個)  
**計算方式**: 計算二進制中 `1` 的個數

```python
def calculate_d1(binary: str) -> int:
    count = binary.count('1')
    if count == 0:
        return 0  # 零個
    elif count == 1:
        return 1  # 一個
    else:
        return 2  # 多個 (>= 2)
```

**示例**：
- `"1011"` → count = 3 → D1 = 2 (多個)
- `"1000"` → count = 1 → D1 = 1 (一個)
- `"0000"` → count = 0 → D1 = 0 (零個)

### D4 - 重複判定（優化版）

**輸入**: 
- 當前二進制編碼（從 D4 API 獲得）
- 歷史二進制編碼列表

**輸出**: `0` (正常) 或 `1` (重複)

**優化邏輯**：
只檢查當前觸及的知識點（值為 `1` 的位置）是否在歷史中也連續為 `1`

```python
def classify_d4_repetition(current_binary: str, history_binaries: list) -> int:
    if len(history_binaries) < 2:
        return 0
    
    recent_2 = history_binaries[-2:]
    
    # 只檢查當前為 "1" 的位置
    for pos in range(len(current_binary)):
        if current_binary[pos] == '1':
            # 檢查這個位置在歷史最近2筆是否也都為 "1"
            if all(history[pos] == '1' for history in recent_2):
                return 1  # 該位置連續3次為 "1"
    
    return 0
```

**示例**：
```
當前: "1011" (第0,2,3位為1)
歷史: ["1010", "1001"]

檢查：
- 第0位: 當前=1, 歷史=[1,1] → 連續3次為1 ✓ 重複！
- 第2位: 當前=1, 歷史=[1,0] → 不連續
- 第3位: 當前=1, 歷史=[0,1] → 不連續

結果: D4=1 (重複)
```

---

## 🚀 執行流程

### 並行執行（3個 API）

```python
# 並行調用 D2, D3, D4 API
results = await asyncio.gather(
    classify_d2_has_error(query),
    classify_d3_detail_level(query),
    classify_d4_knowledge_detection(query)
)

d2 = results[0]  # 0/1
d3 = results[1]  # 0/1
current_binary = results[2]  # "1011"
```

### 本地計算

```python
# D1: 從 D4 的二進制編碼計算
count = count_knowledge_points(current_binary)
d1 = 0 if count == 0 else 1 if count == 1 else 2

# D4 重複判定: 檢查歷史
d4 = classify_d4_repetition(current_binary, history_binaries)
```

### 完整結果

```python
{
    "D1": d1,                    # 0/1/2 (本地計算)
    "D2": d2,                    # 0/1 (API)
    "D3": d3,                    # 0/1 (API)
    "D4": d4,                    # 0/1 (本地判定)
    "knowledge_binary": current_binary  # 二進制編碼
}
```

---

## ✨ 優化效果

### API 調用優化
- **優化前**: 4個 API 調用
- **優化後**: 3個 API 調用
- **減少**: 25%

### 計算效率優化
- **D1**: 不再需要 API，本地計算（幾乎無延遲）
- **D4 重複判定**: 只檢查當前觸及的知識點（節省 25-100% 檢查時間）

### 邏輯清晰度
- **D4 API 職責明確**: 只負責判定知識點
- **本地計算職責明確**: D1 計算數量，D4 判定重複
- **無 RAG 依賴**: D4 API 不再依賴 RAG 結果

---

## 📝 總結

**當前架構（3個 API + 本地計算）**：
- ✅ 減少 API 調用次數
- ✅ 提高計算效率
- ✅ 邏輯更清晰
- ✅ 無 RAG 依賴
- ✅ 優化重複判定

系統更簡潔、更高效！
