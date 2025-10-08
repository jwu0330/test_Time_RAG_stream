#!/bin/bash
# 清除歷史記錄

echo "🧹 清除歷史記錄..."
echo ""

# 激活虛擬環境
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi
fi

# 運行清除腳本
python3 clear_history.py

echo ""
echo "✅ 完成！"
