# Bug 修復報告

## 🐛 發現的問題

### 錯誤訊息
```
TypeError: HistoryManager.get_recent_history() got an unexpected keyword argument 'limit'
```

---

## ✅ 已修復

### 1. 參數名稱錯誤
**位置**: `main_parallel.py` 第 166 行

**錯誤**:
```python
history = self.history_manager.get_recent_history(limit=5)
```

**修正**:
```python
history = self.history_manager.get_recent_history(n=5)
```

**原因**: `HistoryManager.get_recent_history()` 的參數是 `n` 而不是 `limit`

---

### 2. 模型更新為 gpt-4o-mini

**位置 1**: `core/scenario_classifier.py` 第 151 行
```python
model="gpt-4o-mini"  # 原本是 "gpt-4"
```

**位置 2**: `config.py` 第 17 行
```python
LLM_MODEL = "gpt-4o-mini"  # 原本是 "gpt-3.5-turbo"
```

**優勢**:
- ✅ 更快的回應速度
- ✅ 更低的成本
- ✅ 足夠的準確度

---

## 🚀 現在可以正常運行

系統已修復，可以正常處理查詢：

```bash
# 測試系統
python3 main_parallel.py

# 啟動 Web API
python3 web_api.py
```

---

## 📊 修復後的流程

```
用戶提問："你好"
    ↓
雙線程並行
    ├─ 主線：RAG 檢索 ✅
    └─ 分支：情境判定 ✅
         ├─ 獲取歷史記錄（n=5）✅
         ├─ 呼叫 gpt-4o-mini API ✅
         └─ 返回情境編號 ✅
    ↓
會診合併 ✅
    ↓
生成最終答案 ✅
```

---

## ✅ 驗證清單

- [x] 修正參數名稱 `limit` → `n`
- [x] 更新模型為 `gpt-4o-mini`
- [x] 情境判定 API 正常呼叫
- [x] 系統可以正常運行

**Bug 已修復！系統現在可以正常使用！** 🎉
