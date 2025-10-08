#!/bin/bash

echo "🚀 快速啟動 RAG 系統"
echo "=================================="
echo ""

# 檢查環境
echo "📋 檢查環境..."
echo ""

# 檢查 Poetry
if command -v poetry &> /dev/null; then
    echo "✅ Poetry: $(poetry --version)"
    USE_POETRY=true
else
    echo "⚠️  Poetry: 未安裝"
    USE_POETRY=false
fi

# 檢查 Python
if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
else
    echo "❌ Python: 未安裝"
    echo ""
    echo "請先安裝 Python 3.8+"
    exit 1
fi

echo ""
echo "=================================="
echo ""

# 根據環境選擇安裝方式
if [ "$USE_POETRY" = true ]; then
    echo "📦 使用 Poetry 管理依賴"
    echo ""
    
    # 檢查是否已安裝依賴
    if poetry run python -c "import openai" 2>/dev/null; then
        echo "✅ 依賴已安裝"
    else
        echo "📥 安裝依賴..."
        poetry install
    fi
    
    echo ""
    echo "🧪 運行測試..."
    echo ""
    poetry run python RUN_TEST.py
    
else
    echo "📦 使用 venv + pip 管理依賴"
    echo ""
    
    # 檢查虛擬環境
    if [ ! -d "venv" ]; then
        echo "📥 創建虛擬環境..."
        python3 -m venv venv
    fi
    
    # 激活虛擬環境
    source venv/bin/activate
    
    # 檢查是否已安裝依賴
    if python -c "import openai" 2>/dev/null; then
        echo "✅ 依賴已安裝"
    else
        echo "📥 安裝依賴..."
        pip install --upgrade pip
        pip install -r requirements.txt
    fi
    
    echo ""
    echo "🧪 運行測試..."
    echo ""
    python RUN_TEST.py
fi
