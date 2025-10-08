#!/bin/bash

echo "=================================="
echo "📤 推送到 GitHub"
echo "=================================="
echo ""

# 檢查是否有遠端倉庫
if ! git remote | grep -q origin; then
    echo "📌 添加遠端倉庫..."
    git remote add origin git@github.com:jwu0330/test_Time_RAG_stream.git
    echo "✅ 遠端倉庫已添加"
else
    echo "✅ 遠端倉庫已存在"
    # 確保 URL 正確
    git remote set-url origin git@github.com:jwu0330/test_Time_RAG_stream.git
fi

echo ""

# 檢查 Git 狀態
echo "📋 檢查文件狀態..."
git status

echo ""

# 添加所有文件
echo "📦 添加文件..."
git add .

echo ""

# 提交
echo "💾 提交更改..."
git commit -m "完整的 RAG 流式系統 - 包含 24 種情境、並行處理、Web 界面"

echo ""

# 推送
echo "📤 推送到 GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✅ 推送成功！"
    echo "=================================="
    echo ""
    echo "GitHub 倉庫："
    echo "https://github.com/jwu0330/test_Time_RAG_stream"
else
    echo ""
    echo "=================================="
    echo "⚠️  推送失敗"
    echo "=================================="
    echo ""
    echo "可能的原因："
    echo "1. 分支名稱不是 main（可能是 master）"
    echo "2. 需要先拉取遠端更新"
    echo ""
    echo "嘗試其他分支："
    echo "  git push -u origin master"
    echo ""
    echo "或先拉取："
    echo "  git pull origin main --rebase"
    echo "  git push -u origin main"
fi
