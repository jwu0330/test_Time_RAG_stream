#!/bin/bash
# 在虛擬環境中安裝依賴

echo "📦 在虛擬環境中安裝 Responses API RAG 系統依賴"
echo "=================================================="
echo ""

# 檢查虛擬環境
if [ ! -d ".venv" ]; then
    echo "⚠️  虛擬環境不存在，正在創建..."
    python3 -m venv .venv
    echo "✅ 虛擬環境已創建"
fi

# 激活虛擬環境
echo "🔄 激活虛擬環境..."
source .venv/bin/activate

# 檢查是否成功激活
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ 無法激活虛擬環境"
    exit 1
fi

echo "✅ 虛擬環境已激活: $VIRTUAL_ENV"
echo ""

# 升級 pip
echo "📦 升級 pip..."
pip install --upgrade pip
echo ""

# 安裝依賴
echo "📦 安裝專案依賴到虛擬環境..."
echo "   - openai (最新版 >= 1.54.0)"
echo "   - numpy"
echo "   - python-dotenv"
echo "   - fastapi"
echo "   - uvicorn"
echo "   - pydantic"
echo ""

pip install -U openai numpy python-dotenv fastapi uvicorn pydantic

# 檢查安裝結果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 所有依賴安裝成功！"
    echo ""
    echo "📋 虛擬環境中已安裝的套件版本："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    pip list | grep -E "openai|numpy|python-dotenv|fastapi|uvicorn|pydantic"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 虛擬環境位置: $VIRTUAL_ENV"
    echo ""
    echo "🎯 下一步："
    echo "1. 激活虛擬環境:"
    echo "   source .venv/bin/activate"
    echo ""
    echo "2. 設定 API Key:"
    echo "   export OPENAI_API_KEY='your-api-key'"
    echo ""
    echo "3. 測試系統:"
    echo "   python main_parallel.py"
    echo ""
    echo "4. 或啟動 Web API:"
    echo "   python web_api.py"
else
    echo ""
    echo "❌ 安裝失敗，請檢查錯誤信息"
    exit 1
fi

# 保持虛擬環境激活
echo ""
echo "💡 提示：虛擬環境仍處於激活狀態"
echo "   要退出虛擬環境，請執行: deactivate"
