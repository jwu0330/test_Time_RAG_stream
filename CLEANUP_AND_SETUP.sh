#!/bin/bash

echo "=================================="
echo "🧹 清理並創建獨立環境"
echo "=================================="
echo ""

# 步驟 1: 清理用戶安裝的包
echo "📦 步驟 1: 清理剛才安裝的包..."
echo ""
echo "移除以下包："
pip3 uninstall -y openai numpy python-dotenv fastapi uvicorn pydantic \
    typing-extensions tqdm sniffio jiter h11 annotated-types \
    pydantic-core httpcore exceptiongroup starlette httpx typing-inspection anyio

echo ""
echo "✅ 清理完成"
echo ""

# 步驟 2: 創建虛擬環境
echo "📦 步驟 2: 創建獨立的虛擬環境..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "✅ 虛擬環境創建成功"
else
    echo "❌ 虛擬環境創建失敗"
    exit 1
fi

echo ""

# 步驟 3: 激活虛擬環境
echo "📦 步驟 3: 激活虛擬環境..."
source venv/bin/activate

echo "✅ 虛擬環境已激活"
echo "   Python 路徑: $(which python)"
echo "   Python 版本: $(python --version)"
echo ""

# 步驟 4: 升級 pip
echo "📦 步驟 4: 升級 pip..."
pip install --upgrade pip

echo ""

# 步驟 5: 安裝依賴到虛擬環境
echo "📦 步驟 5: 安裝項目依賴到虛擬環境..."
pip install openai numpy python-dotenv fastapi uvicorn pydantic

echo ""
echo "=================================="
echo "✅ 環境設置完成！"
echo "=================================="
echo ""
echo "📋 重要說明："
echo ""
echo "1. 所有依賴已安裝到獨立的虛擬環境中"
echo "   位置: $(pwd)/venv/"
echo ""
echo "2. 不會影響系統或其他用戶的 Python 環境"
echo ""
echo "3. 使用方法："
echo "   - 激活環境: source venv/bin/activate"
echo "   - 運行程序: python RUN_TEST.py"
echo "   - 退出環境: deactivate"
echo ""
echo "4. 刪除環境（如果需要）："
echo "   rm -rf venv/"
echo ""
echo "=================================="
