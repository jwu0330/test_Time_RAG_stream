"""
快速啟動腳本 - 用於快速測試系統
"""
import asyncio
import os
from main import RAGStreamSystem


async def quick_start():
    """快速啟動並測試系統"""
    
    print("🚀 RAG 流式中斷與續寫系統 - 快速啟動")
    print("="*60)
    
    # 檢查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  警告：未設定 OPENAI_API_KEY")
        print("請執行以下命令設定 API Key：")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("\n或創建 .env 文件：")
        print("  echo 'OPENAI_API_KEY=your-api-key-here' > .env")
        print("  pip install python-dotenv")
        return
    
    # 初始化系統
    print("\n📦 初始化系統...")
    system = RAGStreamSystem()
    
    # 初始化文件和情境
    print("\n📚 初始化文件向量...")
    await system.initialize_documents("docs")
    
    print("\n🎭 載入情境...")
    await system.load_scenarios("scenarios")
    
    # 單個測試查詢
    print("\n" + "="*60)
    print("🧪 執行測試查詢")
    print("="*60)
    
    test_query = "什麼是機器學習？請給我一個初學者友好的解釋。"
    
    print(f"\n❓ 查詢: {test_query}")
    
    result = await system.process_query(test_query)
    
    # 顯示結果
    print("\n" + "="*60)
    print("📊 測試結果")
    print("="*60)
    
    system.print_summary(result)
    system.save_result(result)
    
    print("\n✅ 快速測試完成！")
    print("\n💡 提示：")
    print("  - 查看 results/ 目錄獲取詳細結果")
    print("  - 修改 docs/ 目錄中的文件來自定義知識庫")
    print("  - 修改 scenarios/ 目錄中的情境來調整回答風格")
    print("  - 執行 python main.py 進行完整測試")


if __name__ == "__main__":
    try:
        asyncio.run(quick_start())
    except KeyboardInterrupt:
        print("\n\n⚠️  用戶中斷執行")
    except Exception as e:
        print(f"\n\n❌ 錯誤: {e}")
        print("\n請檢查：")
        print("  1. OPENAI_API_KEY 是否正確設定")
        print("  2. 網絡連接是否正常")
        print("  3. docs/ 和 scenarios/ 目錄是否存在")
