# Poetry 遷移說明

**📅 遷移日期**: 2025-10-09  
**✅ 狀態**: 已完成  
**🔧 環境管理**: Poetry 2.2.1+

---

## 🎯 遷移原因

### 遇到的問題

1. **PEP 668 錯誤**
   - 系統 Python 被標記為 `externally-managed`
   - 無法直接使用 `pip install` 安裝套件
   - 錯誤訊息：`error: externally-managed-environment`

2. **虛擬環境路徑問題**
   - `.venv` 路徑硬編碼在 shebang 中
   - 移動專案後虛擬環境失效
   - 錯誤：`bad interpreter: /old/path/.venv/bin/python3`

3. **依賴管理複雜**
   - 手動維護 `requirements.txt`
   - 版本衝突需手動解決
   - 團隊成員可能使用不同版本

### Poetry 的優勢

- ✅ **自動虛擬環境管理**：無需手動創建和激活
- ✅ **依賴解析**：自動處理版本衝突
- ✅ **版本鎖定**：`poetry.lock` 確保一致性
- ✅ **避免 PEP 668**：不會觸發系統保護機制
- ✅ **統一命令**：`poetry run` 和 `poetry shell`

---

## 📋 變更清單

### 新增文件

| 文件 | 位置 | 說明 |
|------|------|------|
| `pyproject.toml` | 根目錄 | Poetry 配置文件 |
| `poetry.lock` | 根目錄 | 依賴版本鎖定文件 |
| `03_POETRY_GUIDE.md` | `README_ALL/` | Poetry 使用指南 |
| `04_POETRY_MIGRATION.md` | `README_ALL/` | 本文件 |
| `poetry_run.sh` | `README_ALL/BASH_ALL/` | Poetry 快速啟動腳本 |

### 更新文件

| 文件 | 變更內容 |
|------|---------|
| `README.md` | 添加 Poetry 安裝和使用說明 |
| `01_QUICK_START.md` | 更新為 Poetry 命令 |
| `00_README_INDEX.md` | 添加 Poetry 指南索引 |
| `.gitignore` | 添加 `.venv/` 和 `poetry.lock` |

### 保留文件

| 文件 | 說明 |
|------|------|
| `requirements.txt` | 保留以支持傳統 pip 安裝 |

### 刪除內容

| 項目 | 原因 |
|------|------|
| 舊的 `.venv/` | 路徑損壞，已重建 |
| `venv/` | 舊虛擬環境 |
| 根目錄的 `run.sh` | 移至 `README_ALL/BASH_ALL/poetry_run.sh` |

---

## 🔧 技術細節

### pyproject.toml 配置

```toml
[tool.poetry]
name = "rag-stream-system"
version = "1.0.0"
description = "RAG 流式中斷與續寫系統"
authors = ["Jim"]
readme = "README.md"
package-mode = false  # 僅依賴管理，不打包

[tool.poetry.dependencies]
python = "^3.9"  # 從 3.8 升級到 3.9（numpy 要求）
openai = ">=1.54.0"  # 從 1.12.0 升級
numpy = "^1.26.0"  # 從 1.24.0 升級
python-dotenv = ">=1.0.0"
fastapi = ">=0.104.0"
uvicorn = {extras = ["standard"], version = ">=0.24.0"}
pydantic = ">=2.0.0"
```

### 虛擬環境位置

Poetry 配置為在專案內創建虛擬環境：

```bash
poetry config virtualenvs.in-project true
```

虛擬環境位置：`/mnt/c/Jim_Data/code/python/test_Time_RAG_stream/.venv`

### 依賴版本

| 套件 | 舊版本 | 新版本 | 說明 |
|------|--------|--------|------|
| openai | >=1.12.0 | >=1.54.0 | 支持最新 API |
| numpy | >=1.24.0 | ^1.26.0 | Python 3.9+ 要求 |
| fastapi | >=0.104.0 | >=0.104.0 | 無變更 |
| uvicorn | >=0.24.0 | >=0.24.0 | 添加 standard extras |
| pydantic | >=2.0.0 | >=2.0.0 | 無變更 |

---

## 📝 使用方式變更

### 之前（pip + venv）

```bash
# 創建虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 運行程序
python main_parallel.py
```

### 現在（Poetry）

```bash
# 安裝依賴（自動創建虛擬環境）
poetry install

# 方式 1：使用 poetry run
poetry run python main_parallel.py

# 方式 2：進入 shell
poetry shell
python main_parallel.py

# 方式 3：使用快速腳本
bash README_ALL/BASH_ALL/poetry_run.sh test
```

