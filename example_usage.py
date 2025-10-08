"""
使用範例 - 展示各種使用場景
"""
import asyncio
import os
from main import RAGStreamSystem


async def example_1_basic_usage():
    """範例 1: 基本使用"""
    print("\n" + "="*60)
    print("📘 範例 1: 基本使用")
    print("="*60)
    
    # 初始化系統
    system = RAGStreamSystem()
    
    # 初始化文件和情境
    await system.initialize_documents("docs")
    await system.load_scenarios("scenarios")
    
    # 處理查詢
    result = await system.process_query("什麼是機器學習？")
    
    # 顯示結果
    system.print_summary(result)


async def example_2_custom_scenarios():
    """範例 2: 指定特定情境"""
    print("\n" + "="*60)
    print("📘 範例 2: 指定特定情境")
    print("="*60)
    
    system = RAGStreamSystem()
    await system.initialize_documents("docs")
    await system.load_scenarios("scenarios")
    
    # 使用學術情境
    result = await system.process_query(
        query="深度學習中的反向傳播算法是如何工作的？",
        scenario_ids=["academic"],
        auto_classify=False
    )
    
    print(f"\n使用情境: {result['scenario_used']}")
    print(f"匹配文件: {', '.join(result['matched_docs'])}")


async def example_3_multiple_queries():
    """範例 3: 批量處理多個查詢"""
    print("\n" + "="*60)
    print("📘 範例 3: 批量處理多個查詢")
    print("="*60)
    
    system = RAGStreamSystem()
    await system.initialize_documents("docs")
    await system.load_scenarios("scenarios")
    
    queries = [
        "什麼是監督式學習？",
        "如何優化神經網絡？",
        "BERT 模型的原理是什麼？"
    ]
    
    results = []
    for i, query in enumerate(queries, 1):
        print(f"\n處理查詢 {i}/{len(queries)}: {query}")
        result = await system.process_query(query)
        results.append(result)
        
        # 簡短摘要
        print(f"  耗時: {result['time_report']['total_time']}s")
        print(f"  情境: {result['scenario_used']}")
    
    # 平均時間分析
    avg_time = sum(r['time_report']['total_time'] for r in results) / len(results)
    print(f"\n平均處理時間: {avg_time:.3f}s")


async def example_4_cache_demonstration():
    """範例 4: 快取效果展示"""
    print("\n" + "="*60)
    print("📘 範例 4: 快取效果展示")
    print("="*60)
    
    system = RAGStreamSystem()
    await system.initialize_documents("docs")
    await system.load_scenarios("scenarios")
    
    query = "什麼是深度學習？"
    
    # 第一次查詢（無快取）
    print("\n第一次查詢（無快取）:")
    result1 = await system.process_query(query)
    time1 = result1['time_report']['total_time']
    print(f"  耗時: {time1:.3f}s")
    
    # 第二次相同查詢（有快取）
    print("\n第二次查詢（使用快取）:")
    result2 = await system.process_query(query)
    time2 = result2['time_report']['total_time']
    print(f"  耗時: {time2:.3f}s")
    
    # 比較
    speedup = (time1 - time2) / time1 * 100 if time1 > time2 else 0
    print(f"\n快取加速: {speedup:.1f}%")


async def example_5_custom_retrieval():
    """範例 5: 自定義檢索參數"""
    print("\n" + "="*60)
    print("📘 範例 5: 自定義檢索參數")
    print("="*60)
    
    system = RAGStreamSystem()
    await system.initialize_documents("docs")
    
    query = "神經網絡訓練技巧"
    
    # 使用不同的 top_k 值
    print("\n檢索 Top-1 文件:")
    results_1 = await system.rag_retriever.retrieve(query, top_k=1)
    for doc in results_1:
        print(f"  {doc['doc_id']}: {doc['score']:.3f}")
    
    print("\n檢索 Top-3 文件:")
    results_3 = await system.rag_retriever.retrieve(query, top_k=3)
    for doc in results_3:
        print(f"  {doc['doc_id']}: {doc['score']:.3f}")
    
    # 使用相似度閾值
    print("\n使用相似度閾值 0.7:")
    results_threshold = await system.rag_retriever.retrieve_with_threshold(
        query, threshold=0.7, top_k=5
    )
    print(f"  找到 {len(results_threshold)} 個符合條件的文件")


async def example_6_scenario_classification():
    """範例 6: 情境分類詳解"""
    print("\n" + "="*60)
    print("📘 範例 6: 情境分類詳解")
    print("="*60)
    
    system = RAGStreamSystem()
    await system.initialize_documents("docs")
    await system.load_scenarios("scenarios")
    
    queries = [
        "什麼是機器學習？（初學者）",
        "如何在生產環境部署深度學習模型？",
        "深度學習中的注意力機制的數學原理"
    ]
    
    for query in queries:
        print(f"\n查詢: {query}")
        
        # 獲取 RAG 上下文
        retrieved = await system.rag_retriever.retrieve(query, top_k=2)
        context = system.rag_retriever.format_context(retrieved)
        
        # 進行情境分類
        classification = await system.scenario_classifier.classify_scenario(
            query=query,
            context=context
        )
        
        print("  四向度評分:")
        for dim in ["D1", "D2", "D3", "D4"]:
            if dim in classification:
                score = classification[dim].get("score", 0)
                reason = classification[dim].get("reason", "")
                print(f"    {dim}: {score}/5 - {reason}")


