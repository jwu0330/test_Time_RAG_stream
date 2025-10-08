#!/bin/bash
# 完整安裝所有依賴

echo "📦 安裝 Responses API RAG 系統所有依賴"
echo "========================================"
echo ""

# 檢查 pip3
if ! command -v pip3 &> /dev/null; then
    echo "⚠️  pip3 未安裝，正在安裝..."
    sudo apt update
    sudo apt install -y python3-pip
fi

echo "✅ pip3 已就緒"
echo ""

# 升級 pip
echo "📦 升級 pip..."
pip3 install --user --upgrade pip
echo ""

# 安裝依賴
echo "📦 安裝專案依賴..."
echo "   - openai (最新版 >= 1.54.0)"
echo "   - numpy"
echo "   - python-dotenv"
echo "   - fastapi"
echo "   - uvicorn"
echo "   - pydantic"
echo ""

pip3 install --user -U openai numpy python-dotenv fastapi uvicorn pydantic

# 檢查安裝結果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 所有依賴安裝成功！"
    echo ""
    echo "📋 已安裝的套件版本："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    pip3 list | grep -E "openai|numpy|python-dotenv|fastapi|uvicorn|pydantic"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🎯 下一步："
    echo "1. 設定 API Key:"
    echo "   export OPENAI_API_KEY='your-api-key'"
    echo ""
    echo "2. 測試系統:"
    echo "   python3 main_parallel.py"
    echo ""
    echo "3. 或啟動 Web API:"
    echo "   python3 web_api.py"
else
    echo ""
    echo "❌ 安裝失敗，請檢查錯誤信息"
    echo ""
    echo "💡 手動安裝命令："
    echo "pip3 install --user -U openai numpy python-dotenv fastapi uvicorn pydantic"
    exit 1
fi
