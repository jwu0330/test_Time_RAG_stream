# 文檔索引

**📅 更新日期**: 2025-10-09  
**📚 文檔版本**: 3.1（Poetry 環境管理）

---

## 🎯 如何使用本文檔

### 我是新用戶 → 從這裡開始

1. **[01_QUICK_START.md](01_QUICK_START.md)** - 5分鐘快速上手
2. **[02_INSTALLATION.md](02_INSTALLATION.md)** - 詳細安裝步驟
3. **[10_SYSTEM_OVERVIEW.md](10_SYSTEM_OVERVIEW.md)** - 了解系統功能

### 我想深入了解系統

4. **[11_SIMPLIFICATION_SUMMARY.md](11_SIMPLIFICATION_SUMMARY.md)** - 系統簡化總結
5. **[19_THREE_APIS_ARCHITECTURE.md](19_THREE_APIS_ARCHITECTURE.md)** - 三個 API 架構
6. **[20_FOUR_PARALLEL_ARCHITECTURE.md](20_FOUR_PARALLEL_ARCHITECTURE.md)** - 四個並行分支
7. 查看 `core/` 目錄中的源代碼了解架構細節

### 我要使用系統

8. 查看主 `README.md` 了解常用命令
9. 查看 `web/README.md` 了解 Web 界面使用
10. 查看 `web_api.py` 了解 API 端點

---

## 📁 文檔結構

### 第一類：快速開始（00-09）

| 文檔 | 用途 | 閱讀時間 |
|------|------|---------|
| **00_README_INDEX.md** | 文檔導航（本文件） | 2分鐘 |
| **01_QUICK_START.md** | 快速開始指南 | 5分鐘 |
| **02_INSTALLATION.md** | 詳細安裝說明 | 10分鐘 |
| **03_POETRY_GUIDE.md** | Poetry 使用指南 | 15分鐘 |

### 第二類：系統說明（10-19）

| 文檔 | 用途 | 閱讀時間 |
|------|------|---------|
| **10_SYSTEM_OVERVIEW.md** | 系統完整概述 | 15分鐘 |
| **11_SIMPLIFICATION_SUMMARY.md** | 系統簡化總結 | 10分鐘 |
| **16_TROUBLESHOOTING.md** | 故障排除指南 | 15分鐘 |
| **19_THREE_APIS_ARCHITECTURE.md** | 三個 API 架構說明 | 15分鐘 |

### 第三類：架構說明（20-29）

| 文檔 | 用途 | 閱讀時間 |
|------|------|---------|
| **20_FOUR_PARALLEL_ARCHITECTURE.md** | 四個並行分支架構 | 15分鐘 |

### 第四類：腳本與工具

| 位置 | 用途 |
|------|------|
| `BASH_ALL/` | 所有執行腳本 |
| `README.md` | 主要說明文件 |
| `config.py` | 系統配置文件 |
| `core/` | 核心模組源代碼 |
| `web/` | Web 界面文件 |
| `web_api.py` | API 後端實現 |

### 第五類：歸檔（ARCHIVE/）

舊版文檔和過時報告，僅供參考。

---

## 🚀 常見場景快速導航

### 場景 1：第一次使用

```
01_QUICK_START.md → 02_INSTALLATION.md → 運行系統
```

### 場景 2：了解系統原理

```
10_SYSTEM_OVERVIEW.md → 12_DUAL_THREAD_TIMING.md → 閱讀源代碼
```

### 場景 3：使用 Web 界面

```
web/README.md → 啟動並使用
```

### 場景 4：自定義教材

```
修改 config.py → 添加文件到 data/docs/ → 重新向量化
```

---

## 📊 文檔狀態

### ✅ 已完成（最新版本）

- [x] 00_README_INDEX.md - 文檔索引
- [x] 00_DOC_REORGANIZATION_2025-10-08.md - 整理報告
- [x] 01_QUICK_START.md - 快速開始
- [x] 02_INSTALLATION.md - 安裝指南
- [x] 10_SYSTEM_OVERVIEW.md - 系統概述
- [x] 12_DUAL_THREAD_TIMING.md - 雙線程計時系統（舊版）
- [x] 13_RESPONSES_API_ARCHITECTURE.md - Responses API 架構
- [x] 14_MIGRATION_GUIDE.md - 遷移指南
- [x] 15_SETUP_SUMMARY.md - 設置總結
- [x] 16_TROUBLESHOOTING.md - 故障排除
- [x] 17_TIMING_UPDATES.md - 時間記錄更新
- [x] DOC_REORG_SUMMARY.md - 文檔整理總結