async def example_7_time_analysis():
    """範例 7: 詳細時間分析"""
    print("\n" + "="*60)
    print("📘 範例 7: 詳細時間分析")
    print("="*60)
    
    system = RAGStreamSystem()
    await system.initialize_documents("docs")
    await system.load_scenarios("scenarios")
    
    # 執行多次測試
    num_tests = 3
    all_results = []
    
    for i in range(num_tests):
        print(f"\n執行測試 {i+1}/{num_tests}...")
        result = await system.process_query("什麼是自然語言處理？")
        all_results.append(result)
    
    # 分析各階段平均時間
    print("\n" + "="*60)
    print("⏱️  各階段平均時間分析")
    print("="*60)
    
    stage_times = {}
    for result in all_results:
        for stage, duration in result['time_report']['stages'].items():
            if stage not in stage_times:
                stage_times[stage] = []
            stage_times[stage].append(duration)
    
    for stage, times in stage_times.items():
        avg = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        print(f"{stage:25s}: 平均 {avg:.3f}s (範圍: {min_time:.3f}s - {max_time:.3f}s)")
    
    # 總時間
    total_times = [r['time_report']['total_time'] for r in all_results]
    avg_total = sum(total_times) / len(total_times)
    print(f"{'總計':25s}: 平均 {avg_total:.3f}s")


async def example_8_error_handling():
    """範例 8: 錯誤處理"""
    print("\n" + "="*60)
    print("📘 範例 8: 錯誤處理")
    print("="*60)
    
    try:
        system = RAGStreamSystem()
        
        # 嘗試載入不存在的目錄
        print("\n測試: 載入不存在的文件目錄")
        await system.initialize_documents("non_existent_docs")
        
        # 嘗試載入不存在的情境目錄
        print("\n測試: 載入不存在的情境目錄")
        await system.load_scenarios("non_existent_scenarios")
        
        print("\n✅ 錯誤處理正常，系統繼續運行")
        
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")


async def example_9_save_and_load():
    """範例 9: 向量儲存與載入"""
    print("\n" + "="*60)
    print("📘 範例 9: 向量儲存與載入")
    print("="*60)
    
    system = RAGStreamSystem()
    
    # 第一次：向量化並儲存
    print("\n第一次執行：向量化文件...")
    await system.initialize_documents("docs")
    
    # 第二次：載入已儲存的向量
    print("\n第二次執行：載入已儲存的向量...")
    system2 = RAGStreamSystem()
    await system2.initialize_documents("docs")
    
    print("\n✅ 向量儲存與載入測試完成")
    print("   提示: 第二次執行應該更快，因為直接載入了已儲存的向量")


async def example_10_background_tasks():
    """範例 10: 背景任務執行"""
    print("\n" + "="*60)
    print("📘 範例 10: 背景任務執行")
    print("="*60)
    
    system = RAGStreamSystem()
    await system.initialize_documents("docs")
    await system.load_scenarios("scenarios")
    
    print("\n處理查詢並執行背景任務...")
    result = await system.process_query("什麼是強化學習？")
    
    # 背景任務時間
    bg_time = result['time_report']['stages'].get('背景任務', 0)
    total_time = result['time_report']['total_time']
    
    print(f"\n背景任務耗時: {bg_time:.3f}s")
    print(f"總耗時: {total_time:.3f}s")
    print(f"背景任務佔比: {bg_time/total_time*100:.1f}%")


async def run_all_examples():
    """執行所有範例"""
    
    # 檢查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  警告：未設定 OPENAI_API_KEY")
        print("請設定 API Key 後再執行範例")
        return
    
    print("="*60)
    print("🎓 RAG 系統使用範例集")
    print("="*60)
    
    examples = [
        ("基本使用", example_1_basic_usage),
        ("指定特定情境", example_2_custom_scenarios),
        ("批量處理", example_3_multiple_queries),
        ("快取效果", example_4_cache_demonstration),
        ("自定義檢索", example_5_custom_retrieval),
        ("情境分類", example_6_scenario_classification),
        ("時間分析", example_7_time_analysis),
        ("錯誤處理", example_8_error_handling),
        ("儲存與載入", example_9_save_and_load),
        ("背景任務", example_10_background_tasks),
    ]
    
    print("\n可用範例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\n選擇要執行的範例 (輸入數字，或 'all' 執行全部，'q' 退出):")
    choice = input("> ").strip()
    
    if choice.lower() == 'q':
        return
    elif choice.lower() == 'all':
        for name, func in examples:
            try:
                await func()
                await asyncio.sleep(1)
            except Exception as e:
                print(f"\n❌ 範例 '{name}' 執行失敗: {e}")
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                name, func = examples[idx]
                await func()
            else:
                print("❌ 無效的選擇")
        except ValueError:
            print("❌ 請輸入有效的數字")


async def main():
    """主函數"""
    try:
        await run_all_examples()
        print("\n✅ 範例執行完成！")
    except KeyboardInterrupt:
        print("\n\n⚠️  用戶中斷執行")
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")


if __name__ == "__main__":
    asyncio.run(main())
