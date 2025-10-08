#!/bin/bash
# Git 同步腳本 - 一鍵執行

echo "🚀 開始同步到遠端倉庫..."
echo ""

# 顯示當前狀態
echo "📊 當前狀態："
git status
echo ""

# 詢問是否繼續
read -p "是否繼續同步？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ 已取消同步"
    exit 1
fi

# 添加所有變更
echo "📦 添加所有變更..."
git add .

# 提交
echo "💾 提交變更..."
git commit -m "重組專案架構並更新文檔

主要變更：
- 重組目錄結構：core/, data/, tests/, scripts/
- 整理文檔到 README_ALL/ 目錄
- 刪除根目錄重複文件
- 新增根目錄 README.md
- 更新所有文檔路徑和命令

新架構：
- core/: 核心模組（vector_store, rag_module, scenario_module 等）
- data/: 數據文件（docs, scenarios, knowledge_relations.json）
- tests/: 測試文件（test_system, test_d4_logic）
- scripts/: 工具腳本（run_test, scenario_generator）
- README_ALL/: 完整文檔集合

根目錄保留：
- main_parallel.py: 主程序
- web_api.py: Web API
- config.py: 配置文件
- README.md: 專案說明"

# 推送
echo "🚀 推送到遠端..."
git push origin main

# 檢查結果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 同步成功！"
    echo ""
    echo "📊 最終狀態："
    git status
else
    echo ""
    echo "❌ 推送失敗，請檢查錯誤信息"
    echo ""
    echo "💡 可能的解決方案："
    echo "1. 如果主分支是 master，執行: git push origin master"
    echo "2. 如果需要強制推送，執行: git push -f origin main"
    echo "3. 如果需要先拉取，執行: git pull origin main"
fi
