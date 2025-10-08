"""
測試 D4（重複詢問）判斷邏輯
驗證 AI 是否能正確判斷重複狀態
"""
import asyncio
from core.scenario_module import DimensionClassifier
from core.history_manager import HistoryManager


async def test_d4_repetition():
    """測試 D4 重複判斷邏輯"""
    
    print("="*60)
    print("🧪 測試 D4 重複詢問判斷邏輯")
    print("="*60)
    
    # 初始化分類器
    classifier = DimensionClassifier()
    
    # 清空歷史記錄
    classifier.history_manager.clear()
    print("\n✅ 已清空歷史記錄\n")
    
    # 測試案例 1: 連續詢問相同問題（應該判定為重複）
    print("\n" + "-"*60)
    print("📝 測試案例 1: 連續詢問相同問題")
    print("-"*60)
    
    test_queries_1 = [
        ("什麼是機器學習？", ["ml_basics.txt"]),
        ("機器學習是什麼？", ["ml_basics.txt"]),
        ("請解釋一下機器學習", ["ml_basics.txt"]),
        ("再說一次機器學習的定義", ["ml_basics.txt"])  # 第4次，應該判定為重複
    ]
    
    for i, (query, docs) in enumerate(test_queries_1, 1):
        print(f"\n第 {i} 次查詢: {query}")
        
        # 提取知識點
        knowledge_points = classifier._extract_knowledge_points(docs)
        print(f"知識點: {knowledge_points}")
        
        # 判斷 D4
        d4_result = await classifier._classify_d4(query, knowledge_points)
        print(f"D4 判斷結果: {d4_result}")
        
        # 記錄到歷史（模擬完整流程）
        dimensions = {
            "D1": "一個",
            "D2": "無錯誤",
            "D3": "粗略",
            "D4": d4_result
        }
        classifier.history_manager.add_query(query, docs, dimensions)
    
    # 測試案例 2: 相同知識點但不同角度（應該判定為正常）
    print("\n" + "="*60)
    print("📝 測試案例 2: 相同知識點但不同角度")
    print("="*60)
    
    # 清空歷史
    classifier.history_manager.clear()
    
    test_queries_2 = [
        ("什麼是機器學習？", ["ml_basics.txt"]),
        ("機器學習有哪些類型？", ["ml_basics.txt"]),
        ("監督式學習和非監督式學習的區別？", ["ml_basics.txt"]),
        ("機器學習在實際中如何應用？", ["ml_basics.txt"])  # 雖然都是機器學習，但角度不同
    ]
    
    for i, (query, docs) in enumerate(test_queries_2, 1):
        print(f"\n第 {i} 次查詢: {query}")
        
        knowledge_points = classifier._extract_knowledge_points(docs)
        print(f"知識點: {knowledge_points}")
        
        d4_result = await classifier._classify_d4(query, knowledge_points)
        print(f"D4 判斷結果: {d4_result}")
        
        dimensions = {
            "D1": "一個",
            "D2": "無錯誤",
            "D3": "粗略",
            "D4": d4_result
        }
        classifier.history_manager.add_query(query, docs, dimensions)
    
    # 測試案例 3: 在不同知識點之間切換（應該判定為正常）
    print("\n" + "="*60)
    print("📝 測試案例 3: 在不同知識點之間切換")
    print("="*60)
    
    # 清空歷史
    classifier.history_manager.clear()
    
    test_queries_3 = [
        ("什麼是機器學習？", ["ml_basics.txt"]),
        ("什麼是深度學習？", ["deep_learning.txt"]),
        ("什麼是自然語言處理？", ["nlp_intro.txt"]),
        ("機器學習和深度學習的關係？", ["ml_basics.txt", "deep_learning.txt"])
    ]
    
    for i, (query, docs) in enumerate(test_queries_3, 1):
        print(f"\n第 {i} 次查詢: {query}")
        
        knowledge_points = classifier._extract_knowledge_points(docs)
        print(f"知識點: {knowledge_points}")
        
        d4_result = await classifier._classify_d4(query, knowledge_points)
        print(f"D4 判斷結果: {d4_result}")
        
        dimensions = {
            "D1": "一個" if len(knowledge_points) == 1 else "多個",
            "D2": "無錯誤",
            "D3": "粗略",
            "D4": d4_result
        }
        classifier.history_manager.add_query(query, docs, dimensions)
    
    # 顯示最終歷史統計
    print("\n" + "="*60)
    print("📊 歷史記錄統計")
    print("="*60)
    classifier.history_manager.print_summary()
    
    print("\n✅ 測試完成！")


async def test_all_dimensions():
    """測試所有四個向度"""
    
    print("\n" + "="*60)
    print("🧪 測試完整四向度分類")
    print("="*60)
    
    classifier = DimensionClassifier()
    classifier.history_manager.clear()
    
    test_cases = [
        {
            "query": "什麼是機器學習？",
            "docs": ["ml_basics.txt"],
            "expected": {
                "D1": "一個",
                "D2": "無錯誤",
                "D3": "粗略",
                "D4": "正常狀態"
            }
        },
        {
            "query": "機器學習和深度學習有什麼不同？請詳細說明它們的應用場景、技術特點以及各自的優缺點。",
            "docs": ["ml_basics.txt", "deep_learning.txt"],
            "expected": {
                "D1": "多個",
                "D2": "無錯誤",
                "D3": "非常詳細",
                "D4": "正常狀態"
            }
        },
        {
            "query": "深度學習怎麼訓練",
            "docs": ["deep_learning.txt"],
            "expected": {
                "D1": "一個",
                "D2": "無錯誤",
                "D3": "粗略",
                "D4": "正常狀態"
            }
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"測試案例 {i}")
        print(f"{'='*60}")
        print(f"查詢: {case['query']}")
        print(f"匹配文件: {case['docs']}")
        
        # 執行分類
        dimensions = await classifier.classify(
            query=case['query'],
            matched_docs=case['docs']
        )
        
        print(f"\n實際結果:")
        for dim, value in dimensions.items():
            expected = case['expected'].get(dim, "?")
            match = "✅" if value == expected else "❌"
            print(f"  {dim}: {value} (預期: {expected}) {match}")
    
    print("\n✅ 完整測試完成！")


async def main():
    """主函數"""
    
    print("\n" + "="*60)
    print("🚀 D4 重複判斷邏輯測試套件")
    print("="*60)
    print("\n說明：")
    print("- D1: 通過 RAG 實際匹配判斷知識點數量")
    print("- D2: 由 AI 判斷表達是否有錯誤")
    print("- D3: 由 AI 判斷表達詳細程度")
    print("- D4: 由 AI 分析歷史記錄判斷是否重複")
    print("\n" + "="*60)
    
    # 測試 D4 邏輯
    await test_d4_repetition()
    
    # 測試完整四向度
    await test_all_dimensions()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  測試被中斷")
    except Exception as e:
        print(f"\n\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
