#!/bin/bash
# 清理用戶目錄的包並在虛擬環境中重新安裝

echo "🧹 清理並重新安裝到虛擬環境"
echo "================================"
echo ""

# 步驟 1: 清理用戶目錄中的包
echo "📦 步驟 1: 清理用戶目錄中安裝的包..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 列出要清理的包
PACKAGES_TO_REMOVE="openai numpy python-dotenv fastapi uvicorn pydantic starlette httpx httpcore anyio jiter sniffio tqdm typing-extensions annotated-types pydantic-core exceptiongroup h11 typing-inspection"

echo "將清理以下包："
echo "$PACKAGES_TO_REMOVE"
echo ""

# 卸載用戶目錄中的包
for pkg in $PACKAGES_TO_REMOVE; do
    pip3 uninstall -y $pkg 2>/dev/null
done

echo "✅ 用戶目錄清理完成"
echo ""

# 步驟 2: 檢查/創建虛擬環境
echo "📦 步驟 2: 檢查虛擬環境..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -d ".venv" ]; then
    echo "⚠️  虛擬環境不存在，正在創建..."
    python3 -m venv .venv
    echo "✅ 虛擬環境已創建"
else
    echo "✅ 虛擬環境已存在"
fi
echo ""

# 步驟 3: 在虛擬環境中安裝依賴
echo "📦 步驟 3: 在虛擬環境中安裝依賴..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 激活虛擬環境並安裝
source .venv/bin/activate

# 升級 pip
echo "升級 pip..."
pip install --upgrade pip

echo ""
echo "安裝專案依賴..."
pip install -U openai numpy python-dotenv fastapi uvicorn pydantic

# 檢查安裝結果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 所有依賴已成功安裝到虛擬環境！"
    echo ""
    echo "📋 虛擬環境中的套件版本："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    pip list | grep -E "openai|numpy|python-dotenv|fastapi|uvicorn|pydantic"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 虛擬環境位置: $VIRTUAL_ENV"
    echo ""
    echo "🎯 使用方法："
    echo ""
    echo "1. 激活虛擬環境:"
    echo "   source .venv/bin/activate"
    echo ""
    echo "2. 設定 API Key:"
    echo "   export OPENAI_API_KEY='your-api-key'"
    echo ""
    echo "3. 運行程序:"
    echo "   python main_parallel.py"
    echo "   或"
    echo "   python web_api.py"
    echo ""
    echo "4. 退出虛擬環境:"
    echo "   deactivate"
    
    # 退出虛擬環境
    deactivate
else
    echo ""
    echo "❌ 安裝失敗，請檢查錯誤信息"
    deactivate
    exit 1
fi

echo ""
echo "✅ 清理和重新安裝完成！"
