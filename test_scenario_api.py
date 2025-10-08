#!/usr/bin/env python3
"""
測試情境判定 API 呼叫
"""
import asyncio
from core.scenario_classifier import ScenarioClassifier


async def test_scenario_classification():
    """測試情境分類器的 API 呼叫"""
    print("\n" + "="*70)
    print("🧪 測試情境判定 API 呼叫")
    print("="*70 + "\n")
    
    # 初始化分類器
    classifier = ScenarioClassifier()
    
    # 測試問題
    test_queries = [
        "什麼是機器學習？",
        "深度學習和機器學習有什麼區別？",
        "ML",  # 粗略的問題
        "請詳細解釋一下自然語言處理的工作原理，包括詞嵌入、注意力機制等技術細節",  # 非常詳細
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"測試 {i}: {query}")
        print('='*70)
        
        try:
            # 呼叫分類器（會呼叫 OpenAI API）
            result = classifier.classify(query, history=None)
            
            print(f"\n✅ 判定成功！")
            print(f"情境編號: {result['scenario_number']}")
            print(f"情境描述: {result['description']}")
            print(f"\n四向度:")
            for dim, value in result['dimensions'].items():
                print(f"  {dim}: {value}")
            print(f"\n顯示文字: {result['display_text']}")
            
        except Exception as e:
            print(f"\n❌ 測試失敗: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("測試完成")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(test_scenario_classification())
