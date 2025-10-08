# 24 種情境系統使用指南

## 📋 系統概述

本系統實現了**方案 A**：基於四向度組合的 24 種情境自動匹配和調用。

### 核心組件

1. **`knowledge_relations.json`** - 知識點關聯關係定義
2. **`scenario_generator.py`** - 24 種情境自動生成器
3. **`scenario_matcher.py`** - 情境快速匹配和調用系統
4. **`scenarios_24/`** - 24 個情境文件目錄

---

## 🎯 24 種情境組合

### 組合計算

```
D1 (知識點數量): 3 種 × 
D2 (表達錯誤): 2 種 × 
D3 (表達詳細度): 3 種 × 
D4 (重複詢問): 2 種 
= 3 × 2 × 3 × 2 = 24 種組合
```

### 情境編號規則

| 編號 | D1 | D2 | D3 | D4 |
|------|----|----|----|----|
| 01 | 零個 | 有錯誤 | 非常詳細 | 重複狀態 |
| 02 | 零個 | 有錯誤 | 非常詳細 | 正常狀態 |
| 03 | 零個 | 有錯誤 | 粗略 | 重複狀態 |
| ... | ... | ... | ... | ... |
| 24 | 多個 | 無錯誤 | 未談及重點 | 正常狀態 |

---

## 🚀 快速開始

### 步驟 1：生成 24 種情境

```bash
python scenario_generator.py
```

這會在 `scenarios_24/` 目錄下生成 24 個 JSON 文件：
- `scenario_01.json` 到 `scenario_24.json`
- `index.json`（索引文件）

### 步驟 2：擴展情境內容

每個情境文件包含：
```json
{
  "id": "scenario_01",
  "scenario_number": 1,
  "name": "零個+有錯誤+非常詳細+重複狀態",
  "dimensions": {
    "D1": "零個",
    "D2": "有錯誤",
    "D3": "非常詳細",
    "D4": "重複狀態"
  },
  "description": "...",
  "response_strategy": {...},
  "prompt_template": "..."
}
```

**您需要做的**：
- 將 `prompt_template` 擴展到約 **5000 字**
- 添加具體的回答指引和範例
- 根據您的需求調整回答策略

### 步驟 3：測試情境匹配

```bash
python scenario_matcher.py
```

這會測試：
- 情境載入
- 維度匹配
- 提示詞生成

---

## 📚 知識點關聯系統

### 文件：`knowledge_relations.json`

定義了 3 個知識點之間的關聯關係：

#### 1. 單一知識點
```json
{
  "ml_basics": {
    "name": "機器學習基礎",
    "file": "ml_basics.txt",
    "description": "...",
    "keywords": [...]
  }
}
```

#### 2. 兩個知識點的關聯
```json
{
  "ml_basics_to_deep_learning": {
    "from": "ml_basics",
    "to": "deep_learning",
    "relation_type": "基礎到進階",
    "description": "深度學習是機器學習的一個重要分支",
    "key_connections": [...],
    "differences": [...],
    "when_to_mention": "..."
  }
}
```

#### 3. 三個知識點的關聯
```json
{
  "all_three": {
    "knowledge_points": ["ml_basics", "deep_learning", "nlp"],
    "relation_type": "完整技術棧",
    "hierarchy": {...},
    "learning_path": [...],
    "integration_points": [...]
  }
}
```

### 使用方式

當 D1 = "多個" 時，系統會：
1. 識別涉及的知識點
2. 從 `knowledge_relations.json` 中查找對應的關聯
3. 將關聯信息注入到提示詞中
4. AI 根據關聯信息回答

---

## 🔍 情境匹配流程

### 完整流程圖

```
用戶輸入問題
    ↓
RAG 檢索 → 匹配文件 → 提取知識點
    ↓
四向度分類
  ├─ D1: RAG 匹配判斷（零個/一個/多個）
  ├─ D2: AI 判斷表達錯誤
  ├─ D3: AI 判斷詳細度
  └─ D4: AI 分析歷史判斷重複
    ↓
生成維度組合鍵
例如: "一個|無錯誤|粗略|正常狀態"
    ↓
ScenarioMatcher.match_scenario()
    ↓
快速查找對應情境
例如: scenario_08
    ↓
獲取情境的 prompt_template
    ↓
如果 D1="多個"，從 knowledge_relations.json
獲取知識點關聯信息
    ↓
填充模板變量：
  - {query}: 用戶問題
  - {context}: RAG 上下文
  - {knowledge_points}: 知識點列表
  - {knowledge_relations}: 關聯信息
    ↓
生成完整提示詞
    ↓
發送給 LLM 生成最終答案
```

### 代碼示例

```python
from scenario_matcher import ScenarioMatcher

# 初始化匹配器
matcher = ScenarioMatcher()

# 四向度分類結果
dimensions = {
    "D1": "多個",
    "D2": "無錯誤",
    "D3": "非常詳細",
    "D4": "正常狀態"
}

# 匹配情境
scenario = matcher.match_scenario(dimensions)
print(f"匹配到情境: {scenario['scenario_number']}")

# 獲取完整提示詞
prompt = matcher.get_prompt(
    dimensions=dimensions,
    query="機器學習和深度學習有什麼區別？",
    context="[RAG 檢索到的內容]",
    knowledge_points=["機器學習基礎", "深度學習"]
)

# 發送給 LLM
response = llm.generate(prompt)
```

---

## 📝 情境文件結構

### 標準格式