---

## 🚀 快速啟動腳本

### 腳本位置

`README_ALL/BASH_ALL/poetry_run.sh`

### 使用方式

```bash
# 運行主程序
bash README_ALL/BASH_ALL/poetry_run.sh test

# 啟動 Web API
bash README_ALL/BASH_ALL/poetry_run.sh web

# 進入 Poetry Shell
bash README_ALL/BASH_ALL/poetry_run.sh shell

# 安裝依賴
bash README_ALL/BASH_ALL/poetry_run.sh install

# 更新依賴
bash README_ALL/BASH_ALL/poetry_run.sh update
```

### 腳本功能

- ✅ 自動檢查 Poetry 是否安裝
- ✅ 自動安裝依賴（首次運行）
- ✅ 檢查 `.env` 文件
- ✅ 添加 Poetry 到 PATH

---

## 📂 文件組織

### 遵守專案架構規則

根據 `README.md` 的文件組織規則：

- ✅ **說明文件** → `README_ALL/`
  - `03_POETRY_GUIDE.md`
  - `04_POETRY_MIGRATION.md`

- ✅ **.sh 腳本** → `README_ALL/BASH_ALL/`
  - `poetry_run.sh`

- ✅ **配置文件** → 根目錄
  - `pyproject.toml`
  - `poetry.lock`（自動生成）

---

## ✅ 驗證安裝

### 檢查 Poetry

```bash
poetry --version
# 輸出: Poetry (version 2.2.1)
```

### 檢查依賴

```bash
poetry show
# 列出所有已安裝的套件
```

### 檢查虛擬環境

```bash
poetry env info
# 顯示虛擬環境信息
```

### 測試運行

```bash
poetry run python -c "import openai, fastapi, numpy; print('✅ 所有依賴已安裝')"
```

---

## 🐛 常見問題

### Q1: Poetry 命令找不到

**問題**：`poetry: command not found`

**解決**：
```bash
# 添加到 PATH
export PATH="$HOME/.local/bin:$PATH"

# 或重新安裝
curl -sSL https://install.python-poetry.org | python3 -
```

### Q2: 依賴安裝失敗

**問題**：`Resolving dependencies... Failed`

**解決**：
```bash
# 清除緩存
poetry cache clear pypi --all

# 刪除 lock 文件重試
rm poetry.lock
poetry install
```

### Q3: 虛擬環境位置

**問題**：不知道虛擬環境在哪裡

**解決**：
```bash
poetry env info --path
```

### Q4: 仍想使用 pip

**問題**：不想使用 Poetry

**解決**：
```bash
# 仍可使用傳統方式（需處理 PEP 668）
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📊 遷移前後對比

| 項目 | 遷移前 | 遷移後 |
|------|--------|--------|
| 環境管理 | 手動 venv | Poetry 自動 |
| 依賴安裝 | pip + requirements.txt | poetry install |
| 版本鎖定 | 無 | poetry.lock |
| 依賴解析 | 手動 | 自動 |
| 運行命令 | python script.py | poetry run python script.py |
| PEP 668 錯誤 | 會遇到 | 不會遇到 |
| 路徑問題 | 可能損壞 | 自動處理 |

---

## 🎯 後續步驟

### 團隊成員

1. 拉取最新代碼
2. 安裝 Poetry：`curl -sSL https://install.python-poetry.org | python3 -`
3. 安裝依賴：`poetry install`
4. 開始使用：`poetry run python main_parallel.py`

### 持續維護

1. 添加新依賴：`poetry add package-name`
2. 更新依賴：`poetry update`
3. 提交 `poetry.lock` 到 Git
4. 保持 `requirements.txt` 同步（可選）

---

## 📚 相關文檔

- **[03_POETRY_GUIDE.md](03_POETRY_GUIDE.md)** - Poetry 詳細使用指南
- **[01_QUICK_START.md](01_QUICK_START.md)** - 快速開始（已更新）
- **[02_INSTALLATION.md](02_INSTALLATION.md)** - 安裝指南
- **[16_TROUBLESHOOTING.md](16_TROUBLESHOOTING.md)** - 故障排除

---

## ✨ 總結

遷移到 Poetry 後：

- ✅ 解決了 PEP 668 錯誤
- ✅ 簡化了環境管理
- ✅ 提升了依賴管理效率
- ✅ 遵守了專案架構規則
- ✅ 保持了向後兼容（保留 requirements.txt）

**推薦所有用戶使用 Poetry 進行開發！** 🚀
