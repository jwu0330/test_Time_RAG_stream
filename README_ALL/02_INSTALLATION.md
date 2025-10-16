# 詳細安裝指南

**📅 更新日期**: 2025-10-08  
**🔧 系統版本**: 2.0

---

## 📋 環境需求

### 系統需求

- **作業系統**: Linux / macOS / Windows (WSL)
- **Python 版本**: >= 3.8
- **記憶體**: >= 2GB
- **磁碟空間**: >= 500MB

### 必要工具

- Python 3.8+
- pip3
- Git (可選，用於克隆倉庫)

---

## 🔧 安裝方式

### 方式 1：使用 pip（推薦）

```bash
# 1. 克隆倉庫（如果還沒有）
git clone https://github.com/jwu0330/test_Time_RAG_stream.git
cd test_Time_RAG_stream

# 2. 安裝依賴
pip3 install --user -r requirements.txt

# 3. 設定 API Key
export OPENAI_API_KEY="your-api-key-here"

# 4. 測試運行
python3 main_parallel.py
```

### 方式 2：使用虛擬環境（推薦用於開發）

```bash
# 1. 創建虛擬環境
python3 -m venv venv

# 2. 激活環境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 設定 API Key
export OPENAI_API_KEY="your-api-key-here"

# 5. 運行
python main_parallel.py
```

### 方式 3：使用 Poetry（進階）

```bash
# 1. 安裝 Poetry（如果還沒有）
curl -sSL https://install.python-poetry.org | python3 -

# 2. 安裝依賴
poetry install

# 3. 運行
poetry run python main_parallel.py
```

---

## 🔑 API Key 設定

### OpenAI API Key

**獲取方式**：
1. 訪問 https://platform.openai.com/api-keys
2. 登錄或註冊帳號
3. 創建新的 API Key
4. 複製 Key（格式：sk-...）

### 設定方式

#### 方式 A：環境變數（臨時）

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**優點**: 簡單快速  
**缺點**: 每次打開新終端都需要重新設定

#### 方式 B：.env 文件（推薦）

```bash
# 1. 複製範例文件
cp .env.example .env

# 2. 編輯 .env
nano .env

# 3. 添加你的 Key
OPENAI_API_KEY=sk-your-key-here
```

**優點**: 一次設定，永久有效  
**缺點**: 需要注意不要提交到 Git（已在 .gitignore 中）

#### 方式 C：shell 配置文件（永久）

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**優點**: 系統級配置，所有專案都能用  
**缺點**: 需要注意安全性

---

## 📦 依賴詳解

### requirements.txt

```txt
openai>=1.12.0       # OpenAI API 客戶端
numpy>=1.24.0        # 數值計算（向量操作）
python-dotenv>=1.0.0 # 環境變數管理
fastapi>=0.104.0     # Web API 框架
uvicorn>=0.24.0      # ASGI 服務器
pydantic>=2.0.0      # 數據驗證
```

### 可選依賴

```bash
# 如果需要更快的向量檢索
pip3 install faiss-cpu

# 如果需要使用 Jupyter
pip3 install jupyter

# 如果需要進行測試
pip3 install pytest pytest-asyncio
```

---

## 🧪 驗證安裝

### 檢查 Python 環境

```bash
# 檢查 Python 版本
python3 --version
# 應該顯示: Python 3.8.x 或更高

# 檢查 pip 版本
pip3 --version
```

### 檢查依賴安裝

```bash
# 檢查所有依賴
pip3 list | grep -E "openai|fastapi|numpy|uvicorn|pydantic"

# 應該顯示類似：
# openai        1.12.0
# fastapi       0.104.0
# numpy         1.24.0
# uvicorn       0.24.0
# pydantic      2.5.0
```

### 檢查 API Key

```bash
# 檢查是否設定
echo $OPENAI_API_KEY

# 應該顯示: sk-...
```

### 運行健康檢查

```bash
# 如果有 verify_system.py
python3 verify_system.py

# 或手動檢查
python3 -c "from openai import OpenAI; print('✅ OpenAI 安裝正常')"
```

