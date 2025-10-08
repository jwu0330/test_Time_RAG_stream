"""
系統測試腳本
用於驗證各模組功能
"""
import asyncio
import os
import sys
from typing import List, Dict


async def test_imports():
    """測試模組導入"""
    print("🧪 測試 1: 模組導入")
    print("-" * 50)
    
    try:
        from core.vector_store import VectorStore, cosine_similarity
        from core.rag_module import RAGRetriever, RAGCache
        from core.scenario_module import DimensionClassifier, ScenarioInjector
        from core.timer_utils import Timer, TimerRecord, TimerReport
        from main_parallel import ParallelRAGSystem
        
        print("✅ 所有模組導入成功")
        return True
    except Exception as e:
        print(f"❌ 模組導入失敗: {e}")
        return False


async def test_timer():
    """測試計時器功能"""
    print("\n🧪 測試 2: 計時器功能")
    print("-" * 50)
    
    try:
        from core.timer_utils import Timer
        
        timer = Timer()
        
        # 測試階段計時
        timer.start_stage("測試階段1")
        await asyncio.sleep(0.1)
        duration1 = timer.stop_stage("測試階段1")
        
        timer.start_stage("測試階段2")
        await asyncio.sleep(0.05)
        duration2 = timer.stop_stage("測試階段2")
        
        # 生成報告
        report = timer.get_report()
        
        assert duration1 > 0.09, "階段1計時不準確"
        assert duration2 > 0.04, "階段2計時不準確"
        assert report.total_time > 0.14, "總計時不準確"
        
        print(f"  階段1耗時: {duration1:.3f}s")
        print(f"  階段2耗時: {duration2:.3f}s")
        print(f"  總耗時: {report.total_time:.3f}s")
        print("✅ 計時器測試通過")
        return True
    except Exception as e:
        print(f"❌ 計時器測試失敗: {e}")
        return False


async def test_vector_store():
    """測試向量儲存功能"""
    print("\n🧪 測試 3: 向量儲存功能")
    print("-" * 50)
    
    # 檢查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  跳過：未設定 OPENAI_API_KEY")
        return None
    
    try:
        from vector_store import VectorStore, cosine_similarity
        
        # 創建測試向量儲存
        store = VectorStore(storage_path="test_vectors.pkl")
        
        # 添加測試文件
        await store.add_document(
            doc_id="test_doc1",
            content="這是一個關於機器學習的測試文件",
            metadata={"category": "test"}
        )
        
        await store.add_document(
            doc_id="test_doc2",
            content="這是一個關於深度學習的測試文件",
            metadata={"category": "test"}
        )
        
        # 測試儲存
        store.save()
        
        # 測試載入
        new_store = VectorStore(storage_path="test_vectors.pkl")
        loaded = new_store.load()
        
        assert loaded, "向量載入失敗"
        assert len(new_store.get_all_documents()) == 2, "文件數量不正確"
        
        # 測試相似度計算
        doc1 = new_store.get_document("test_doc1")
        doc2 = new_store.get_document("test_doc2")
        
        similarity = cosine_similarity(doc1["embedding"], doc2["embedding"])
        
        print(f"  已添加文件數: 2")
        print(f"  相似度: {similarity:.3f}")
        print("✅ 向量儲存測試通過")
        
        # 清理測試文件
        if os.path.exists("test_vectors.pkl"):
            os.remove("test_vectors.pkl")
        
        return True
    except Exception as e:
        print(f"❌ 向量儲存測試失敗: {e}")
        # 清理測試文件
        if os.path.exists("test_vectors.pkl"):
            os.remove("test_vectors.pkl")
        return False


async def test_rag_cache():
    """測試 RAG 快取功能"""
    print("\n🧪 測試 4: RAG 快取功能")
    print("-" * 50)
    
    try:
        from core.rag_module import RAGCache
        
        cache = RAGCache(max_size=10)
        
        # 測試快取存取
        test_query = "測試查詢"
        test_results = [{"doc_id": "doc1", "score": 0.9}]
        
        # 第一次應該 miss
        result = cache.get(test_query)
        assert result is None, "快取應該為空"
        
        # 放入快取
        cache.put(test_query, test_results)
        
        # 第二次應該 hit
        result = cache.get(test_query)
        assert result is not None, "快取應該有值"
        assert result[0]["doc_id"] == "doc1", "快取內容不正確"
        
        # 檢查統計
        stats = cache.get_stats()
        assert stats["hits"] == 1, "命中次數不正確"
        assert stats["misses"] == 1, "未命中次數不正確"
        
        print(f"  快取命中率: {stats['hit_rate']:.1%}")
        print(f"  快取大小: {stats['cache_size']}")
        print("✅ RAG 快取測試通過")
        return True
    except Exception as e:
        print(f"❌ RAG 快取測試失敗: {e}")
        return False


