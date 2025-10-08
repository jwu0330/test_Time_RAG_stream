#!/bin/bash
# 啟動 Web API 服務

echo "🚀 啟動 Responses API 雙回合 RAG 系統 Web API"
echo "=============================================="
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

# 檢查依賴
echo "📦 檢查依賴..."
python3 -c "import openai, fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少依賴，請運行: bash README_ALL/BASH_ALL/cleanup_and_reinstall.sh"
    exit 1
fi
echo "✅ 依賴檢查通過"
echo ""

echo "✅ 啟動 Web API 服務..."
echo "📡 API 地址: http://0.0.0.0:8000"
echo "📖 API 文檔: http://0.0.0.0:8000/docs"
echo "💡 按 Ctrl+C 停止服務"
echo ""

python3 web_api.py
