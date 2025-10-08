#!/bin/bash
# 整理 Web 文件到 web/ 資料夾

echo "🌐 開始整理 Web 文件..."
echo ""

cd /home/jim/code/python/test_Time_RAG_stream

# 確保 web 目錄存在
mkdir -p web

# 移動舊的 web 文件（如果存在）
if [ -f "web_interface.html" ]; then
    mv web_interface.html web/old_interface.html
    echo "✅ 已移動: web_interface.html → web/old_interface.html"
fi

if [ -f "web_interface_interactive.html" ]; then
    mv web_interface_interactive.html web/interactive.html
    echo "✅ 已移動: web_interface_interactive.html → web/interactive.html"
fi

# 同步指令文件移到 README_ALL
if [ -f "同步指令.txt" ]; then
    mv 同步指令.txt README_ALL/
    echo "✅ 已移動: 同步指令.txt → README_ALL/"
fi

echo ""
echo "✅ Web 文件整理完成！"
echo ""
echo "📁 當前 web/ 目錄結構："
ls -lh web/
echo ""
echo "🎯 使用方式："
echo "1. 啟動 API: python3 web_api.py"
echo "2. 打開界面: open web/index.html"
