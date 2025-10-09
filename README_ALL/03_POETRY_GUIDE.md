# Poetry 使用指南

**📅 更新日期**: 2025-10-09  
**✅ Poetry 版本**: 2.2.1+

---

## 🎯 為什麼使用 Poetry

### 優勢

- ✅ **自動管理虛擬環境**：無需手動創建和激活
- ✅ **依賴解析**：自動處理版本衝突
- ✅ **鎖定版本**：確保團隊使用相同版本
- ✅ **簡化命令**：統一的命令接口
- ✅ **避免系統污染**：不會影響系統 Python

### 與 pip + venv 的對比

| 功能 | pip + venv | Poetry |
|------|-----------|--------|
| 創建環境 | `python3 -m venv .venv` | 自動 |
| 激活環境 | `source .venv/bin/activate` | `poetry shell` 或 `poetry run` |
| 安裝依賴 | `pip install -r requirements.txt` | `poetry install` |
| 添加套件 | `pip install xxx` + 手動更新 requirements.txt | `poetry add xxx` |
| 依賴解析 | 手動處理衝突 | 自動解析 |
| 版本鎖定 | 無（或使用 requirements.lock） | poetry.lock |

---

## 📦 安裝 Poetry

### 方法 1: 官方安裝腳本（推薦）

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 方法 2: 使用 pip

```bash
pip install --user poetry
```

### 添加到 PATH

Poetry 安裝在 `~/.local/bin`，需要添加到 PATH：

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 驗證安裝

```bash
poetry --version
# 輸出: Poetry (version 2.2.1)
```

---

## 🚀 快速開始

### 1. 安裝專案依賴

```bash
# 在專案目錄下
poetry install
```

這會：
- 自動創建虛擬環境（在 `.venv/` 或 Poetry 緩存目錄）
- 安裝所有依賴
- 生成 `poetry.lock` 文件

### 2. 運行程序

#### 方式 A: 使用 `poetry run`

```bash
poetry run python main_parallel.py
poetry run python web_api.py
```

#### 方式 B: 進入 Poetry Shell

```bash
# 進入虛擬環境
poetry shell

# 現在可以直接運行
python main_parallel.py
python web_api.py

# 退出
exit
```

#### 方式 C: 使用快速啟動腳本

```bash
./run.sh test    # 運行主程序
./run.sh web     # 啟動 Web API
./run.sh shell   # 進入 Shell
```

---

## 📝 常用命令

### 環境管理

```bash
# 安裝依賴
poetry install

# 更新依賴
poetry update

# 查看已安裝的套件
poetry show

# 查看特定套件信息
poetry show openai

# 查看虛擬環境信息
poetry env info

# 列出所有虛擬環境
poetry env list

# 刪除虛擬環境
poetry env remove python3.12
# 或刪除所有
poetry env remove --all
```

### 添加/移除套件

```bash
# 添加套件
poetry add requests

# 添加開發依賴
poetry add --group dev pytest

# 移除套件
poetry remove requests

# 更新特定套件
poetry update openai
```

### 運行命令

```bash
# 運行 Python 腳本
poetry run python script.py

# 運行任意命令
poetry run pytest
poetry run black .

# 進入 Shell
poetry shell
```

### 配置

```bash
# 查看配置
poetry config --list

# 設置虛擬環境在專案內創建
poetry config virtualenvs.in-project true

# 設置虛擬環境在 Poetry 緩存目錄
poetry config virtualenvs.in-project false
```

---

## 🔧 專案配置

### pyproject.toml 結構

```toml
[tool.poetry]
name = "rag-stream-system"
version = "1.0.0"
description = "RAG 流式中斷與續寫系統"
authors = ["Jim"]
readme = "README.md"
package-mode = false  # 不打包，僅依賴管理

[tool.poetry.dependencies]
python = "^3.9"  # Python 版本要求
openai = ">=1.54.0"
numpy = "^1.26.0"
python-dotenv = ">=1.0.0"
fastapi = ">=0.104.0"
uvicorn = {extras = ["standard"], version = ">=0.24.0"}
pydantic = ">=2.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### 版本約束語法

| 語法 | 說明 | 範例 |
|------|------|------|
| `^1.2.3` | 兼容版本（不改變最左非零位） | `>=1.2.3, <2.0.0` |
| `~1.2.3` | 近似版本 | `>=1.2.3, <1.3.0` |
| `>=1.2.3` | 大於等於 | `>=1.2.3` |
| `1.2.*` | 通配符 | `>=1.2.0, <1.3.0` |
| `1.2.3` | 精確版本 | `==1.2.3` |

---

## 🐛 常見問題

### Q1: ModuleNotFoundError

**問題**：運行時找不到模組

**原因**：沒有使用 Poetry 環境運行

**解決**：
```bash
# 使用 poetry run
poetry run python script.py

