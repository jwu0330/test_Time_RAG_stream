#!/bin/bash
# 快速測試腳本 - 自動激活虛擬環境並運行

echo "🚀 快速測試 Responses API 系統"
echo "================================"
echo ""

# 自動激活虛擬環境
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f ".venv/bin/activate" ]; then
        echo "🔄 激活虛擬環境..."
        source .venv/bin/activate
        echo "✅ 虛擬環境已激活"
    else
        echo "❌ 找不到虛擬環境"
        echo "請先運行: bash README_ALL/BASH_ALL/cleanup_and_reinstall.sh"
        exit 1
    fi
fi

# 檢查 API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  未設定 OPENAI_API_KEY"
    echo ""
    echo "請設定您的 API Key:"
    read -p "輸入 OpenAI API Key: " api_key
    export OPENAI_API_KEY="$api_key"
    echo "✅ API Key 已設定"
fi

echo ""
echo "📊 環境信息："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "虛擬環境: $VIRTUAL_ENV"
echo "Python: $(python3 --version)"
echo "OpenAI SDK: $(python3 -c 'import openai; print(openai.__version__)' 2>/dev/null || echo '未安裝')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 運行測試
echo "🧪 運行測試..."
echo ""
python3 main_parallel.py

echo ""
echo "✅ 測試完成！"
echo ""
echo "💡 提示："
echo "  - 要退出虛擬環境: deactivate"
echo "  - 要啟動 Web API: python3 web_api.py"
