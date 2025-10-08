#!/bin/bash

echo "🚀 激活環境並運行測試"
echo "=================================="
echo ""

# 檢查虛擬環境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虛擬環境不存在"
    echo ""
    echo "請先運行："
    echo "  chmod +x SETUP_CLEAN_ENV.sh"
    echo "  ./SETUP_CLEAN_ENV.sh"
    exit 1
fi

# 激活虛擬環境
echo "📦 激活虛擬環境..."
source venv/bin/activate

echo "✅ 環境已激活"
echo "   Python: $(which python)"
echo ""

# 運行測試
echo "🧪 運行測試..."
echo ""
python RUN_TEST.py