```json
{
  "id": "scenario_XX",
  "scenario_number": XX,
  "name": "D1值+D2值+D3值+D4值",
  "dimensions": {
    "D1": "...",
    "D2": "...",
    "D3": "...",
    "D4": "..."
  },
  "description": "情境描述",
  "response_strategy": {
    "tone": "語氣風格",
    "structure": ["結構要點1", "結構要點2"],
    "emphasis": ["強調重點1", "強調重點2"],
    "length": "回答長度"
  },
  "prompt_template": "完整的提示詞模板（約5000字）"
}
```

### 提示詞模板變量

可用的變量：
- `{query}` - 用戶問題
- `{context}` - RAG 檢索到的上下文
- `{knowledge_points}` - 知識點列表（逗號分隔）
- `{knowledge_relations}` - 知識點關聯信息（僅當 D1="多個" 時有效）

---

## 🎯 擴展情境內容指南

### 建議的結構（5000 字）

#### 1. 情境說明（500 字）
- 這個情境的特點
- 用戶的典型狀態
- 回答的總體策略

#### 2. 回答指引（2000 字）
- 詳細的回答步驟
- 每個步驟的注意事項
- 語氣和用詞建議
- 結構化的回答框架

#### 3. 範例和模板（1500 字）
- 3-5 個具體範例
- 不同場景的應對方式
- 常見問題的回答模板

#### 4. 特殊處理（500 字）
- 邊界情況處理
- 錯誤處理
- 用戶引導策略

#### 5. 質量檢查（500 字）
- 回答質量標準
- 自我檢查清單
- 改進建議

### 範例：scenario_08（一個+無錯誤+粗略+正常狀態）

```
【情境說明】
這是最常見的情境之一。用戶提出了一個關於單一知識點的簡單問題，
表達正確但不夠詳細，這是首次詢問該問題。

【回答策略】
1. 直接回答問題的核心
2. 提供清晰的定義和解釋
3. 給出 1-2 個實例
4. 保持回答簡潔但完整
5. 語氣友好、專業

【回答結構】
第一段：直接回答核心問題（定義或概念）
第二段：詳細解釋（原理、特點）
第三段：實際應用或範例
第四段：總結或延伸

【範例 1：什麼是機器學習？】
[5000 字的詳細回答指引...]

【範例 2：深度學習的優化方法有哪些？】
[5000 字的詳細回答指引...]

...
```

---

## 🔧 系統集成

### 在 main.py 中使用

```python
from scenario_matcher import ScenarioMatcher

class RAGStreamSystem:
    def __init__(self):
        # ... 其他初始化 ...
        self.scenario_matcher = ScenarioMatcher()
    
    async def process_query(self, query, ...):
        # ... RAG 檢索 ...
        
        # 四向度分類
        dimensions = await self.classifier.classify(
            query, matched_docs, context
        )
        
        # 匹配情境
        scenario = self.scenario_matcher.match_scenario(dimensions)
        
        # 獲取提示詞
        prompt = self.scenario_matcher.get_prompt(
            dimensions=dimensions,
            query=query,
            context=context,
            knowledge_points=knowledge_points
        )
        
        # 生成答案
        answer = await self.generate_with_prompt(prompt)
        
        return {
            "answer": answer,
            "scenario_number": scenario['scenario_number'],
            "scenario_name": scenario['name'],
            "dimensions": dimensions
        }
```

### 在 Web API 中使用

```python
from scenario_matcher import ScenarioMatcher

matcher = ScenarioMatcher()

@app.post("/api/query")
async def process_query(request: QueryRequest):
    # ... 處理查詢 ...
    
    # 獲取情境信息
    scenario = matcher.match_scenario(dimensions)
    
    return {
        "answer": final_answer,
        "scenario": {
            "number": scenario['scenario_number'],
            "name": scenario['name'],
            "description": scenario['description']
        },
        "dimensions": dimensions
    }
```

---

## 📊 情境統計和分析

### 查看所有情境

```python
from scenario_matcher import ScenarioMatcher

matcher = ScenarioMatcher()
matcher.list_all_scenarios()
```

### 查看特定情境

```python
# 根據編號查看
scenario = matcher.get_scenario_by_number(16)
print(scenario)

# 根據維度查看
dimensions = {"D1": "一個", "D2": "無錯誤", "D3": "粗略", "D4": "正常狀態"}
matcher.print_scenario_info(dimensions)
```

---

## ✅ 檢查清單

### 系統設置
- [ ] 已生成 24 個情境文件
- [ ] 已擴展提示詞到約 5000 字
- [ ] 已定義知識點關聯關係
- [ ] 已更新 config.py 中的知識點映射

### 測試驗證
- [ ] 測試情境生成器
- [ ] 測試情境匹配器
- [ ] 測試知識點關聯提取
- [ ] 測試完整流程

### 文檔完整性
- [ ] 每個情境都有完整的描述
- [ ] 每個情境都有詳細的提示詞
- [ ] 知識點關聯已清楚標註
- [ ] 使用指南已完成

---

## 🎉 總結

本系統實現了：

1. ✅ **24 種情境自動生成**（方案 A）
2. ✅ **快速情境匹配**（O(1) 時間複雜度）
3. ✅ **知識點關聯管理**（JSON 格式）
4. ✅ **提示詞自動填充**（支持變量替換）
5. ✅ **完整的文檔和指南**

### 下一步

1. 執行 `python scenario_generator.py` 生成情境文件
2. 編輯 `scenarios_24/` 中的文件，擴展到 5000 字
3. 根據您的需求調整 `knowledge_relations.json`
4. 測試完整流程

**系統已就緒，可以開始擴展情境內容！** 🚀
