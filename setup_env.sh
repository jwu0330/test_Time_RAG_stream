#!/bin/bash

echo "=================================="
echo "🔧 環境設置腳本"
echo "=================================="

# 檢查 Poetry
if command -v poetry &> /dev/null; then
    echo "✅ 檢測到 Poetry"
    echo ""
    echo "使用 Poetry 安裝依賴..."
    
    # 安裝依賴
    poetry install
    
    echo ""
    echo "✅ 依賴安裝完成！"
    echo ""
    echo "運行測試："
    echo "  poetry run python RUN_TEST.py"
    echo ""
    echo "或進入 Poetry shell："
    echo "  poetry shell"
    echo "  python RUN_TEST.py"
    
else
    echo "⚠️  未檢測到 Poetry"
    echo ""
    echo "使用 venv + pip 安裝..."
    
    # 檢查 Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ 錯誤：未找到 python3"
        echo "請先安裝 Python 3.8+"
        exit 1
    fi
    
    # 創建虛擬環境
    if [ ! -d "venv" ]; then
        echo "創建虛擬環境..."
        python3 -m venv venv
    fi
    
    # 激活虛擬環境
    echo "激活虛擬環境..."
    source venv/bin/activate
    
    # 升級 pip
    echo "升級 pip..."
    pip install --upgrade pip
    
    # 安裝依賴
    echo "安裝依賴..."
    pip install -r requirements.txt
    
    echo ""
    echo "✅ 依賴安裝完成！"
    echo ""
    echo "運行測試："
    echo "  source venv/bin/activate"
    echo "  python RUN_TEST.py"
fi

echo ""
echo "=================================="
echo "🎉 環境設置完成！"
echo "=================================="