async def test_scenario_loading():
    """測試情境載入功能"""
    print("\n🧪 測試 5: 情境載入功能")
    print("-" * 50)
    
    # 檢查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  跳過：未設定 OPENAI_API_KEY")
        return None
    
    try:
        from core.scenario_module import DimensionClassifier
        
        classifier = ScenarioClassifier()
        
        # 載入情境
        classifier.load_scenarios_from_dir("scenarios")
        
        scenario_count = len(classifier.scenarios)
        
        print(f"  已載入情境數: {scenario_count}")
        
        if scenario_count > 0:
            print(f"  情境列表: {', '.join(classifier.scenarios.keys())}")
            
            # 測試獲取情境內容
            first_scenario = list(classifier.scenarios.keys())[0]
            content = classifier.get_scenario_content(first_scenario)
            
            assert len(content) > 0, "情境內容為空"
            print(f"  測試情境 '{first_scenario}' 內容長度: {len(content)} 字符")
        
        print("✅ 情境載入測試通過")
        return True
    except Exception as e:
        print(f"❌ 情境載入測試失敗: {e}")
        return False


async def test_file_structure():
    """測試文件結構"""
    print("\n🧪 測試 6: 文件結構檢查")
    print("-" * 50)
    
    required_files = [
        "main.py",
        "vector_store.py",
        "rag_module.py",
        "scenario_module.py",
        "timer_utils.py",
        "requirements.txt",
        "JIM_README.md"
    ]
    
    required_dirs = [
        "docs",
        "scenarios"
    ]
    
    all_ok = True
    
    # 檢查文件
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (缺失)")
            all_ok = False
    
    # 檢查目錄
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            file_count = len(os.listdir(dir_name))
            print(f"  ✅ {dir_name}/ ({file_count} 個文件)")
        else:
            print(f"  ❌ {dir_name}/ (缺失)")
            all_ok = False
    
    if all_ok:
        print("✅ 文件結構檢查通過")
    else:
        print("⚠️  部分文件或目錄缺失")
    
    return all_ok


async def run_all_tests():
    """執行所有測試"""
    print("="*60)
    print("🚀 RAG 系統測試套件")
    print("="*60)
    
    results = {}
    
    # 執行測試
    results["imports"] = await test_imports()
    results["timer"] = await test_timer()
    results["file_structure"] = await test_file_structure()
    results["rag_cache"] = await test_rag_cache()
    results["vector_store"] = await test_vector_store()
    results["scenario_loading"] = await test_scenario_loading()
    
    # 統計結果
    print("\n" + "="*60)
    print("📊 測試結果摘要")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ 通過" if result is True else "❌ 失敗" if result is False else "⚠️  跳過"
        print(f"  {test_name:20s}: {status}")
    
    print("-"*60)
    print(f"  總計: {total} | 通過: {passed} | 失敗: {failed} | 跳過: {skipped}")
    print("="*60)
    
    if failed > 0:
        print("\n⚠️  部分測試失敗，請檢查錯誤信息")
        return False
    elif skipped > 0:
        print("\n⚠️  部分測試被跳過（可能需要設定 OPENAI_API_KEY）")
        return True
    else:
        print("\n✅ 所有測試通過！系統已就緒。")
        return True


async def main():
    """主函數"""
    try:
        success = await run_all_tests()
        
        if success:
            print("\n💡 下一步:")
            print("  1. 設定 OPENAI_API_KEY (如果尚未設定)")
            print("  2. 執行 python quick_start.py 進行快速測試")
            print("  3. 執行 python main.py 進行完整測試")
            print("  4. 查看 JIM_README.md 獲取詳細文檔")
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  測試被中斷")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
