# 情境判定 API 實作完成報告

## ✅ 已完成

### 1. **使用 OpenAI Function Calling 實作情境判定**

**位置**: `core/scenario_classifier.py`

**實作方式**: 選項 A - Function Calling（最精確）

**關鍵代碼**:
```python
functions = [{
    "name": "classify_dimensions",
    "description": "判定用戶問題的四個向度",
    "parameters": {
        "type": "object",
        "properties": {
            "D1": {"type": "string", "enum": ["零個", "一個", "多個"]},
            "D2": {"type": "string", "enum": ["有錯誤", "無錯誤"]},
            "D3": {"type": "string", "enum": ["粗略", "非常詳細"]},
            "D4": {"type": "string", "enum": ["重複狀態", "正常狀態"]}
        },
        "required": ["D1", "D2", "D3", "D4"]
    }
}]
```

---

## 🎯 實作流程

### 分支線程：情境判定

```
用戶提問
    ↓
【準備資料】
1. 用戶當前問題
2. 歷史對話記錄（最近5條）
3. 知識本體論內容
    ↓
【呼叫 OpenAI API】
使用 Function Calling
    ↓
【API 返回】
{
  "D1": "一個",
  "D2": "無錯誤",
  "D3": "非常詳細",
  "D4": "正常狀態"
}
    ↓
【查找情境】
根據四向度在 scenarios_24.json 中查找
    ↓
【返回結果】
{
  "scenario_number": 16,
  "dimensions": {...},
  "description": "...",
  "display_text": "當前情境：D1=一個, D2=無錯誤, D3=非常詳細, D4=正常狀態 → 第 16 種情境"
}
```

---

## 📋 傳遞給 API 的資訊

### 1. 知識本體論
```
【知識本體論】
# 知識本體論
# 用於提示詞模板，說明知識點之間的關係

知識節點
1. 機器學習基礎 (ml_basics)
2. 深度學習 (deep_learning)
3. 自然語言處理 (nlp)

節點關係
【機器學習基礎 → 深度學習】
深度學習是機器學習的進階分支...
...
```

### 2. 歷史對話記錄
```
【歷史對話】
Q: 什麼是機器學習？
知識點: 機器學習基礎
向度: {'D1': '一個', 'D2': '無錯誤', 'D3': '非常詳細', 'D4': '正常狀態'}

Q: 深度學習是什麼？
知識點: 深度學習
向度: {'D1': '一個', 'D2': '無錯誤', 'D3': '粗略', 'D4': '正常狀態'}
```

### 3. 當前問題
```
【當前問題】
機器學習和深度學習有什麼區別？
```

---

## 🔧 四向度判定邏輯

### D1 - 知識點數量
**判定方式**: AI 根據問題內容和本體論判斷

**範例**:
- "什麼是機器學習？" → **一個**（只涉及機器學習基礎）
- "機器學習和深度學習有什麼區別？" → **多個**（涉及兩個知識點）
- "你好" → **零個**（不涉及任何知識點）

### D2 - 表達錯誤
**判定方式**: AI 分析問題的語法和邏輯

**範例**:
- "什麼是機器學習？" → **無錯誤**
- "機器學習是不是就是深度學習？" → **有錯誤**（概念混淆）

### D3 - 表達詳細度
**判定方式**: AI 分析問題的完整性和具體性

**範例**:
- "ML" → **粗略**
- "請詳細解釋機器學習的工作原理，包括訓練過程和評估方法" → **非常詳細**

### D4 - 重複詢問
**判定方式**: AI 根據歷史記錄判斷是否重複

**範例**:
- 第一次問"什麼是機器學習？" → **正常狀態**
- 連續3次問同樣的問題 → **重複狀態**

---

## 🔄 與主系統的整合

### main_parallel.py 更新

```python
async def branch_thread_scenario(self, query: str) -> Dict:
    """分支：情境判定"""
    print("【分支】開始情境判定...")
    
    # 獲取歷史記錄
    history = self.history_manager.get_recent_history(limit=5)
    
    # 呼叫 API 進行四向度判定
    result = self.scenario_classifier.classify(query, history=history)
    
    print("【分支】情境判定完成")
    
    return result
```

---

## ✅ 優勢

### 使用 Function Calling 的好處

1. **強制格式** ✅
   - API 保證返回正確的 JSON 格式
   - 不會有解析錯誤

2. **類型安全** ✅
   - enum 限制只能返回預定義的值
   - 不會出現 "一個知識點" 這種錯誤格式

3. **更可靠** ✅
   - OpenAI 會確保 function call 的參數符合 schema
   - 降級處理：API 失敗時返回錯誤資訊

4. **更精確** ✅
   - AI 明確知道要返回什麼格式
   - 減少歧義

---

## 🧪 測試方式

### 測試情境判定 API
```bash
python3 test_scenario_api.py
```

### 測試完整系統
```bash
python3 main_parallel.py
```

### 測試 Web API
```bash
python3 web_api.py
# 然後訪問 http://localhost:8000/docs
```

---

## 📊 API 呼叫示例

### 請求
```python
{
    "query": "機器學習和深度學習有什麼區別？",
    "history": [
        {
            "query": "什麼是機器學習？",
            "knowledge_points": ["機器學習基礎"],
            "dimensions": {"D1": "一個", "D2": "無錯誤", "D3": "非常詳細", "D4": "正常狀態"}
        }
    ]
}
```

### 回應
```python
{
    "scenario_number": 22,
    "dimensions": {
        "D1": "多個",
        "D2": "無錯誤",
        "D3": "粗略",
        "D4": "正常狀態"
    },
    "description": "多個 + 無錯誤 + 粗略 + 正常狀態",
    "display_text": "當前情境：D1=多個, D2=無錯誤, D3=粗略, D4=正常狀態 → 第 22 種情境"
}
```

---

## ⚠️ 注意事項

### 1. API Key
確保設定了 OpenAI API Key：
```bash
export OPENAI_API_KEY="your-api-key"
```

### 2. 成本
每次情境判定會呼叫一次 GPT-4 API，請注意成本。

### 3. 錯誤處理
如果 API 呼叫失敗，系統會返回錯誤資訊但不會崩潰。

---

## 🎉 總結

✅ **實作完成**：使用 Function Calling 實作情境判定  
✅ **傳遞本體論**：AI 知道有哪些知識節點  
✅ **傳遞歷史**：AI 可以判斷是否重複  
✅ **精確判定**：強制格式，保證正確性  
✅ **完整整合**：已整合到主系統  

**系統已準備就緒，可以開始使用！** 🚀