---

## 📁 初始化數據

### 檢查數據文件

```bash
# 檢查教材文件
ls -lh data/docs/
# 應該有: ml_basics.txt, deep_learning.txt, nlp_intro.txt

# 檢查情境文件
ls -lh data/scenarios/
# 應該有: scenarios_12.json

# 檢查本體論
ls -lh data/ontology/
# 應該有: knowledge_ontology.txt
```

### 首次向量化

**第一次運行時**，系統會自動向量化教材：

```bash
python3 main_parallel.py
```

**預期輸出**：
```
📚 初始化文件向量...
⚠️  首次啟動，需要調用 OpenAI API 生成向量
⏳ 預計需要 10-15 秒，請稍候...
  📄 載入: ml_basics.txt (661 字)
  📄 載入: deep_learning.txt (1106 字)
  📄 載入: nlp_intro.txt (1440 字)
✅ 已向量化文件: ml_basics.txt
✅ 已向量化文件: deep_learning.txt
✅ 已向量化文件: nlp_intro.txt
💾 向量已儲存至: vectors.pkl
```

**之後運行**只需 2-3 秒：
```
📚 初始化文件向量...
✅ 已載入 3 個向量
✅ 使用已儲存的向量（快速啟動）
```

---

## 🔧 故障排除

### 問題 1：pip3 command not found

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip

# macOS
brew install python3

# 或使用 python3 -m pip
python3 -m pip install --user -r requirements.txt
```

### 問題 2：Permission denied

```bash
# 使用 --user 標誌
pip3 install --user -r requirements.txt

# 或使用虛擬環境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 問題 3：SSL 證書錯誤

```bash
# 臨時解決（不推薦用於生產）
pip3 install --user --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### 問題 4：numpy 安裝失敗

```bash
# 先安裝編譯工具
sudo apt install build-essential python3-dev

# 再安裝 numpy
pip3 install --user numpy
```

### 問題 5：ModuleNotFoundError after install

```bash
# 檢查 Python 路徑
python3 -m site --user-site

# 確保該路徑在 PYTHONPATH 中
export PYTHONPATH=$PYTHONPATH:$(python3 -m site --user-site)
```

---

## ✅ 完整安裝檢查清單

### 基礎環境

- [ ] Python 3.8+ 已安裝
- [ ] pip3 可用
- [ ] Git 已安裝（可選）

### 專案設置

- [ ] 代碼已克隆或下載
- [ ] 在專案根目錄
- [ ] requirements.txt 存在

### 依賴安裝

- [ ] 所有依賴已安裝
- [ ] 無錯誤訊息
- [ ] 可以 import openai, fastapi 等

### API 配置

- [ ] OpenAI API Key 已獲取
- [ ] 環境變數已設定
- [ ] echo $OPENAI_API_KEY 有輸出

### 數據文件

- [ ] data/docs/ 有 3 個 .txt 文件
- [ ] data/scenarios/ 有配置文件
- [ ] data/ontology/ 有本體論文件

### 運行測試

- [ ] python3 main_parallel.py 可運行
- [ ] 首次向量化成功
- [ ] vectors.pkl 已生成
- [ ] 可以處理查詢

---

## 🎯 下一步

安裝完成後，您可以：

### 立即開始

```bash
# 運行主程序
python3 main_parallel.py

# 或啟動 Web 界面
python3 web_api.py &
open web/index.html
```

### 了解更多

- **快速開始**: [01_QUICK_START.md](01_QUICK_START.md)
- **系統概述**: [10_SYSTEM_OVERVIEW.md](10_SYSTEM_OVERVIEW.md)
- **命令參考**: [20_COMMAND_REFERENCE.md](20_COMMAND_REFERENCE.md)

### 自定義配置

- **編輯教材**: `data/docs/`
- **調整配置**: `config.py`
- **自定義情境**: `data/scenarios/scenarios_12.json`

---

**安裝完成！準備開始使用！** 🎉