### 📦 已歸檔（ARCHIVE/）

- [x] API_IMPLEMENTATION_REPORT.md
- [x] STARTUP_ANALYSIS.md
- [x] TIMING_IMPLEMENTATION_REPORT.md
- [x] WEB_FILES_ORGANIZATION.md
- [x] WEB_INTERFACE_GUIDE.md
- [x] WEB_TESTING_GUIDE.md
- [x] GIT_SYNC.md

---

## 🎯 推薦學習路徑

### 路徑 A：快速上手（30分鐘）

```
1. 01_QUICK_START.md（5分鐘）
   ├─ 理解系統基本功能
   └─ 完成安裝和運行

2. 10_SYSTEM_OVERVIEW.md（15分鐘）
   ├─ 了解四向度分類
   ├─ 了解24種情境
   └─ 了解雙線程架構

3. 啟動 Web 界面（10分鐘）
   └─ 實際體驗系統
```

### 路徑 B：深入理解（2小時）

```
1. 10_SYSTEM_OVERVIEW.md（15分鐘）
   └─ 系統整體概述

2. 13_RESPONSES_API_ARCHITECTURE.md（20分鐘）
   ├─ Responses API 架構說明
   ├─ 雙回合流程詳解
   └─ 性能優化

3. 17_TIMING_UPDATES.md（10分鐘）
   └─ 時間記錄系統說明

4. 閱讀源代碼（45分鐘）
   ├─ main_parallel.py - 主流程
   ├─ core/ - 核心模組
   └─ web_api.py - API 實現

5. 修改配置（10分鐘）
   └─ config.py - 自定義參數
```

### 路徑 C：開發者（3小時）

完整閱讀所有文檔和源代碼，包括：
- 系統原理和架構
- 核心模組實現
- API 端點和數據流
- 自定義和擴展方法
- 測試和調試技巧

---

## 🔍 快速搜索

### 按主題查找

**安裝相關**
- [02_INSTALLATION.md](02_INSTALLATION.md)
- 主 README.md - 環境需求

**使用相關**
- [01_QUICK_START.md](01_QUICK_START.md)
- 主 README.md - 常用命令
- web/README.md - Web 界面

**開發相關**
- [10_SYSTEM_OVERVIEW.md](10_SYSTEM_OVERVIEW.md)
- [13_RESPONSES_API_ARCHITECTURE.md](13_RESPONSES_API_ARCHITECTURE.md)
- [17_TIMING_UPDATES.md](17_TIMING_UPDATES.md)
- config.py - 配置文件
- core/ - 源代碼

**故障排除**
- [16_TROUBLESHOOTING.md](16_TROUBLESHOOTING.md)
- [14_MIGRATION_GUIDE.md](14_MIGRATION_GUIDE.md)

---

## 💡 文檔使用技巧

### 1. 使用目錄功能

所有文檔都包含目錄（TOC），點擊快速跳轉。

### 2. 利用搜索功能

使用 Ctrl+F（或 Cmd+F）搜索關鍵詞。

### 3. 跟隨交叉引用

文檔之間有超鏈接，方便跳轉閱讀。

### 4. 從問題出發

遇到問題時，先查看錯誤信息和日誌輸出。

### 5. 實踐中學習

邊閱讀邊實際操作，效果最好。

---

## 📞 獲取幫助

### 文檔內查找

1. 查看本索引找到相關文檔
2. 閱讀相應章節
3. 查看故障排除指南

### 外部資源

- **GitHub Issues**: 提交問題和建議
- **項目 README**: 查看最新更新
- **代碼註釋**: 直接閱讀源代碼

---

## 🔄 文檔更新記錄

### 2025-10-08 - 版本 2.0

- ✅ 完成文檔重組
- ✅ 創建統一編號系統
- ✅ 整合重複內容
- ✅ 移除過時信息
- ✅ 添加雙線程計時文檔
- ✅ 創建文檔索引

### 下次更新計劃

- [ ] 完成所有編號文檔的創建
- [ ] 歸檔舊文檔
- [ ] 添加更多實例和截圖
- [ ] 創建視頻教程鏈接

---

## ✅ 檢查清單

使用文檔前，確認：

- [ ] 已閱讀本索引
- [ ] 明確自己的需求（新用戶/開發者/問題排除）
- [ ] 選擇合適的學習路徑
- [ ] 準備好實際操作環境

---

**準備好了？從 [01_QUICK_START.md](01_QUICK_START.md) 開始吧！** 🚀
