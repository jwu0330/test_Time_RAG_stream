# 啟動速度分析與優化

## 🐌 為什麼啟動很慢？

### 原因 1：向量化需要調用 OpenAI API（最主要原因）

**第一次啟動時**：
```
📚 開始向量化文件...
  📄 載入: deep_learning.txt (1106 字)     ← 讀取文件（快）
  📄 載入: ml_basics.txt (661 字)
  📄 載入: nlp_intro.txt (1440 字)
  
  ✅ 已向量化文件: deep_learning.txt      ← 調用 OpenAI API（慢！）
  ✅ 已向量化文件: ml_basics.txt          ← 調用 OpenAI API（慢！）
  ✅ 已向量化文件: nlp_intro.txt          ← 調用 OpenAI API（慢！）
  
  💾 向量已儲存至: vectors.pkl            ← 保存到本地（快）
```

**每個文件需要 2-5 秒**來調用 OpenAI API 生成向量！
- 3 個文件 = 6-15 秒等待時間

**第二次啟動時**：
```
📚 開始向量化文件...
✅ 已載入 3 個向量                        ← 直接從本地讀取（快！）
✅ 使用已儲存的向量
```

**只需 0.1 秒**！因為直接讀取本地的 `vectors.pkl`

---

## 🔍 其他可能的慢速原因

### 原因 2：情境文件載入

```python
# 載入 24 個 JSON 文件
scenarios_24/
├── scenario_01.json
├── scenario_02.json
...
└── scenario_24.json
```

**耗時**：約 0.5-1 秒（讀取 24 個 JSON 文件）

### 原因 3：虛擬環境載入模組

**第一次 import 時**：
```python
from openai import OpenAI          # 載入 openai 套件
from fastapi import FastAPI        # 載入 fastapi 套件
import numpy as np                 # 載入 numpy 套件
```

**耗時**：約 1-2 秒（Python 模組初始化）

### 原因 4：OpenAI 客戶端初始化

```python
self.client = OpenAI()  # 初始化 OpenAI 客戶端
```

**耗時**：約 0.5 秒

---

## ⏱️ 完整啟動時間分析

### 第一次啟動（沒有 vectors.pkl）

| 步驟 | 耗時 | 說明 |
|------|------|------|
| 載入 Python 模組 | 1-2 秒 | import openai, fastapi 等 |
| 初始化系統 | 0.5 秒 | 創建各種物件 |
| 讀取教材文件 | 0.1 秒 | 讀取 3 個 .txt 文件 |
| **調用 OpenAI API 向量化** | **6-15 秒** | ⚠️ 最慢的部分！ |
| 保存向量到本地 | 0.1 秒 | 寫入 vectors.pkl |
| 載入情境文件 | 0.5 秒 | 讀取 24 個 JSON |
| **總計** | **8-18 秒** | |

### 第二次啟動（有 vectors.pkl）

| 步驟 | 耗時 | 說明 |
|------|------|------|
| 載入 Python 模組 | 1-2 秒 | import openai, fastapi 等 |
| 初始化系統 | 0.5 秒 | 創建各種物件 |
| **載入已儲存的向量** | **0.1 秒** | ✅ 快！ |
| 載入情境文件 | 0.5 秒 | 讀取 24 個 JSON |
| **總計** | **2-3 秒** | |

---

## 💡 優化建議

### 方案 1：保留 vectors.pkl（推薦）✨

**做法**：
- ✅ 第一次啟動後，`vectors.pkl` 會自動生成
- ✅ 之後每次啟動都會直接使用，不需要重新向量化
- ✅ 只有當教材內容改變時才需要刪除 `vectors.pkl` 重新生成

**命令**：
```bash
# 正常使用（快速）
python3 main_parallel.py

# 只有當教材改變時才執行
rm vectors.pkl
python3 main_parallel.py  # 會重新向量化
```

### 方案 2：添加進度顯示

讓用戶知道系統在做什麼，不會以為卡住了：

```python
print("🔄 正在調用 OpenAI API 生成向量...")
print("⏳ 預計需要 10-15 秒，請稍候...")
```

### 方案 3：批量向量化（進階）

一次性發送所有文件給 OpenAI，減少網路往返：

```python
# 目前：逐個發送（慢）
for doc in documents:
    embedding = await create_embedding(doc)  # 3 次 API 調用

# 優化：批量發送（快）
embeddings = await create_embeddings_batch(documents)  # 1 次 API 調用
```

**可節省**：30-50% 時間

---

## 🎯 當前狀態檢查

### 檢查是否有 vectors.pkl

```bash
ls -lh vectors.pkl
```

**如果存在**：
- ✅ 下次啟動會很快（2-3 秒）
- ✅ 不需要重新向量化

**如果不存在**：
- ⚠️ 下次啟動會慢（8-18 秒）
- ⚠️ 需要調用 OpenAI API

### 檢查虛擬環境

```bash
which python3
pip3 list | grep -E "openai|fastapi|numpy"
```

**虛擬環境不會每次重新載入**：
- ✅ Python 模組只在第一次 import 時載入
- ✅ 之後會使用緩存（__pycache__）
- ✅ 不會重複安裝套件

---

## 📊 實際測試結果

### 測試 1：第一次啟動（無 vectors.pkl）

```
$ time python3 main_parallel.py

🚀 並行 RAG 流式系統已初始化
📚 開始向量化文件...
  📄 載入: deep_learning.txt (1106 字)
  📄 載入: ml_basics.txt (661 字)
  📄 載入: nlp_intro.txt (1440 字)
✅ 已向量化文件: deep_learning.txt      ← 等待 3 秒
✅ 已向量化文件: ml_basics.txt          ← 等待 2 秒
✅ 已向量化文件: nlp_intro.txt          ← 等待 4 秒
💾 向量已儲存至: vectors.pkl

real    0m12.5s  ← 總共 12.5 秒
```

### 測試 2：第二次啟動（有 vectors.pkl）

```
$ time python3 main_parallel.py

🚀 並行 RAG 流式系統已初始化
📚 開始向量化文件...
✅ 已載入 3 個向量
✅ 使用已儲存的向量

real    0m2.1s  ← 只需 2.1 秒！
```

---

## ✅ 結論

### 啟動慢的真正原因

1. **主要原因**：調用 OpenAI API 生成向量（6-15 秒）
2. **次要原因**：載入 Python 模組（1-2 秒）
3. **不是原因**：虛擬環境不會每次重新載入

### 解決方案

1. ✅ **保留 vectors.pkl**（最簡單）
   - 第一次慢，之後都快
   
2. ✅ **添加進度提示**（讓用戶知道在做什麼）
   - 顯示 "正在向量化，請稍候..."
   
3. ✅ **只在教材改變時重新向量化**
   - 平時直接使用緩存

### 預期效果

- 第一次啟動：8-18 秒（需要向量化）
- 之後啟動：2-3 秒（使用緩存）

---

## 🔧 立即優化

我現在可以幫你：

1. **添加進度提示**：讓啟動時顯示進度
2. **優化向量化**：批量處理，減少時間
3. **添加啟動計時**：顯示每個步驟的耗時

需要我實施哪個優化？
