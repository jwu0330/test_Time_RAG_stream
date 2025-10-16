# K/C/R 三維度系統 - 架構說明

## 📅 更新日期：2025-10-15
## 🔧 系統版本：3.0（K/C/R 三維度分類）

---

## ✅ 核心簡化

### **RepetitionChecker（R 值檢測器）**

#### 簡化前
- 需要傳入歷史記錄
- 需要手動管理歷史
- 邏輯分散在多個地方

#### 簡化後
```python
class RepetitionChecker:
    def __init__(self):
        # 只記錄最近兩次的知識點集合
        self.history = deque(maxlen=2)
    
    def check_and_update(self, current_kps: List[str]) -> int:
        """
        檢查是否重複，然後更新歷史記錄
        
        邏輯：
        1. 找出前兩次共同出現的知識點
        2. 檢查當前知識點是否與共同知識點重疊
        3. 若有重疊 → 重複（返回1）
        4. 將當前知識點加入佇列（自動維持僅兩筆記錄）
        """
        if len(self.history) < 2:
            self.history.append(set(current_kps))
            return 0
        
        # 找出前兩次共同出現的知識點
        common = set(self.history[0]) & set(self.history[1])
        
        # 檢查當前知識點是否與共同知識點重疊
        current_set = set(current_kps)
        if current_set & common:
            self.history.append(current_set)
            return 1  # 重複
        
        self.history.append(current_set)
        return 0  # 正常
```

**優勢：**
- ✅ 只需 15 行代碼
- ✅ 自動管理歷史（deque(maxlen=2)）
- ✅ 一次調用完成檢查和更新

---

### **KnowledgeDetector（知識點檢測器）**

#### 簡化
- 移除 `history_knowledge` 參數
- 不需要傳入歷史記錄
- 只專注於檢測當前問題的知識點

```python
async def detect(self, query: str) -> List[str]:
    """
    檢測問題涉及的知識點
    
    Returns:
        List[str]: ["機器學習基礎", "深度學習"]
    """
    # 簡化的 API 調用
    # 只傳入當前問題和知識點清單
```

---

### **DimensionClassifier（集中管理器）**

#### 簡化
- 移除 `history` 參數
- R 值檢測內建歷史管理

```python
async def classify_all(self, query: str) -> Dict:
    """
    執行完整的維度分類流程
    
    流程：
    1. 並行執行 2 次 API 調用（C 值和知識點檢測）
    2. 計算 K 值（本地）
    3. 檢測 R 值並自動更新歷史（本地）
    4. 計算情境編號
    """
    # 並行執行 2 次 API 調用
    c_value, knowledge_points = await asyncio.gather(
        self.correctness_detector.detect(query),
        self.knowledge_detector.detect(query)
    )
    
    # 本地計算 K 值
    k_value = self.knowledge_detector.calculate_k_value(knowledge_points)
    
    # 檢測 R 值並更新歷史（一次完成）
    r_value = self.repetition_checker.check_and_update(knowledge_points)
    
    # 計算情境編號
    scenario_number = self.scenario_calculator.calculate(k_value, c_value, r_value)
    
    return {...}
```

---

### **ScenarioClassifier（情境分類器）**

#### 簡化
- 移除 `history` 和 `matched_docs` 參數
- 只需要 `query`

```python
async def classify(self, query: str) -> Dict:
    """判定情境（使用 K, C, R 三個維度）"""
    result = await self.dimension_classifier.classify_all(query)
    # ...
```

---

### **main_parallel.py（主程序）**

#### 簡化
- 移除歷史記錄的傳遞
- 簡化調用鏈

```python
# 簡化前
history = self.history_manager.get_recent_history(5)
history_list = [h.to_dict() for h in history]
result = await self.scenario_classifier.classify(query, history_list, matched_docs)

# 簡化後
result = await self.scenario_classifier.classify(query)
```

---

## 📊 完整執行流程

```
用戶問題：「什麼是深度學習？」
    ↓
【並行處理 - 3個API同時執行】
├─ Thread 1: RAG Embedding API（向量檢索）
├─ Thread 2: C值檢測 API（正確性判斷）
└─ Thread 3: 知識點檢測 API（識別知識點）
    ↓
【本地計算 - 幾乎無延遲】
├─ K值 = len(knowledge_points)  # 從知識點列表計算
└─ R值 = repetition_checker.check_and_update(knowledge_points)
    ├─ 內部自動檢查前兩次歷史
    ├─ 找出共同知識點
    ├─ 判斷是否重疊
    └─ 自動更新歷史記錄
    ↓
【計算情境編號】
scenario_number = k*4 + c*2 + r + 1  # 1-12
    ↓
【整合結果】
├─ RAG 上下文
├─ 情境提示詞
└─ 知識本體論
    ↓
【生成答案】
最終回合 API: 生成答案（流式輸出）
```

---

## 🎯 範例執行

### **第 1 次對話**
```python
query = "什麼是深度學習？"
knowledge_points = ["深度學習"]

# R 值檢測
repetition_checker.history = []  # 空的
r_value = 0  # 正常（歷史不足2筆）
repetition_checker.history = [{"深度學習"}]
```

### **第 2 次對話**
```python
query = "深度學習的應用？"
knowledge_points = ["深度學習"]

# R 值檢測
repetition_checker.history = [{"深度學習"}]  # 只有1筆
r_value = 0  # 正常（歷史不足2筆）
repetition_checker.history = [{"深度學習"}, {"深度學習"}]
```

### **第 3 次對話**
```python
query = "深度學習和機器學習的區別？"
knowledge_points = ["深度學習", "機器學習基礎"]

# R 值檢測
repetition_checker.history = [{"深度學習"}, {"深度學習"}]
common = {"深度學習"} & {"深度學習"} = {"深度學習"}
current = {"深度學習", "機器學習基礎"}
current & common = {"深度學習"}  # 有重疊！
r_value = 1  # 重複
repetition_checker.history = [{"深度學習"}, {"深度學習", "機器學習基礎"}]
```

---

## ✅ 優勢總結

1. **代碼更簡潔**
   - RepetitionChecker：從 70 行 → 15 行
   - 移除不必要的參數傳遞

2. **邏輯更清晰**
   - R 值檢測自動管理歷史
   - 一次調用完成檢查和更新

3. **維護更容易**
   - 歷史記錄集中在 RepetitionChecker
   - 不需要在多個地方傳遞歷史

4. **性能更好**
   - 使用 set 進行交集運算（O(n)）
   - deque 自動維護大小

---

## 📝 已更新的檔案

1. ✅ `core/tools/repetition_checker.py` - 簡化為 15 行
2. ✅ `core/tools/knowledge_detector.py` - 移除 history 參數
3. ✅ `core/dimension_classifier.py` - 移除 history 參數
4. ✅ `core/scenario_classifier.py` - 簡化參數
5. ✅ `main_parallel.py` - 簡化調用

---

## 🚀 測試

```bash
cd /mnt/c/Jim_Data/code/python/test_Time_RAG_stream
poetry run python main_parallel.py
```

**預期結果：**
- ✅ 第 1-2 次對話：R=0（正常）
- ✅ 第 3 次對話（相同知識點）：R=1（重複）
- ✅ 自動維護最近 2 筆歷史記錄

---

**簡化完成！系統現在更精簡、更高效。** 🎉
