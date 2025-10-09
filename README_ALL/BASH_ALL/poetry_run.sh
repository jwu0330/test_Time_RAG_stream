#!/bin/bash
# Poetry 快速啟動腳本

# 添加 Poetry 到 PATH
export PATH="$HOME/.local/bin:$PATH"

# 檢查 Poetry 是否安裝
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry 未安裝"
    echo "請執行: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# 檢查依賴是否安裝
if [ ! -d ".venv" ]; then
    echo "📦 首次運行，正在安裝依賴..."
    poetry install
fi

# 檢查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件"
    echo "請複製 .env.example 並設置 OPENAI_API_KEY"
    echo "執行: cp .env.example .env"
    exit 1
fi

# 根據參數運行不同命令
case "$1" in
    "web")
        echo "🌐 啟動 Web API..."
        poetry run python web_api.py
        ;;
    "test")
        echo "🧪 運行測試..."
        poetry run python main_parallel.py
        ;;
    "shell")
        echo "🐚 進入 Poetry Shell..."
        poetry shell
        ;;
    "install")
        echo "📦 安裝/更新依賴..."
        poetry install
        ;;
    "update")
        echo "🔄 更新依賴..."
        poetry update
        ;;
    *)
        echo "使用方法:"
        echo "  ./run.sh web      - 啟動 Web API"
        echo "  ./run.sh test     - 運行主程序測試"
        echo "  ./run.sh shell    - 進入 Poetry Shell"
        echo "  ./run.sh install  - 安裝依賴"
        echo "  ./run.sh update   - 更新依賴"
        ;;
esac
