# 環境設置指南

## 🔍 檢查當前環境

請先執行以下命令檢查您的環境：

```bash
# 檢查 Python
python3 --version
which python3

# 檢查 pip
pip3 --version
which pip3

# 檢查 Poetry
poetry --version
which poetry
```

---

## 📦 方案 A：使用 Poetry（推薦）

如果您已經有 Poetry，使用 Poetry 管理依賴更好。

### 1. 創建 Poetry 項目

```bash
# 初始化 Poetry（如果還沒有 pyproject.toml）
poetry init --no-interaction

# 或者我已經為您準備好了 pyproject.toml
```

### 2. 安裝依賴

```bash
# 使用 Poetry 安裝所有依賴
poetry install

# 或者添加依賴
poetry add openai numpy python-dotenv fastapi uvicorn pydantic
```

### 3. 運行測試

```bash
# 使用 Poetry 環境運行
poetry run python RUN_TEST.py

# 或者進入 Poetry shell
poetry shell
python RUN_TEST.py
```

---

## 📦 方案 B：使用 pip + venv（如果沒有 Poetry）

### 1. 創建虛擬環境

```bash
# 創建虛擬環境
python3 -m venv venv

# 激活虛擬環境
source venv/bin/activate
```

### 2. 安裝依賴

```bash
# 安裝依賴
pip install -r requirements.txt

# 或手動安裝
pip install openai numpy python-dotenv fastapi uvicorn pydantic
```

### 3. 運行測試

```bash
# 確保虛擬環境已激活
python RUN_TEST.py
```

---

## 📦 方案 C：全局安裝（不推薦，但最簡單）

```bash
# 直接安裝到系統 Python
pip3 install openai numpy python-dotenv fastapi uvicorn pydantic

# 運行測試
python3 RUN_TEST.py
```

---

## 🎯 我的建議

根據您的情況：

### 如果有 Poetry：
```bash
poetry install
poetry run python RUN_TEST.py
```

### 如果沒有 Poetry：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python RUN_TEST.py
```

---

## 📝 快速安裝腳本

我為您準備了一個自動安裝腳本。
