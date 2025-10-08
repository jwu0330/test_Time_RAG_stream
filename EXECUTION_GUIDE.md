# 執行指南

## 🚀 首次設置

### 步驟 1：創建虛擬環境
```bash
python3 -m venv venv
```

### 步驟 2：激活環境
```bash
source venv/bin/activate
```

### 步驟 3：安裝依賴
```bash
pip install -r requirements.txt
```

### 步驟 4：設定 API Key
```bash
export OPENAI_API_KEY="your-api-key-here"
```

---

## 📝 日常使用

### 運行測試
```bash
source venv/bin/activate
python RUN_TEST.py
```

### 啟動 Web 界面
```bash
source venv/bin/activate
python web_api.py
# 然後在瀏覽器打開 web_interface.html
```

### 測試 D4 邏輯
```bash
source venv/bin/activate
python test_d4_logic.py
```

### 完整系統測試
```bash
source venv/bin/activate
python test_system.py
```

---

## 🔧 自定義配置

### 修改教材
```bash
# 1. 將教材放入 docs/ 目錄
cp your_materials/* docs/

# 2. 編輯配置
nano config.py
# 更新 KNOWLEDGE_POINTS 映射

# 3. 刪除舊向量並重新生成
rm vectors.pkl vectors.json
python RUN_TEST.py
```

### 生成新的情境
```bash
source venv/bin/activate
python scenario_generator.py
```

### 調整情境內容
```bash
# 編輯 scenarios_24/ 目錄中的 JSON 文件
nano scenarios_24/scenario_08.json
```

---

## 🗑️ 清理環境

### 清理多餘文件
```bash
# 查看清理說明
cat CLEANUP_FILES.md

# 執行清理（複製 CLEANUP_FILES.md 中的命令）
```

### 刪除虛擬環境
```bash
rm -rf venv/
```

### 刪除向量文件
```bash
rm -f vectors.pkl vectors.json
```

### 刪除歷史記錄
```bash
rm -f history.json
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
source venv/bin/activate
pip install -r requirements.txt
```

### 向量化失敗
```bash
rm vectors.pkl vectors.json
python RUN_TEST.py
```

### 情境文件不存在
```bash
python scenario_generator.py
```

---

## 📖 查看文檔

- **快速開始**：`README_SIMPLE.md`
- **完整文檔**：`README_FULL.md`
- **清理說明**：`CLEANUP_FILES.md`
