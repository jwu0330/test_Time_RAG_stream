#!/bin/bash
# 快速安裝依賴腳本

echo "🚀 開始安裝 Python 依賴..."
echo ""

# 檢查 pip3 是否存在
if ! command -v pip3 &> /dev/null
then
    echo "⚠️  pip3 未安裝，正在安裝..."
    sudo apt update
    sudo apt install -y python3-pip
    echo "✅ pip3 安裝完成"
    echo ""
fi

# 安裝依賴
echo "📦 安裝專案依賴..."
pip3 install --user -r requirements.txt

# 檢查安裝結果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 所有依賴安裝成功！"
    echo ""
    echo "📋 已安裝的套件："
    pip3 list | grep -E "openai|numpy|fastapi|uvicorn|pydantic|python-dotenv"
    echo ""
    echo "🎯 下一步："
    echo "1. 設定 API Key: export OPENAI_API_KEY='your-key'"
    echo "2. 運行測試: python3 scripts/run_test.py"
    echo "3. 或啟動 Web: python3 web_api.py"
else
    echo ""
    echo "❌ 安裝失敗，請檢查錯誤信息"
    echo ""
    echo "💡 手動安裝："
    echo "pip3 install --user openai numpy python-dotenv fastapi uvicorn pydantic"
fi
