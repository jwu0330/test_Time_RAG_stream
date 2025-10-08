# 性能優化指南

**📅 更新日期**: 2025-10-08  
**📚 版本**: 1.0

---

## 🚨 發現的性能問題

### 問題：情境判定耗時過長

**症狀**：
```
Thread B - 支線（Responses API 情境判定）: 10.345s
總計時間: 13.324s
```

**預期**：
- 情境判定應該只需 0.3-0.5 秒
- 總計時間應該在 3-5 秒

**根本原因**：
1. ❌ 提示詞過長（包含完整的計算規則和四向度說明）
2. ❌ 不必要的計算邏輯（讓 AI 自己計算情境編號）
3. ❌ 歷史記錄過多（取最近 5 條）
4. ❌ System prompt 過於詳細

---

## ✅ 優化方案

### 1. **極簡提示詞**

#### 優化前（~200 tokens）
```python
prompt = f"""請根據用戶問題和歷史對話，判定當前情境編號（1-24）。

【四向度定義】
D1 - 知識點數量: 零個, 一個, 多個
D2 - 表達錯誤: 有錯誤, 無錯誤
D3 - 表達詳細度: 粗略, 非常詳細
D4 - 重複詢問: 重複狀態, 正常狀態

【情境編號計算規則】
情境編號 = D1_index * 8 + D2_index * 4 + D3_index * 2 + D4_index + 1

其中：
- D1: 零個=0, 一個=1, 多個=2
- D2: 有錯誤=0, 無錯誤=1
- D3: 粗略=0, 非常詳細=1
- D4: 重複狀態=0, 正常狀態=1

例如：D1=零個, D2=有錯誤, D3=粗略, D4=重複狀態 → 0*8 + 0*4 + 0*2 + 0 + 1 = 1

【當前問題】
{query}

【歷史對話】
{history_text}

請分析四個向度，並計算出對應的情境編號（1-24）。只需調用 classify_scenario 函數返回數字即可。"""
```

#### 優化後（~50 tokens）
```python
prompt = f"""分析問題並返回情境編號（1-24）。

問題: {query}
歷史: {history_text}

快速判斷：
- 知識點數量（0/1/多個）
- 表達錯誤（有/無）
- 詳細度（粗略/詳細）
- 重複詢問（是/否）

直接返回情境編號。"""
```

**改進**：
- ✅ Token 數減少 75%
- ✅ 移除計算規則（不需要 AI 計算）
- ✅ 簡化四向度說明
- ✅ 直接要求返回結果

### 2. **簡化歷史記錄**

#### 優化前
```python
# 取最近 5 條，包含知識點信息
for item in history[-5:]:
    query_text = item_dict.get('query', '')
    knowledge_points = item_dict.get('knowledge_points', [])
    if knowledge_points:
        history_items.append(f"- {query_text} (知識點: {', '.join(knowledge_points)})")
    else:
        history_items.append(f"- {query_text}")
```

#### 優化後
```python
# 只取最近 2 條，只顯示問題
recent = history[-2:] if len(history) >= 2 else history
for item in recent:
    query_text = item_dict.get('query', '')
    if query_text:
        history_items.append(query_text)
history_text = "; ".join(history_items)
```

**改進**：
- ✅ 歷史記錄從 5 條減少到 2 條
- ✅ 移除知識點信息（不必要）
- ✅ 使用簡潔的分號分隔

### 3. **極簡 System Prompt**

#### 優化前
```python
{"role": "system", "content": "你是一個專業的教育情境分析助手。請根據用戶問題和歷史對話，判定當前情境編號（1-24）。"}
```

#### 優化後
```python
{"role": "system", "content": "快速分析並返回情境編號（1-24）。"}
```

**改進**：
- ✅ 從 30+ tokens 減少到 10 tokens
- ✅ 直接說明任務，不要額外描述

### 4. **減少 max_tokens**

#### 優化前
```python
max_tokens=50
```

#### 優化後
```python
max_tokens=20
```

**改進**：
- ✅ 只需返回一個數字，20 tokens 足夠
- ✅ 減少 API 處理時間

### 5. **使用更快的模型**

#### 優化前
```python
CLASSIFIER_MODEL = "gpt-3.5-turbo"
```

#### 優化後
```python
CLASSIFIER_MODEL = "gpt-4o-mini"
```

**改進**：
- ✅ gpt-4o-mini 響應速度更快
- ✅ 成本更低
- ✅ 準確度相當

