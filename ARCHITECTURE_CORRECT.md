# 正確的系統架構

## 🎯 核心流程

### 階段 1：並行分析（多線程）

```
用戶輸入問題
    ↓
┌─────────────────────────────────────────┐
│         並行啟動多個線程                 │
├─────────────────────────────────────────┤
│                                         │
│  線程 1: RAG 檢索                       │
│    └─ 檢索 docs/ 中的教材（5000字）     │
│    └─ 提取相關內容                      │
│    └─ 識別匹配的知識點                  │
│                                         │
│  線程 2: D1 分析                        │
│    └─ 基於 RAG 結果判斷知識點數量       │
│                                         │
│  線程 3: D2 分析                        │
│    └─ AI 判斷表達是否有錯誤             │
│                                         │
│  線程 4: D3 分析                        │
│    └─ AI 判斷表達詳細度                 │
│                                         │
│  線程 5: D4 分析                        │
│    └─ AI 分析歷史記錄判斷是否重複       │
│                                         │
└─────────────────────────────────────────┘
    ↓
等待所有線程完成
    ↓
初步整理結果
```

### 階段 2：情境判定與合併

```
收集並行分析結果
    ↓
確定四向度組合
例如：D1="一個", D2="無錯誤", D3="粗略", D4="正常狀態"
    ↓
ScenarioMatcher 快速查找
    ↓
判定：這是第 8 個情境（scenario_08）
    ↓
讀取 scenarios_24/scenario_08.json
    ↓
將該情境的 JSON 數據合併到主線程
```

### 階段 3：主線程處理

```
主線程接收：
  ├─ RAG 檢索結果（教材內容）
  ├─ 四向度分析結果
  └─ 情境 JSON 數據（scenario_08.json）
    ↓
合併所有數據
    ↓
構建完整上下文
    ↓
發送給 LLM 生成最終答案
    ↓
返回結果
```

---

## 📁 文件結構說明

### 教材文件（docs/）
```
docs/
├── ml_basics.txt          # 機器學習基礎教材（~5000字）
├── deep_learning.txt      # 深度學習教材（~5000字）
└── nlp_intro.txt          # NLP 教材（~5000字）
```
**用途**：RAG 檢索的來源，提供知識內容

### 情境文件（scenarios_24/）
```
scenarios_24/
├── scenario_01.json       # 情境 1 的配置和策略
├── scenario_02.json       # 情境 2 的配置和策略
├── ...
└── scenario_24.json       # 情境 24 的配置和策略
```
**用途**：當判定出是第幾個情境時，將整個 JSON 合併到主線程

### 情境 JSON 結構
```json
{
  "id": "scenario_08",
  "scenario_number": 8,
  "name": "一個+無錯誤+粗略+正常狀態",
  "dimensions": {
    "D1": "一個",
    "D2": "無錯誤",
    "D3": "粗略",
    "D4": "正常狀態"
  },
  "description": "...",
  "response_strategy": {
    "tone": "友好、專業",
    "structure": [...],
    "emphasis": [...],
    "length": "適中"
  },
  "prompt_template": "...",  // 您稍後會確認這部分
  "additional_guidance": "..."  // 其他指引
}
```

---

## 🔧 實現：並行處理架構

### 代碼實現

