#!/bin/bash

echo "🔧 直接安裝依賴到系統 Python"
echo "=================================="
echo ""

# 使用系統的 pip3 直接安裝
echo "📥 安裝依賴..."
echo ""

pip3 install --user openai numpy python-dotenv fastapi uvicorn pydantic

echo ""
echo "✅ 安裝完成！"
echo ""
echo "現在可以運行測試："
echo "  python3 RUN_TEST.py"
