#!/bin/bash

# RAG 流式系統安裝腳本

echo "🚀 RAG 流式中斷與續寫系統 - 安裝腳本"
echo "========================================================"

# 檢查 Python 版本
echo ""
echo "📋 檢查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python 版本: $python_version"

# 創建虛擬環境（可選）
read -p "是否創建虛擬環境? (y/n): " create_venv
if [ "$create_venv" = "y" ]; then
    echo ""
    echo "🔧 創建虛擬環境..."
    python3 -m venv venv
    echo "✅ 虛擬環境已創建"
    echo ""
    echo "請執行以下命令激活虛擬環境:"
    echo "   source venv/bin/activate"
    echo ""
    read -p "按 Enter 繼續..."
fi

# 安裝依賴
echo ""
echo "📦 安裝 Python 依賴..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 依賴安裝成功"
else
    echo "❌ 依賴安裝失敗"
    exit 1
fi

# 創建必要目錄
echo ""
echo "📁 創建必要目錄..."
mkdir -p docs scenarios results

echo "✅ 目錄結構已創建"

# 檢查 .env 文件
echo ""
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件"
    read -p "是否現在設定 OPENAI_API_KEY? (y/n): " setup_key
    
    if [ "$setup_key" = "y" ]; then
        read -p "請輸入您的 OpenAI API Key: " api_key
        echo "OPENAI_API_KEY=$api_key" > .env
        echo "✅ API Key 已儲存到 .env 文件"
    else
        echo "⚠️  請稍後手動設定 OPENAI_API_KEY"
        echo "   方法1: export OPENAI_API_KEY='your-key'"
        echo "   方法2: 創建 .env 文件並添加 OPENAI_API_KEY=your-key"
    fi
else
    echo "✅ .env 文件已存在"
fi

# 執行測試
echo ""
read -p "是否執行系統測試? (y/n): " run_test

if [ "$run_test" = "y" ]; then
    echo ""
    echo "🧪 執行系統測試..."
    python3 test_system.py
fi

echo ""
echo "========================================================"
echo "✅ 安裝完成！"
echo ""
echo "📖 快速開始:"
echo "   1. 確保已設定 OPENAI_API_KEY"
echo "   2. 執行: python quick_start.py"
echo "   3. 查看: JIM_README.md 獲取詳細文檔"
echo ""
echo "🎯 主要命令:"
echo "   python test_system.py   - 執行系統測試"
echo "   python quick_start.py   - 快速測試"
echo "   python main.py          - 完整測試流程"
echo ""
echo "========================================================"