```python
import asyncio
from typing import Dict, Tuple

class ParallelRAGSystem:
    """並行處理的 RAG 系統"""
    
    async def process_query_parallel(self, query: str) -> Dict:
        """
        並行處理查詢
        
        Args:
            query: 用戶問題
            
        Returns:
            完整結果
        """
        # 階段 1：並行啟動多個分析任務
        print("🚀 啟動並行分析...")
        
        rag_task = self.rag_retrieval(query)
        d1_task = self.analyze_d1(query)  # 需要等 RAG 結果
        d2_task = self.analyze_d2(query)
        d3_task = self.analyze_d3(query)
        d4_task = self.analyze_d4(query)
        
        # 等待所有任務完成
        results = await asyncio.gather(
            rag_task,
            d2_task,  # D2 可以立即開始
            d3_task,  # D3 可以立即開始
            d4_task   # D4 需要歷史記錄
        )
        
        rag_result = results[0]
        d2_result = results[1]
        d3_result = results[2]
        d4_result = results[3]
        
        # D1 需要 RAG 結果
        d1_result = await self.analyze_d1_with_rag(rag_result)
        
        # 階段 2：判定情境
        print("🎯 判定情境...")
        
        dimensions = {
            "D1": d1_result,
            "D2": d2_result,
            "D3": d3_result,
            "D4": d4_result
        }
        
        scenario = self.scenario_matcher.match_scenario(dimensions)
        scenario_number = scenario['scenario_number']
        
        print(f"✅ 判定為第 {scenario_number} 個情境")
        
        # 階段 3：合併到主線程
        print("🔗 合併情境數據到主線程...")
        
        merged_context = self.merge_to_main_thread(
            rag_result=rag_result,
            dimensions=dimensions,
            scenario_data=scenario,
            query=query
        )
        
        # 階段 4：主線程處理
        print("⚙️  主線程處理...")
        
        final_answer = await self.main_thread_process(merged_context)
        
        return {
            "query": query,
            "final_answer": final_answer,
            "scenario_number": scenario_number,
            "scenario_name": scenario['name'],
            "dimensions": dimensions,
            "rag_context": rag_result['context'],
            "knowledge_points": rag_result['knowledge_points']
        }
    
    def merge_to_main_thread(
        self,
        rag_result: Dict,
        dimensions: Dict,
        scenario_data: Dict,
        query: str
    ) -> Dict:
        """
        將所有數據合併到主線程
        
        Args:
            rag_result: RAG 檢索結果
            dimensions: 四向度分析結果
            scenario_data: 情境 JSON 數據
            query: 用戶問題
            
        Returns:
            合併後的上下文
        """
        merged = {
            "query": query,
            "rag_context": rag_result['context'],
            "knowledge_points": rag_result['knowledge_points'],
            "matched_docs": rag_result['matched_docs'],
            "dimensions": dimensions,
            "scenario": scenario_data,  # 完整的情境 JSON
            "response_strategy": scenario_data['response_strategy'],
            "prompt_template": scenario_data.get('prompt_template', ''),
            "timestamp": datetime.now().isoformat()
        }
        
        # 如果涉及多個知識點，添加關聯信息
        if dimensions['D1'] == "多個":
            relations = self.get_knowledge_relations(
                rag_result['knowledge_points']
            )
            merged['knowledge_relations'] = relations
        
        return merged
    
    async def main_thread_process(self, context: Dict) -> str:
        """
        主線程處理
        
        Args:
            context: 合併後的完整上下文
            
        Returns:
            最終答案
        """
        # 構建提示詞（根據情境數據）
        prompt = self.build_prompt_from_context(context)
        
        # 調用 LLM
        response = await self.llm_generate(prompt)
        
        return response
    
    def build_prompt_from_context(self, context: Dict) -> str:
        """
        根據合併的上下文構建提示詞
        
        Args:
            context: 完整上下文
            
        Returns:
            提示詞
        """
        scenario = context['scenario']
        strategy = context['response_strategy']
        
        # 基礎提示詞
        prompt_parts = [
            "你是一個專業的知識助手。",
            f"\n【情境】第 {scenario['scenario_number']} 個情境",
            f"情境名稱：{scenario['name']}",
            f"情境描述：{scenario['description']}",
            f"\n【回答策略】",
            f"語氣：{strategy['tone']}",
            f"長度：{strategy['length']}",
            f"結構要點：{', '.join(strategy['structure'])}",
            f"強調重點：{', '.join(strategy['emphasis'])}",
        ]
        
        # 添加 RAG 檢索內容
        prompt_parts.append(f"\n【檢索到的教材內容】")
        prompt_parts.append(context['rag_context'])
        
        # 如果有知識點關聯
        if 'knowledge_relations' in context:
            prompt_parts.append(f"\n【知識點關聯】")
            prompt_parts.append(context['knowledge_relations'])
        
        # 添加用戶問題
        prompt_parts.append(f"\n【用戶問題】")
        prompt_parts.append(context['query'])
        
        # 添加情境的提示詞模板（如果有）
        if context['prompt_template']:
            prompt_parts.append(f"\n【具體指引】")
            prompt_parts.append(context['prompt_template'])
        
        prompt_parts.append("\n請根據以上情境和內容，生成適當的回答：")
        
        return "\n".join(prompt_parts)
```

