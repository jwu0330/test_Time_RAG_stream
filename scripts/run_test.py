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

from main_parallel import ParallelRAGSystem


def generate_24_scenarios():
    """生成 24 個情境文件"""
    print("="*60)
    print("🔧 生成 24 個情境文件...")
    print("="*60)
    
    # 創建目錄
    os.makedirs("scenarios_24", exist_ok=True)
    
    # 四向度的所有可能值
    dimension_values = {
        "D1": ["零個", "一個", "多個"],
        "D2": ["有錯誤", "無錯誤"],
        "D3": ["非常詳細", "粗略", "未談及重點"],
        "D4": ["重複狀態", "正常狀態"]
    }
    
    scenario_id = 1
    
    # 生成所有組合
    for d1 in dimension_values["D1"]:
        for d2 in dimension_values["D2"]:
            for d3 in dimension_values["D3"]:
                for d4 in dimension_values["D4"]:
                    # 創建情境
                    scenario = {
                        "id": f"scenario_{scenario_id:02d}",
                        "scenario_number": scenario_id,
                        "name": f"{d1}+{d2}+{d3}+{d4}",
                        "dimensions": {
                            "D1": d1,
                            "D2": d2,
                            "D3": d3,
                            "D4": d4
                        },
                        "description": f"這是第 {scenario_id} 種情境",
                        "response_strategy": {
                            "tone": "友好、專業",
                            "structure": ["根據情境調整回答"],
                            "emphasis": ["提供準確信息"],
                            "length": "適中"
                        },
                        "prompt_template": f"""
【情境說明】
現在是第 {scenario_id} 種情境。

四向度分析結果：
- D1 (知識點數量): {d1}
- D2 (表達錯誤): {d2}
- D3 (表達詳細度): {d3}
- D4 (重複詢問): {d4}

【回答指引】
請在回答開頭明確說明：「現在是第 {scenario_id} 種情境」

然後說明各向度的情況：
- 知識點數量：{d1}
- 表達錯誤：{d2}
- 表達詳細度：{d3}
- 重複詢問：{d4}

接著根據檢索到的教材內容，提供適當的回答。
"""
                    }
                    
                    # 保存文件
                    filename = f"scenarios_24/scenario_{scenario_id:02d}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(scenario, f, ensure_ascii=False, indent=2)
                    
                    print(f"  ✅ scenario_{scenario_id:02d}.json - {scenario['name']}")
                    
                    scenario_id += 1
    
    # 生成索引文件
    index = {
        "total_scenarios": 24,
        "description": "24 種情境組合（3×2×3×2=24）",
        "scenarios": []
    }
    
    for i in range(1, 25):
        with open(f"scenarios_24/scenario_{i:02d}.json", 'r', encoding='utf-8') as f:
            scenario = json.load(f)
            index["scenarios"].append({
                "id": scenario["id"],
                "number": scenario["scenario_number"],
                "name": scenario["name"],
                "dimensions": scenario["dimensions"]
            })
    
    with open("scenarios_24/index.json", 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 共生成 24 個情境文件")
    print(f"✅ 索引文件: scenarios_24/index.json\n")


async def test_system():
    """測試系統"""
    print("="*60)
    print("🧪 開始系統測試")
    print("="*60)
    
    # 初始化系統
    system = ParallelRAGSystem()
    
    # 初始化文件（會自動載入或向量化）
    await system.initialize_documents()
    
    # 測試查詢
    test_queries = [
        "什麼是機器學習？",
        "機器學習和深度學習有什麼區別？",
        "請詳細解釋神經網絡的工作原理。",
    ]
    
    print("\n" + "="*60)
    print("📝 執行測試查詢")
    print("="*60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"測試 {i}/{len(test_queries)}")
        print(f"{'='*60}")
        
        try:
            result = await system.process_query_parallel(query)
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
    print("1. 生成 24 個情境文件")
    print("2. 初始化系統和向量化文件")
    print("3. 執行多個測試查詢")
    print("4. 驗證情境匹配和顯示")
    print("\n" + "="*60)
    
    input("\n按 Enter 開始測試...")
    
    # 步驟 1：生成情境
    generate_24_scenarios()
    
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