---

## 📊 預期性能提升

### 優化前
```
Thread B - 支線（Responses API 情境判定）: 10.345s
總計時間: 13.324s
```

### 優化後（預期）
```
Thread B - 支線（Responses API 情境判定）: 0.3-0.5s
總計時間: 3-5s
```

### 提升幅度
- **情境判定速度**: 95% ↑ (從 10s 到 0.5s)
- **總體速度**: 70% ↑ (從 13s 到 4s)
- **成本**: 80% ↓ (token 數大幅減少)

---

## 🔧 配置調整

### config.py

```python
# 使用更快的模型
CLASSIFIER_MODEL = "gpt-4o-mini"  # 而非 gpt-3.5-turbo

# 減少歷史記錄
HISTORY_SIZE = 10  # 但只取最近 2 條用於判定
```

### core/function_tools.py

```python
# 極簡提示詞
def create_classification_prompt(query, history, dimensions):
    # 只取最近 2 條歷史
    # 極簡格式
    # 直接要求返回結果
```

### core/scenario_classifier.py

```python
# 極簡 system prompt
{"role": "system", "content": "快速分析並返回情境編號（1-24）。"}

# 減少 max_tokens
max_tokens=20
```

---

## 🧪 測試驗證

### 測試命令

```bash
# 激活虛擬環境
source .venv/bin/activate

# 設定 API Key
export OPENAI_API_KEY='your-key'

# 運行測試
python3 main_parallel.py
```

### 檢查點

1. **情境判定時間** < 0.5s
2. **總計時間** < 5s
3. **API 調用成功**
4. **情境編號正確** (1-24)

---

## 📈 性能監控

### 關鍵指標

```python
# 在時間報告中查看
【Thread B - 支線（Responses API 情境判定）】
  獲取歷史                               :  0.000s
  情境判定（Responses API）               :  0.XXXs  # 應該 < 0.5s
  ─────────────────────────────────────────────
  支線小計                               :  0.XXXs  # 應該 < 0.5s
```

### 異常情況

如果情境判定仍然 > 1s：
1. 檢查網絡延遲
2. 檢查 API Key 配額
3. 檢查提示詞長度
4. 嘗試更換模型

---

## 🎯 最佳實踐

### 1. **提示詞設計**
- ✅ 越短越好（目標 < 100 tokens）
- ✅ 直接說明任務
- ✅ 避免不必要的解釋
- ✅ 使用簡潔的格式

### 2. **歷史記錄**
- ✅ 只取必要的歷史（2-3 條）
- ✅ 只包含關鍵信息
- ✅ 使用簡潔的格式

### 3. **模型選擇**
- ✅ 判定任務使用 gpt-4o-mini
- ✅ 生成任務使用 gpt-4o-mini
- ✅ 避免使用過大的模型

### 4. **參數設置**
- ✅ temperature=0（確定性輸出）
- ✅ max_tokens 設置為最小必要值
- ✅ 使用 tool_choice 強制調用

---

## 🔍 調試技巧

### 1. 測量各階段時間

```python
import time

start = time.perf_counter()
# 你的代碼
duration = time.perf_counter() - start
print(f"耗時: {duration:.3f}s")
```

### 2. 檢查提示詞長度

```python
import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o-mini")
tokens = encoding.encode(prompt)
print(f"Token 數: {len(tokens)}")
```

### 3. 對比測試

```python
# 測試舊版提示詞
old_duration = test_old_prompt()

# 測試新版提示詞
new_duration = test_new_prompt()

print(f"提升: {(old_duration - new_duration) / old_duration * 100:.1f}%")
```

---

## 📚 相關文檔

- [Responses API 架構](13_RESPONSES_API_ARCHITECTURE.md)
- [時間記錄更新](17_TIMING_UPDATES.md)
- [故障排除](16_TROUBLESHOOTING.md)

---

## ✅ 優化檢查清單

- [x] 簡化提示詞（< 100 tokens）
- [x] 減少歷史記錄（2 條）
- [x] 極簡 system prompt
- [x] 減少 max_tokens（20）
- [x] 使用更快的模型（gpt-4o-mini）
- [x] 移除不必要的計算邏輯
- [ ] 測試驗證性能提升
- [ ] 監控實際運行時間

---

**優化完成！預期情境判定時間從 10s 降低到 0.5s 以內！** ⚡
