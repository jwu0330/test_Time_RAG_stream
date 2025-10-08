#!/bin/bash

echo "=================================="
echo "🧹 創建乾淨的 Python 環境"
echo "=================================="
echo ""

# 1. 創建虛擬環境
echo "📦 步驟 1: 創建虛擬環境..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "✅ 虛擬環境創建成功"
else
    echo "❌ 虛擬環境創建失敗"
    exit 1
fi

echo ""

# 2. 激活虛擬環境
echo "📦 步驟 2: 激活虛擬環境..."
source venv/bin/activate

echo "✅ 虛擬環境已激活"
echo "   Python 路徑: $(which python)"
echo "   Python 版本: $(python --version)"
echo ""

# 3. 升級 pip
echo "📦 步驟 3: 升級 pip..."
pip install --upgrade pip

echo ""

# 4. 安裝依賴
echo "📦 步驟 4: 安裝項目依賴..."
pip install openai numpy python-dotenv fastapi uvicorn pydantic

echo ""
echo "=================================="
echo "✅ 環境設置完成！"
echo "=================================="
echo ""
echo "下次使用時，請先激活環境："
echo "  source venv/bin/activate"
echo ""
echo "然後運行測試："
echo "  python RUN_TEST.py"
echo ""
echo "退出虛擬環境："
echo "  deactivate"
echo ""
echo "=================================="
