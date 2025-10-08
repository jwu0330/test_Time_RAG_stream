# RAG 流式系統 - 完整文檔

## 📋 目錄

1. [系統概述](#系統概述)
2. [環境設置](#環境設置)
3. [系統架構](#系統架構)
4. [使用指南](#使用指南)
5. [自定義配置](#自定義配置)
6. [API 參考](#api-參考)

---

## 系統概述

### 核心功能

#### 1. 四向度分類系統

| 向度 | 名稱 | 判斷方式 | 可能值 |
|------|------|----------|--------|
| D1 | 知識點數量 | RAG 實際匹配 | 零個、一個、多個 |
| D2 | 表達錯誤 | AI 判斷 | 有錯誤、無錯誤 |
| D3 | 表達詳細度 | AI 判斷 | 非常詳細、粗略、未談及重點 |
| D4 | 重複詢問 | AI 分析歷史 | 重複狀態、正常狀態 |

#### 2. 24 種情境組合

3 × 2 × 3 × 2 = 24 種情境，每種情境有獨立的回答策略。

#### 3. 並行處理架構

```
用戶問題
    ↓
並行分析（D2、D3、D4 同時執行）
    ↓
RAG 檢索 → D1 分析
    ↓
情境匹配（O(1) 查找）
    ↓
合併到主線程
    ↓
生成最終答案
```

---

## 環境設置

### 方式 1：使用 venv（推薦）

```bash
# 1. 創建虛擬環境
python3 -m venv venv

# 2. 激活環境
source venv/bin/activate

# 3. 安裝依賴
pip install -r requirements.txt
```

### 方式 2：使用 Poetry

```bash
# 1. 安裝依賴
poetry install

# 2. 運行
poetry run python RUN_TEST.py
```

### 必要配置

```bash
# 設定 OpenAI API Key
export OPENAI_API_KEY="your-api-key-here"
```

---

## 系統架構

### 文件結構

```
test_Time_RAG_stream/
├── config.py                  # 配置文件
├── main_parallel.py           # 並行處理主程序
├── scenario_module.py         # 四向度分類器
├── scenario_matcher.py        # 情境匹配系統
├── history_manager.py         # 歷史記錄管理
├── knowledge_relations.json   # 知識點關聯
├── scenarios_24/              # 24 個情境配置
├── docs/                      # 教材文件
├── web_api.py                 # Web API
└── web_interface.html         # Web 前端
```

### 核心模組

#### 1. ParallelRAGSystem（main_parallel.py）

並行處理的主系統，負責：
- 並行執行四向度分析
- 協調各模組
- 生成最終答案

#### 2. DimensionClassifier（scenario_module.py）

四向度分類器，負責：
- D1: 基於 RAG 結果判斷知識點數量
- D2: AI 判斷表達錯誤
- D3: AI 判斷表達詳細度
- D4: AI 分析歷史判斷重複

#### 3. ScenarioMatcher（scenario_matcher.py）

情境匹配系統，負責：
- 快速匹配 24 種情境（O(1)）
- 提取知識點關聯
- 生成完整提示詞

#### 4. HistoryManager（history_manager.py）

歷史記錄管理，負責：
- 保存最近 10 筆查詢
- 追蹤知識點訪問
- 支持重複檢測

---

## 使用指南

### 基本使用

```bash
# 1. 激活環境
source venv/bin/activate

# 2. 設定 API Key
export OPENAI_API_KEY="your-key"

# 3. 運行測試
python RUN_TEST.py
```

### Web 界面

```bash
# 1. 啟動後端
python web_api.py

# 2. 在瀏覽器打開
open web_interface.html
```

### 程式化使用

```python
import asyncio
from main_parallel import ParallelRAGSystem

async def main():
    # 初始化系統
    system = ParallelRAGSystem()
    
    # 初始化文件
    await system.initialize_documents()
    
    # 處理查詢
    result = await system.process_query_parallel("什麼是機器學習？")
    
    # 查看結果
    print(result['final_answer'])
    print(f"情境：{result['scenario_number']}")
    print(f"四向度：{result['dimensions']}")

asyncio.run(main())
```

---

## 自定義配置

### 1. 修改教材

```bash
# 1. 將教材放入 docs/ 目錄
cp your_materials/* docs/

# 2. 編輯 config.py
nano config.py

# 3. 更新知識點映射
KNOWLEDGE_POINTS = {
    "your_file1.txt": "知識點1",
    "your_file2.txt": "知識點2",
    "your_file3.txt": "知識點3"
}
```

### 2. 調整情境

編輯 `scenarios_24/scenario_XX.json`：

```json
{
  "id": "scenario_08",
  "scenario_number": 8,
  "dimensions": {
    "D1": "一個",
    "D2": "無錯誤",
    "D3": "粗略",
    "D4": "正常狀態"
  },
  "response_strategy": {
    "tone": "友好、專業",
    "length": "適中"
  },
  "prompt_template": "您的自定義提示詞..."
}
```

### 3. 修改知識點關聯

編輯 `knowledge_relations.json`：

```json
{
  "relations": {
    "kp1_to_kp2": {
      "from": "kp1",
      "to": "kp2",
      "description": "關係描述",
      "key_connections": ["連接點1", "連接點2"]
    }
  }
}
```

### 4. 調整模型配置

編輯 `config.py`：

```python
# LLM 模型配置
LLM_MODEL = "gpt-4"  # 或 "gpt-3.5-turbo"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 2000
```

---

## API 參考

### ParallelRAGSystem

#### `__init__(api_key=None)`
初始化系統。

#### `async initialize_documents(docs_dir=None)`
初始化並向量化文件。

#### `async process_query_parallel(query: str) -> Dict`
並行處理查詢，返回完整結果。

**返回格式**：
```python
{
    "query": str,
    "final_answer": str,
    "scenario_number": int,
    "scenario_name": str,
    "dimensions": {
        "D1": str,
        "D2": str,
        "D3": str,
        "D4": str
    },
    "knowledge_points": List[str],
    "time_report": {
        "stages": Dict[str, float],
        "total_time": float
    }
}
```

### ScenarioMatcher

#### `match_scenario(dimensions: Dict) -> Dict`
根據四向度匹配情境。

#### `get_prompt(dimensions, query, context, knowledge_points) -> str`
生成完整提示詞。

### DimensionClassifier

#### `async classify(query, matched_docs, context) -> Dict`
執行四向度分類。

---

## 故障排除

### 問題 1：API Key 錯誤
```bash
export OPENAI_API_KEY="your-key"
```

### 問題 2：找不到模組
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 問題 3：向量化失敗
```bash
# 刪除舊的向量文件
rm vectors.pkl vectors.json

# 重新運行
python RUN_TEST.py
```

---

## 性能優化

### 1. 並行處理
系統已使用並行處理，D2、D3、D4 同時執行。

### 2. 向量緩存
首次向量化後會保存到 `vectors.pkl`，之後直接載入。

### 3. 情境匹配
使用哈希表實現 O(1) 查找。

---

## 開發指南

### 添加新的向度

1. 在 `scenario_module.py` 中添加新的分類方法
2. 更新 `classify()` 方法
3. 更新情境生成器
4. 重新生成情境文件

### 添加新的情境

1. 運行 `scenario_generator.py`
2. 編輯生成的 JSON 文件
3. 自定義提示詞和策略

---

## 授權

MIT License

---

## 聯繫方式

GitHub: https://github.com/jwu0330/test_Time_RAG_stream
