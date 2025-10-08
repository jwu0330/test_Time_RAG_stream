#!/bin/bash
# 測試 Responses API 雙回合流程

echo "🧪 測試 Responses API 雙回合 RAG 系統"
echo "========================================"
echo ""

# 檢查是否在虛擬環境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  未激活虛擬環境，正在激活..."
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        echo "✅ 虛擬環境已激活: $VIRTUAL_ENV"
    else
        echo "❌ 找不到虛擬環境，請先運行: bash README_ALL/BASH_ALL/cleanup_and_reinstall.sh"
        exit 1
    fi
else
    echo "✅ 虛擬環境已激活: $VIRTUAL_ENV"
fi
echo ""

# 檢查 OpenAI API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  未設定 OPENAI_API_KEY"
    echo "請執行: export OPENAI_API_KEY='your-api-key'"
    exit 1
fi

echo "✅ API Key 已設定"
echo ""

# 檢查 OpenAI 版本
echo "📦 檢查 OpenAI SDK 版本..."
OPENAI_VERSION=$(python3 -c "import openai; print(openai.__version__)" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "   OpenAI SDK 版本: $OPENAI_VERSION"
else
    echo "❌ OpenAI SDK 未安裝"
    exit 1
fi
echo ""

# 運行主程序測試
echo "🚀 運行主程序測試..."
echo "========================================"
python3 main_parallel.py

echo ""
echo "✅ 測試完成！"
