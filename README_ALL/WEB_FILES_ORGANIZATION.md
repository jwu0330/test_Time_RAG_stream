# Web 文件整理指南

## 📊 當前狀態

### 根目錄的 Web 文件（需要移動）
```
test_Time_RAG_stream/
├── web_interface.html              ❌ 應移到 web/
├── web_interface_interactive.html  ❌ 應移到 web/
└── web_api.py                      ✅ 保留（後端 API）
```

### 目標結構
```
test_Time_RAG_stream/
├── web_api.py                      ✅ 後端 API（保留在根目錄）
│
└── web/                            🌐 所有前端文件
    ├── index.html                  ✅ 主界面（新的互動式）
    ├── old_interface.html          📦 舊界面（備份）
    ├── interactive.html            📦 互動式界面（備份）
    ├── app.js                      ✅ JavaScript 邏輯
    └── README.md                   ✅ 使用說明
```

---

## 🔧 整理步驟

### 方式 1：使用腳本（推薦）

```bash
chmod +x README_ALL/BASH_ALL/organize_web_files.sh
./README_ALL/BASH_ALL/organize_web_files.sh
```

### 方式 2：手動執行

```bash
cd /home/jim/code/python/test_Time_RAG_stream

# 移動舊界面文件
mv web_interface.html web/old_interface.html
mv web_interface_interactive.html web/interactive.html

# 檢查結果
ls -lh web/
```

---

## 📁 整理後的完整結構

```
test_Time_RAG_stream/
├── README.md
├── main_parallel.py
├── web_api.py              ← 後端 API（保留）
├── config.py
│
├── core/                   # 核心模組
├── data/                   # 數據文件
├── tests/                  # 測試文件
├── scripts/                # 工具腳本
│
├── web/                    # 🌐 所有 Web 前端文件
│   ├── index.html         # 主界面（使用這個）
│   ├── app.js             # JavaScript
│   ├── old_interface.html # 舊界面（備份）
│   ├── interactive.html   # 另一個版本（備份）
│   └── README.md          # 使用說明
│
└── README_ALL/             # 📝 所有文檔
    └── BASH_ALL/           # 🔧 所有腳本
```

---

## 🎯 為什麼這樣組織？

### web_api.py 保留在根目錄
- ✅ 它是後端服務，不是前端文件
- ✅ 與 main_parallel.py 同級
- ✅ 方便直接運行：`python3 web_api.py`

### 前端文件都在 web/
- ✅ HTML、CSS、JavaScript 集中管理
- ✅ 清晰的前後端分離
- ✅ 易於部署和維護

---

## 🚀 使用方式

### 啟動系統

```bash
# 1. 啟動後端 API（在根目錄）
python3 web_api.py

# 2. 打開前端界面（在 web/ 目錄）
open web/index.html
```

### 選擇界面版本

```bash
# 主界面（推薦）
open web/index.html

# 舊界面（簡單版）
open web/old_interface.html

# 互動式界面（功能完整）
open web/interactive.html
```

---

## 📊 文件說明

### web/index.html
- **用途**: 主要的互動式界面
- **特色**: 完整功能、現代設計
- **推薦**: ⭐⭐⭐⭐⭐

### web/old_interface.html
- **用途**: 原始的簡單界面
- **特色**: 基礎功能
- **推薦**: ⭐⭐⭐

### web/interactive.html
- **用途**: 另一個互動式版本
- **特色**: 與 index.html 類似
- **推薦**: ⭐⭐⭐⭐

### web/app.js
- **用途**: JavaScript 邏輯
- **功能**: API 調用、界面交互

---

## 🔄 Git 同步

整理後記得同步到遠端：

```bash
git add .
git commit -m "整理 Web 文件到 web/ 目錄

- 移動 web_interface.html → web/old_interface.html
- 移動 web_interface_interactive.html → web/interactive.html
- 保留 web_api.py 在根目錄
- 新增 web/index.html 作為主界面"

git push origin main
```

---

## ✅ 檢查清單

整理完成後，確認：

- [ ] `web/` 目錄包含所有前端文件
- [ ] `web_api.py` 保留在根目錄
- [ ] `web/index.html` 可以正常打開
- [ ] API 和前端可以正常通信
- [ ] 舊文件已備份到 `web/old_*`

---

## 🎯 立即執行

```bash
# 複製這段命令執行
cd /home/jim/code/python/test_Time_RAG_stream
mv web_interface.html web/old_interface.html
mv web_interface_interactive.html web/interactive.html
echo "✅ Web 文件整理完成！"
ls -lh web/
```

---

**整理後的結構更清晰、更專業！** 🎉