# 或進入 shell
poetry shell
python script.py
```

### Q2: 虛擬環境位置

**問題**：不知道虛擬環境在哪裡

**解決**：
```bash
poetry env info --path
# 輸出: /home/user/.cache/pypoetry/virtualenvs/xxx
# 或: /path/to/project/.venv
```

### Q3: 依賴衝突

**問題**：`Resolving dependencies... Failed`

**解決**：
```bash
# 1. 清除緩存
poetry cache clear pypi --all

# 2. 刪除 poetry.lock 重新解析
rm poetry.lock
poetry install

# 3. 調整版本約束（在 pyproject.toml）
```

### Q4: 安裝很慢

**問題**：`poetry install` 很慢

**解決**：
```bash
# 使用國內鏡像（如果在中國）
poetry source add --priority=primary tsinghua https://pypi.tuna.tsinghua.edu.cn/simple/

# 或使用 pip 緩存
poetry config installer.parallel true
```

### Q5: externally-managed-environment 錯誤

**問題**：系統阻止 pip 安裝

**解決**：使用 Poetry！Poetry 會自動創建隔離的虛擬環境，不會觸發這個錯誤。

---

## 🔄 從 pip 遷移到 Poetry

### 步驟 1: 創建 pyproject.toml

```bash
# 如果還沒有 pyproject.toml
poetry init

# 或從 requirements.txt 導入
poetry add $(cat requirements.txt)
```

### 步驟 2: 清理舊環境

```bash
# 刪除舊的虛擬環境
rm -rf .venv venv

# 刪除 __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +
```

### 步驟 3: 安裝依賴

```bash
poetry install
```

### 步驟 4: 更新文檔

更新 README 和腳本，使用 `poetry run` 替代直接運行。

---

## 📊 最佳實踐

### 1. 使用 poetry.lock

- ✅ **提交到 Git**：確保團隊使用相同版本
- ✅ **定期更新**：`poetry update` 更新依賴

### 2. 虛擬環境位置

```bash
# 推薦：在專案內（方便管理）
poetry config virtualenvs.in-project true

# 或：在 Poetry 緩存目錄（節省空間）
poetry config virtualenvs.in-project false
```

### 3. 開發依賴分組

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^23.0.0"
mypy = "^1.0.0"
```

### 4. 腳本別名

在 `pyproject.toml` 中定義：

```toml
[tool.poetry.scripts]
test = "scripts.test:main"
serve = "scripts.serve:main"
```

然後運行：
```bash
poetry run test
poetry run serve
```

---

## 🎯 本專案使用方式

### 快速啟動

```bash
# 1. 安裝依賴
poetry install

# 2. 設定 API Key
cp .env.example .env
nano .env

# 3. 運行
poetry run python main_parallel.py
```

### 使用腳本

```bash
./run.sh test    # 運行主程序
./run.sh web     # 啟動 Web API
./run.sh shell   # 進入 Shell
```

### 開發流程

```bash
# 進入 Shell
poetry shell

# 開發和測試
python main_parallel.py
python web_api.py

# 添加新依賴
poetry add new-package

# 退出
exit
```

---

## 📚 更多資源

- **官方文檔**: https://python-poetry.org/docs/
- **基本用法**: https://python-poetry.org/docs/basic-usage/
- **依賴管理**: https://python-poetry.org/docs/dependency-specification/
- **配置**: https://python-poetry.org/docs/configuration/

---

**提示**：如果遇到問題，先嘗試 `poetry env remove --all` 和 `poetry install` 重新安裝。
