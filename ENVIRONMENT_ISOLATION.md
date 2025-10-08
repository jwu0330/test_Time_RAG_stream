# 🔒 環境隔離說明

## 問題說明

剛才使用 `pip3 install --user` 安裝的包會安裝到：
```
/home/jim/.local/lib/python3.10/site-packages/
```

這會影響到系統級別的 Python 環境，可能會污染到其他用戶或項目。

---

## ✅ 解決方案：使用虛擬環境

虛擬環境會創建一個**完全獨立**的 Python 環境，所有依賴都安裝在項目目錄內：

```
test_Time_RAG_stream/
└── venv/                          # 虛擬環境（完全獨立）
    ├── bin/python                 # 獨立的 Python
    ├── lib/python3.10/site-packages/  # 獨立的包
    └── ...
```

---

## 🧹 清理並重新設置

### 一鍵清理並設置

```bash
chmod +x CLEANUP_AND_SETUP.sh
./CLEANUP_AND_SETUP.sh
```

這個腳本會：
1. ✅ 移除剛才安裝到 `~/.local/` 的所有包
2. ✅ 創建獨立的虛擬環境 `venv/`
3. ✅ 在虛擬環境中安裝所有依賴
4. ✅ 完全不影響系統環境

---

## 📋 手動步驟（如果需要）

### 1. 清理用戶安裝的包

```bash
pip3 uninstall -y openai numpy python-dotenv fastapi uvicorn pydantic \
    typing-extensions tqdm sniffio jiter h11 annotated-types \
    pydantic-core httpcore exceptiongroup starlette httpx typing-inspection anyio
```

### 2. 創建虛擬環境

```bash
python3 -m venv venv
```

### 3. 激活虛擬環境

```bash
source venv/bin/activate
```

### 4. 安裝依賴

```bash
pip install openai numpy python-dotenv fastapi uvicorn pydantic
```

---

## 🎯 使用虛擬環境

### 每次使用前

```bash
# 激活虛擬環境
source venv/bin/activate

# 現在 python 和 pip 都指向虛擬環境
which python  # 應該顯示: .../venv/bin/python
```

### 運行程序

```bash
# 在激活的虛擬環境中
python RUN_TEST.py
```

### 使用完畢

```bash
# 退出虛擬環境
deactivate
```

---

## 🔍 驗證環境隔離

### 檢查當前使用的 Python

```bash
# 激活虛擬環境後
which python
# 應該顯示: /home/jim/code/py/test_Time_RAG_stream/venv/bin/python

# 檢查安裝的包
pip list
# 只會顯示虛擬環境中的包
```

### 檢查系統 Python

```bash
# 退出虛擬環境
deactivate

# 檢查系統 Python
which python3
# 顯示系統的 Python

pip3 list
# 不會包含剛才安裝的包（已清理）
```

---

## 📦 虛擬環境的優點

1. **完全隔離**
   - 不影響系統 Python
   - 不影響其他用戶
   - 不影響其他項目

2. **易於管理**
   - 可以隨時刪除重建：`rm -rf venv/`
   - 可以導出依賴：`pip freeze > requirements.txt`
   - 可以在其他機器上重現：`pip install -r requirements.txt`

3. **避免衝突**
   - 不同項目可以使用不同版本的包
   - 不會與 pyenv-win 衝突

---

## 🗑️ 完全清理（如果需要）

如果將來不需要這個項目了：

```bash
# 刪除虛擬環境
rm -rf venv/

# 刪除向量文件
rm -f vectors.pkl vectors.json

# 刪除歷史記錄
rm -f history.json

# 刪除結果
rm -rf results/
```

這樣就完全清理乾淨了，不會留下任何痕跡。

---

## ✅ 推薦工作流程

```bash
# 1. 首次設置（只需一次）
chmod +x CLEANUP_AND_SETUP.sh
./CLEANUP_AND_SETUP.sh

# 2. 每次使用
source venv/bin/activate
export OPENAI_API_KEY="your-key"
python RUN_TEST.py
deactivate

# 3. 或使用便捷腳本
chmod +x activate_and_run.sh
./activate_and_run.sh
```

---

## 🎉 總結

使用虛擬環境後：
- ✅ 完全獨立，不污染系統
- ✅ 易於管理和清理
- ✅ 可以安全地與他人共享機器
- ✅ 符合 Python 最佳實踐
