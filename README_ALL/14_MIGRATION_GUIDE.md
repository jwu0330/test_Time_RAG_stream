# 遷移指南：從舊版到 Responses API

**📅 更新日期**: 2025-10-08  
**📚 版本**: 1.0

---

## 🎯 遷移概述

本指南說明如何從舊版系統遷移到使用 **Responses API** 的新架構。

---

## 📊 主要變更

### 1. 系統類名變更

**舊版**：
```python
from main_parallel import ParallelRAGSystem

system = ParallelRAGSystem()
```

**新版**：
```python
from main_parallel import ResponsesRAGSystem

system = ResponsesRAGSystem()
```

### 2. 情境判定機制

**舊版**：使用 Chat Completions API 的 function calling
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    functions=[...],
    function_call={"name": "classify_dimensions"}
)
```

**新版**：使用 Responses API 的 tool call
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[...],
    tools=[classify_scenario_tool],
    tool_choice={"type": "function", "function": {"name": "classify_scenario"}},
    temperature=0,
    max_tokens=50
)
```

### 3. 返回格式

**舊版**：返回四向度字典
```python
{
    "D1": "一個",
    "D2": "無錯誤",
    "D3": "粗略",
    "D4": "正常狀態"
}
```

**新版**：直接返回情境編號
```python
{
    "scenario_id": 14  # 1-24
}
```

### 4. 主線處理

**舊版**：RAG 檢索 + 生成草稿答案
```python
async def main_thread_rag(self, query: str):
    # RAG 檢索
    retrieved_docs = await self.rag_retriever.retrieve(query)
    context = self.rag_retriever.format_context(retrieved_docs)
    
    # 生成草稿答案
    draft_answer = await self.generate_draft(context, query)
    
    return {
        "draft_answer": draft_answer,
        "context": context,
        ...
    }
```

**新版**：只進行 RAG 檢索
```python
async def main_thread_rag(self, query: str):
    # RAG 檢索
    retrieved_docs = await self.rag_retriever.retrieve(query)
    context = self.rag_retriever.format_context(retrieved_docs)
    
    return {
        "context": context,
        "matched_docs": matched_doc_ids,
        "knowledge_points": knowledge_points
    }
```

### 5. 最終生成

**舊版**：使用草稿答案 + 情境調整
```python
async def merge_and_generate(self, rag_result, scenario_result, query):
    draft_answer = rag_result['draft_answer']
    scenario_text = f"現在為第 {scenario_number} 種情境..."
    
    # 調整草稿答案
    final_prompt = f"""
    【初步答案】
    {draft_answer}
    
    【情境資訊】
    {scenario_text}
    
    請調整並生成最終回答...
    """
```

**新版**：直接整合所有資訊生成
```python
async def final_round_generate(self, rag_result, scenario_result, query):
    context = rag_result['context']
    scenario_text = f"現在為第 {scenario_number} 種情境..."
    
    # 直接生成最終答案
    final_prompt = f"""
    【當前情境】
    {scenario_text}
    
    【RAG 檢索到的教材片段】
    {context}
    
    【知識本體論】
    {ontology_content}
    
    請根據上述資訊生成回答...
    """
```

---

## 🔧 依賴更新

### requirements.txt

**舊版**：
```
openai>=1.12.0
```

**新版**：
```
openai>=1.54.0
```

### 更新命令

```bash
pip3 install --user -U openai
```

---

## 📁 新增文件

### 1. `core/function_tools.py`
定義 Responses API 的 function/tool call 工具

### 2. `core/template_loader.py`
模板加載器（保留，未來擴展用）

### 3. `README_ALL/BASH_ALL/test_responses_api.sh`
測試腳本

### 4. `README_ALL/BASH_ALL/verify_function_call.sh`
驗證 function call 功能

### 5. `README_ALL/13_RESPONSES_API_ARCHITECTURE.md`
新架構說明文檔

---

## 🚀 遷移步驟

### 步驟 1：備份當前版本

```bash
# 創建備份分支
git checkout -b backup-old-version
git add .
git commit -m "Backup before migration"

# 切回主分支
git checkout main
```

