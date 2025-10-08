# Git 同步指南

## 📂 文件組織規則

⚠️ **本專案的文件組織規則**：
- 📝 **所有說明文件** → `README_ALL/` 目錄
- 🔧 **所有 .sh 腳本** → `README_ALL/BASH_ALL/` 目錄
- 💻 **核心程式碼** → 根目錄或 `core/`, `scripts/` 等目錄

這樣做的好處：
1. ✅ 根目錄保持簡潔
2. ✅ 文檔集中管理
3. ✅ 腳本統一存放
4. ✅ 易於維護和查找

---

## 📤 同步到遠端倉庫

### 方式 1：標準流程（推薦）

```bash
# 1. 查看狀態
git status

# 2. 添加所有變更
git add .

# 3. 提交變更
git commit -m "重組專案架構並更新文檔"

# 4. 推送到遠端
git push origin main
```

### 方式 2：如果主分支是 master

```bash
git push origin master
```

### 方式 3：第一次推送或設定上游

```bash
git push -u origin main
```

---

## 📝 建議的提交訊息

### 本次重組的提交訊息

```
重組專案架構並更新文檔

主要變更：
- 新增 core/ 目錄存放核心模組
- 新增 data/ 目錄整合教材和情境
- 新增 tests/ 目錄存放測試文件
- 新增 scripts/ 目錄存放工具腳本
- 刪除根目錄重複文件
- 更新所有說明文檔以反映新架構
- 新增架構檢查和重組報告

目錄結構：
- core/: vector_store, rag_module, scenario_module 等核心模組
- data/: docs, scenarios, knowledge_relations.json
- tests/: test_system, test_d4_logic
- scripts/: run_test, scenario_generator, reorganize

文檔更新：
- README_SIMPLE.md: 更新路徑和命令
- EXECUTION_GUIDE.md: 更新所有執行命令
- 新增 GIT_SYNC.md: Git 同步指南
- 新增 ARCHITECTURE_CHECK.md: 架構檢查報告
```

---

## 🔍 推送前檢查

```bash
# 查看將要提交的文件
git status

# 查看具體變更
git diff

# 查看已暫存的變更
git diff --staged
```

---

## 🚨 常見問題

### 問題 1：推送被拒絕

```bash
# 先拉取遠端變更
git pull origin main

# 解決衝突後再推送
git push origin main
```

### 問題 2：忘記添加文件

```bash
# 添加遺漏的文件
git add <file>

# 修改上次提交
git commit --amend
```

### 問題 3：想要撤銷某些變更

```bash
# 撤銷未暫存的變更
git checkout -- <file>

# 撤銷已暫存的變更
git reset HEAD <file>
```

---

## 📋 完整同步命令（複製即用）

```bash
cd /home/jim/code/python/test_Time_RAG_stream

git add .

git commit -m "重組專案架構並更新文檔

- 新增 core/data/tests/scripts 目錄
- 刪除根目錄重複文件
- 更新所有說明文檔
- 新增架構檢查報告"

git push origin main
```

---

## 🎯 推送後驗證

推送成功後，訪問你的 GitHub 倉庫確認：

1. ✅ 新目錄 (core/, data/, tests/, scripts/) 已出現
2. ✅ 重複文件已刪除
3. ✅ 文檔已更新
4. ✅ 提交訊息清晰

---

## 📚 相關文檔

- **架構檢查**: `ARCHITECTURE_CHECK.md`
- **重組報告**: `REORGANIZATION_REPORT.md`
- **執行指南**: `EXECUTION_GUIDE.md`
