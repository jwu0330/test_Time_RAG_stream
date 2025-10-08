# 執行指南

## 📂 文件組織規則

⚠️ **重要規則**：
- 📝 **所有說明文件** → `README_ALL/` 目錄
- 🔧 **所有 .sh 腳本** → `README_ALL/BASH_ALL/` 目錄
- 💻 **核心程式碼** → 根目錄或 `core/`, `scripts/` 等目錄

例如：
- ✅ `README_ALL/README_SIMPLE.md` - 正確
- ✅ `README_ALL/BASH_ALL/SYNC_NOW.sh` - 正確
- ❌ `SYNC_NOW.sh` - 錯誤（應放在 BASH_ALL/）
- ❌ `README.txt` - 錯誤（應放在 README_ALL/）

---

## 🚀 首次設置

### 步驟 1：安裝依賴
```bash
# 如果沒有 pip，先安裝
sudo apt install python3-pip

# 安裝依賴
pip3 install --user -r requirements.txt
```

### 步驟 2：設定 API Key
```bash
export OPENAI_API_KEY="your-api-key-here"

# 或創建 .env 文件
cp .env.example .env
# 編輯 .env 並添加你的 API Key
```

---

## 📝 日常使用

### 運行測試
```bash
python3 scripts/run_test.py
```

### 啟動 Web 界面
```bash
python3 web_api.py
# 然後在瀏覽器打開 web_interface.html
```

### 測試 D4 邏輯
```bash
python3 tests/test_d4_logic.py
```

### 完整系統測試
```bash
python3 tests/test_system.py
```

### 直接運行主程序
```bash
python3 main_parallel.py
```

---

## 🔧 自定義配置

### 修改教材
```bash
# 1. 將教材放入 data/docs/ 目錄
cp your_materials/* data/docs/

# 2. 編輯配置
nano config.py
# 更新 KNOWLEDGE_POINTS 映射

# 3. 刪除舊向量並重新生成
rm vectors.pkl vectors.json
python3 scripts/run_test.py
```

### 生成新的情境
```bash
python3 scripts/scenario_generator.py
```

### 調整情境內容
```bash
# 編輯 data/scenarios/ 目錄中的 JSON 文件
nano data/scenarios/scenario_08.json
```

---

## 🗑️ 清理環境

### 清理多餘文件
```bash
# 查看清理說明
cat CLEANUP_FILES.md

# 執行清理（複製 CLEANUP_FILES.md 中的命令）
```

### 刪除向量文件
```bash
rm -f vectors.pkl vectors.json
```

### 刪除歷史記錄
```bash
rm -f history.json
```

### 刪除緩存
```bash
rm -rf __pycache__
rm -rf core/__pycache__
```

---

## 📤 推送到 GitHub

### 添加並提交
```bash
git add .
git commit -m "您的提交訊息"
```

### 推送
```bash
git push origin main
# 或
git push origin master
```

---

## 🐛 故障排除

### API Key 錯誤
```bash
export OPENAI_API_KEY="your-key"
```

### 模組找不到
```bash
pip3 install --user -r requirements.txt
```

### 向量化失敗
```bash
rm vectors.pkl vectors.json
python3 scripts/run_test.py
```

### 情境文件不存在
```bash
python3 scripts/scenario_generator.py
```

---

## 📖 查看文檔

- **快速開始**：`README_SIMPLE.md`
- **完整文檔**：`README_FULL.md`
- **清理說明**：`CLEANUP_FILES.md`
