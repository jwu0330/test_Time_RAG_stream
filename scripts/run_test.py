"""
完整系統測試腳本
包含情境生成和系統測試
"""
import asyncio
import json
import os
import sys

# 添加父目錄到路徑，以便導入 main_parallel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_parallel import ResponsesRAGSystem


def generate_12_scenarios():
    """生成 12 個情境文件 (K/C/R 三維度)"""
    print("="*60)
    print("🔧 生成 12 個情境文件 (K/C/R 三維度)...")
    print("="*60)
    
    # 創建目錄
    os.makedirs("data/scenarios", exist_ok=True)
    
    # 三維度的所有可能值
    dimension_values = {
        "K": ["零個", "一個", "多個"],
        "C": ["正確", "不正確"],
        "R": ["正常", "重複"]
    }
    
    scenario_id = 1
    scenarios_list = []
    
    # 生成所有組合 (3 * 2 * 2 = 12)
    for k in dimension_values["K"]:
        for c in dimension_values["C"]:
            for r in dimension_values["R"]:
                # 創建情境
                scenario = {
                    "scenario_number": scenario_id,
                    "label": f"{k}知識點 & {c} & {r}",
                    "role": "根據情境調整",
                    "prompt": f"你是專業知識助手。當前情境：{k}知識點 & {c} & {r}。請根據教材內容提供適當的回答。"
                }
                
                scenarios_list.append(scenario)
                print(f"  ✅ 情境 {scenario_id:2d}: {scenario['label']}")
                scenario_id += 1
    
    # 生成索引文件
    index = {
        "total_scenarios": 12,
        "version": "3.0",
        "last_updated": "2025-10-15",
        "description": "簡化版情境系統 - 移除詳細度維度，保留 K (知識點數量)、C (正確性)、R (重複性)",
        "scenarios": scenarios_list
    }
    
    with open("data/scenarios/scenarios_12.json", 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 共生成 12 個情境")
    print(f"✅ 檔案: data/scenarios/scenarios_12.json\n")


async def test_system():
    """測試系統"""
    print("="*60)
    print("🧪 開始系統測試")
    print("="*60)
    
    # 初始化系統
    system = ResponsesRAGSystem()
    
    # 初始化文件（會自動載入或向量化）
    await system.initialize_documents()
    
    # 測試查詢
    test_queries = [
        "什麼是 IPv4？",
        "IPv4 和 IPv6 有什麼區別？",
        "請詳細解釋 DNS 解析的工作原理。",
    ]
    
    print("\n" + "="*60)
    print("📝 執行測試查詢")
    print("="*60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"測試 {i}/{len(test_queries)}")
        print(f"{'='*60}")
        
        try:
            result = await system.process_query(query)
            system.print_summary(result)
            
            # 驗證情境信息是否正確顯示
            print(f"\n✅ 測試 {i} 完成")
            print(f"   情境編號: {result['scenario_number']}")
            print(f"   情境名稱: {result['scenario_name']}")
            
        except Exception as e:
            print(f"\n❌ 測試 {i} 失敗: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("✅ 系統測試完成！")
    print("="*60)


async def main():
    """主函數"""
    print("\n" + "="*60)
    print("🚀 RAG 系統完整測試")
    print("="*60)
    print("\n這個測試會：")
    print("1. 生成 12 個情境文件 (K/C/R 三維度)")
    print("2. 初始化系統和向量化文件")
    print("3. 執行多個測試查詢")
    print("4. 驗證情境匹配和顯示")
    print("\n" + "="*60)
    
    input("\n按 Enter 開始測試...")
    
    # 步驟 1：生成情境
    generate_12_scenarios()
    
    # 步驟 2：測試系統
    await test_system()
    
    print("\n" + "="*60)
    print("🎉 所有測試完成！")
    print("="*60)
    print("\n系統已就緒，可以正常使用。")
    print("\n下一步：")
    print("1. 擴展 docs/ 中的教材到 5000 字")
    print("2. 根據需求調整情境文件")
    print("3. 使用 python main_parallel.py 運行系統")
    print("4. 或使用 python web_api.py 啟動 Web 界面")
    print("="*60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  測試被中斷")
    except Exception as e:
        print(f"\n\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