---

## 📊 時間線對比

### 串行處理（舊方式）
```
RAG 檢索      [====] 1.0s
  ↓
D1 分析       [=] 0.2s
  ↓
D2 分析       [===] 0.5s
  ↓
D3 分析       [===] 0.5s
  ↓
D4 分析       [====] 0.8s
  ↓
情境匹配      [=] 0.1s
  ↓
LLM 生成      [========] 2.0s
────────────────────────────────
總計：5.1s
```

### 並行處理（新方式）
```
RAG 檢索      [====] 1.0s
D2 分析       [===] 0.5s  ┐
D3 分析       [===] 0.5s  ├─ 並行
D4 分析       [====] 0.8s ┘
  ↓
D1 分析       [=] 0.2s
  ↓
情境匹配      [=] 0.1s
  ↓
合併數據      [=] 0.1s
  ↓
LLM 生成      [========] 2.0s
────────────────────────────────
總計：3.2s（節省 37%）
```

---

## 🔄 數據流動

```
┌─────────────┐
│  用戶問題    │
└──────┬──────┘
       │
       ├─────────────────────────────────────┐
       │                                     │
   ┌───▼────┐  ┌────────┐  ┌────────┐  ┌────▼────┐
   │ RAG    │  │ D2 AI  │  │ D3 AI  │  │ D4 AI   │
   │ 檢索   │  │ 分析   │  │ 分析   │  │ 分析    │
   └───┬────┘  └───┬────┘  └───┬────┘  └────┬────┘
       │           │           │            │
       └───────┬───┴───────────┴────────────┘
               │
          ┌────▼─────┐
          │ D1 分析  │
          │(需RAG結果)│
          └────┬─────┘
               │
          ┌────▼──────┐
          │ 情境判定   │
          │(第X個情境) │
          └────┬──────┘
               │
          ┌────▼──────┐
          │ 讀取情境   │
          │ JSON 數據  │
          └────┬──────┘
               │
          ┌────▼──────┐
          │ 合併到     │
          │ 主線程     │
          └────┬──────┘
               │
          ┌────▼──────┐
          │ LLM 生成   │
          │ 最終答案   │
          └────┬──────┘
               │
          ┌────▼──────┐
          │ 返回結果   │
          └───────────┘
```

---

## ✅ 修正後的理解

### 正確的部分 ✅
1. 24 種情境組合
2. 快速匹配機制
3. 知識點關聯系統
4. 四向度分類邏輯

### 需要修正的部分 🔄
1. **教材內容**：5000 字是指 `docs/` 中的教材文件，不是提示詞模板
2. **並行處理**：系統會同時啟動多個線程進行分析
3. **數據合併**：判定出情境後，將該情境的 JSON 數據合併到主線程
4. **提示詞模板**：這部分您稍後會再確認

---

## 📝 您需要做的

### 1. 擴展教材內容到 5000 字
編輯 `docs/` 目錄中的文件：
- `ml_basics.txt` → 擴展到約 5000 字
- `deep_learning.txt` → 擴展到約 5000 字
- `nlp_intro.txt` → 擴展到約 5000 字

### 2. 生成 24 個情境文件
```bash
python scenario_generator.py
```

### 3. 稍後確認提示詞模板
您會再告訴我提示詞模板的具體格式和內容

---

非常感謝您的澄清！我現在理解正確了。系統會：
1. **並行分析**多個向度
2. **判定情境**（第幾個）
3. **合併 JSON 數據**到主線程
4. **主線程處理**並生成答案

請問這樣的理解是否正確？