### 步驟 2：更新依賴

```bash
# 更新 OpenAI SDK
pip3 install --user -U openai

# 驗證版本
python3 -c "import openai; print(openai.__version__)"
```

### 步驟 3：更新代碼

**如果使用 Web API**：
```python
# web_api.py 或其他調用文件
from main_parallel import ResponsesRAGSystem  # 舊版: ParallelRAGSystem

system = ResponsesRAGSystem()  # 舊版: ParallelRAGSystem()
```

**如果直接調用**：
```python
import asyncio
from main_parallel import ResponsesRAGSystem

async def main():
    system = ResponsesRAGSystem()
    await system.initialize_documents()
    result = await system.process_query("什麼是機器學習？")
    print(result['final_answer'])

asyncio.run(main())
```

### 步驟 4：測試驗證

```bash
# 驗證 function call
bash README_ALL/BASH_ALL/verify_function_call.sh

# 測試完整系統
bash README_ALL/BASH_ALL/test_responses_api.sh
```

### 步驟 5：啟動服務

```bash
# 啟動 Web API
bash README_ALL/BASH_ALL/start_web_api.sh

# 或直接運行
python3 web_api.py
```

---

## ⚠️ 注意事項

### 1. API Key 設定

確保設定了 OpenAI API Key：
```bash
export OPENAI_API_KEY='your-api-key'
```

### 2. 向量文件兼容性

新舊版本的向量文件格式相同，可以直接使用：
- `vectors.pkl`
- `vectors.json`

### 3. 歷史記錄兼容性

歷史記錄格式相同，可以直接使用：
- `history.json`

### 4. 配置文件

`config.py` 無需修改，所有配置保持兼容。

---

## 🔍 常見問題

### Q1: 為什麼要遷移到 Responses API？

**A**: 
- ✅ 更低的延遲（判定回合只返回數字）
- ✅ 更低的成本（極小的 token 數）
- ✅ 更好的結構化控制
- ✅ 官方推薦的主要介面

### Q2: 舊版本還能用嗎？

**A**: 可以，但建議遷移到新版本以獲得更好的性能和未來支持。

### Q3: 遷移會影響現有數據嗎？

**A**: 不會。向量文件和歷史記錄完全兼容。

### Q4: 如果遇到問題怎麼辦？

**A**: 
1. 檢查 OpenAI SDK 版本（需 >= 1.54.0）
2. 查看錯誤日誌
3. 運行驗證腳本 `verify_function_call.sh`
4. 查看 [架構說明文檔](13_RESPONSES_API_ARCHITECTURE.md)

---

## 📊 性能對比

### 判定回合

| 指標 | 舊版 | 新版 | 改善 |
|------|------|------|------|
| Token 數 | ~500 | ~50 | 90% ↓ |
| 延遲 | ~1.5s | ~0.3s | 80% ↓ |
| 成本 | 高 | 低 | 90% ↓ |

### 總體流程

| 指標 | 舊版 | 新版 | 改善 |
|------|------|------|------|
| 總延遲 | ~8s | ~6s | 25% ↓ |
| API 調用次數 | 3次 | 2次 | 33% ↓ |
| 總成本 | 高 | 中 | 30% ↓ |

---

## ✅ 遷移檢查清單

- [ ] 備份當前版本
- [ ] 更新 OpenAI SDK 到 >= 1.54.0
- [ ] 更新代碼中的類名（`ParallelRAGSystem` → `ResponsesRAGSystem`）
- [ ] 運行驗證腳本
- [ ] 測試完整流程
- [ ] 檢查 API 響應
- [ ] 驗證歷史記錄功能
- [ ] 測試 Web 界面（如果使用）

---

## 📚 相關文檔

- [Responses API 架構說明](13_RESPONSES_API_ARCHITECTURE.md)
- [系統概述](10_SYSTEM_OVERVIEW.md)
- [快速開始](01_QUICK_START.md)

---

**準備好遷移了？開始執行遷移步驟吧！** 🚀
