# Responses API 雙回合架構說明

**📅 更新日期**: 2025-10-08  
**📚 版本**: 1.0

---

## 🎯 架構概述

本系統使用 **OpenAI Responses API 的 function/tool call 機制**，實現高效的雙回合處理流程。

### 核心特點

- ✅ **低延遲判定**：使用 function call 返回純數字（情境編號 1-24）
- ✅ **並行處理**：RAG 檢索與情境判定同時執行
- ✅ **流式輸出**：最終答案支持流式生成
- ✅ **結構化控制**：通過情境編號確保可重現性

---

## 🔄 雙回合流程

### 第一回合：判定回合（並行執行）

```
用戶問題
    ↓
┌─────────────────────────────────────┐
│   並行執行（asyncio.gather）         │
├──────────────────┬──────────────────┤
│   Thread A       │   Thread B       │
│   主線           │   支線           │
├──────────────────┼──────────────────┤
│ RAG 向量檢索     │ Responses API    │
│ - 檢索相關文檔   │ - Function Call  │
│ - 提取知識點     │ - 返回情境編號   │
│ - 格式化 context │ - (1-24)         │
└──────────────────┴──────────────────┘
    ↓                    ↓
  Context            Scenario ID
    └────────┬────────┘
             ↓
      第二回合
```

### 第二回合：最終回合

```
┌─────────────────────────────────────┐
│  整合資訊                            │
├─────────────────────────────────────┤
│ • RAG 檢索片段 (context)             │
│ • 情境編號 (scenario_id)             │
│ • 四向度值 (dimensions)              │
│ • 知識本體論 (ontology)              │
└─────────────────────────────────────┘
             ↓
    構建最終提示詞
             ↓
    Responses API 生成
    （stream=True）
             ↓
      流式輸出答案
```

---

## 📊 技術細節

### 1. 判定回合 - Function Call

**目的**：快速判定情境編號（1-24）

**配置**：
```python
{
    "model": "gpt-3.5-turbo",
    "tools": [classify_scenario_tool],
    "tool_choice": {"type": "function", "function": {"name": "classify_scenario"}},
    "temperature": 0,
    "max_tokens": 50  # 極小 token 數，降低成本
}
```

**返回格式**：
```json
{
    "scenario_id": 14  // 純數字，範圍 1-24
}
```

### 2. 最終回合 - 流式生成

**目的**：結合所有資訊生成完整答案

**輸入資訊**：
- RAG 檢索到的教材片段
- 情境編號及四向度值
- 知識本體論架構
- 匹配的知識點

**配置**：
```python
{
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": True  # 流式輸出
}
```

---

## 🚀 並行處理機制

使用 Python `asyncio.gather()` 實現協程並發：

```python
# 同時啟動兩條線
main_task = self.main_thread_rag(query)
branch_task = self.branch_thread_scenario(query)

# 等待兩條線都完成
rag_result, scenario_result = await asyncio.gather(main_task, branch_task)
```

**優勢**：
- 降低總延遲（並行執行）
- 提高資源利用率
- 保持代碼簡潔（協程而非多線程）

---

## 📝 情境說明方式

**簡化設計**：不使用複雜模板，直接告訴 AI 當前情境

```python
scenario_text = f"現在為第 {scenario_number} 種情境，代表 D1={dimensions['D1']}, D2={dimensions['D2']}, D3={dimensions['D3']}, D4={dimensions['D4']}"
```

**示例**：
```
現在為第 14 種情境，代表 D1=一個, D2=無錯誤, D3=粗略, D4=正常狀態
```

**未來擴展空間**：
- 可以添加更詳細的回應模板
- 可以根據情境調整回應風格
- 可以設計不同的教學策略

---

## 🔧 核心模組

### 1. `core/function_tools.py`
- 定義 function call 工具
- 創建分類提示詞
- 解析工具調用結果

### 2. `core/scenario_classifier.py`
- 使用 Responses API 判定情境
- 返回情境編號（1-24）
- 處理錯誤降級

### 3. `core/template_loader.py`
- 加載情境配置（保留，未來擴展用）
- 構建回應策略（預留接口）

### 4. `main_parallel.py`
- 實現雙回合流程
- 並行處理 RAG + 情境判定
- 整合生成最終答案

---

## ⚡ 性能優化

### 判定回合優化
- **極小 token 數**：`max_tokens=50`
- **零溫度**：`temperature=0`（確定性輸出）
- **強制 function call**：`tool_choice` 指定函數

### 並行處理優化
- **協程並發**：使用 `asyncio.gather()`
- **同時執行**：RAG 和情境判定不互相等待
- **減少總延遲**：總時間 ≈ max(RAG時間, 判定時間)

---

## 📈 計時報告

系統提供詳細的計時報告：

```
【主流程】
  向量化: 0.123s
  並行處理（總時間）: 2.456s
  最終回合生成: 3.789s
  總流程: 6.368s

【Thread A - 主線】
  RAG檢索: 2.123s
  小計: 2.123s

【Thread B - 分支】
  獲取歷史: 0.012s
  情境判定（Responses API）: 0.345s
  小計: 0.357s

總計: 6.368s
```

---

## 🎓 使用示例

### 命令行測試

```bash
# 更新 SDK
pip3 install --user -U openai

# 設定 API Key
export OPENAI_API_KEY='your-api-key'

# 運行測試
python3 main_parallel.py
```

### Web API 測試

```bash
# 啟動服務
python3 web_api.py

# 訪問文檔
open http://localhost:8000/docs
```

---

## 🔍 故障排除

### 問題 1：SDK 版本過舊

**錯誤**：`AttributeError: 'OpenAI' object has no attribute 'responses'`

**解決**：
```bash
pip3 install --user -U openai
```

### 問題 2：Function Call 未返回

**錯誤**：未收到 tool_calls

**檢查**：
1. 確認 `tool_choice` 設定正確
2. 檢查 function 定義格式
3. 查看 API 返回的錯誤信息

### 問題 3：情境編號超出範圍

**錯誤**：scenario_id 不在 1-24 範圍內

**處理**：系統自動降級到默認情境 14

---

## 📚 相關文檔

- [快速開始](01_QUICK_START.md)
- [系統概述](10_SYSTEM_OVERVIEW.md)
- [雙線程計時](12_DUAL_THREAD_TIMING.md)

---

## 🔄 版本歷史

### v1.0 (2025-10-08)
- ✅ 實現 Responses API function call
- ✅ 雙回合流程
- ✅ 並行處理機制
- ✅ 簡化情境說明

---

**準備好了？運行 `bash README_ALL/BASH_ALL/test_responses_api.sh` 開始測試！** 🚀
