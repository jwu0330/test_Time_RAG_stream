#!/usr/bin/env python3
"""
測試優化後的知識點檢測和 C 值檢測
"""
import asyncio
import time
from core.tools.knowledge_detector import KnowledgeDetector
from core.tools.correctness_detector import CorrectnessDetector
from config import Config

async def test_knowledge_detection():
    """測試知識點檢測優化"""
    print("\n" + "="*70)
    print("🧪 測試知識點檢測優化")
    print("="*70)
    
    detector = KnowledgeDetector()
    
    test_cases = [
        ("什麼是 IPv4 和 IPv6？", ["IPv4", "IPv6"]),
        ("DNS 如何解析網域名稱？", ["DNS"]),
        ("NAT 和 PAT 有什麼不同？", ["NAT", "PAT / NAPT"]),
        ("子網遮罩的作用是什麼？", ["子網遮罩"]),
        ("IP 位址有哪些版本？", ["IPv4", "IPv6", "IP 位址"]),
    ]
    
    results = []
    for query, expected in test_cases:
        print(f"\n{'─'*70}")
        print(f"📝 測試查詢: {query}")
        print(f"🎯 預期知識點: {expected}")
        
        t_start = time.perf_counter()
        detected = await detector.detect(query)
        t_end = time.perf_counter()
        
        duration = t_end - t_start
        success = len(detected) > 0
        
        print(f"✅ 檢測結果: {detected}")
        print(f"⏱️  耗時: {duration:.3f} 秒")
        print(f"📊 狀態: {'成功' if success else '失敗'}")
        
        results.append({
            "query": query,
            "expected": expected,
            "detected": detected,
            "duration": duration,
            "success": success
        })
    
    # 總結
    print(f"\n{'='*70}")
    print(f"📊 知識點檢測測試總結")
    print(f"{'='*70}")
    
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    avg_duration = sum(r["duration"] for r in results) / total
    
    print(f"  總測試數: {total}")
    print(f"  成功數: {successful}")
    print(f"  成功率: {successful/total*100:.1f}%")
    print(f"  平均耗時: {avg_duration:.3f} 秒")
    print(f"{'='*70}")
    
    return results

async def test_correctness_detection():
    """測試 C 值檢測優化"""
    print("\n" + "="*70)
    print("🧪 測試 C 值檢測優化")
    print("="*70)
    
    detector = CorrectnessDetector()
    
    test_cases = [
        ("什麼是 IPv4？", 0, "正常問題"),
        ("IPv4 比 IPv6 更先進", 1, "事實錯誤"),
        ("DNS 如何工作？", 0, "正常問題"),
        ("NAT 可以增加 IP 位址數量", 0, "正常陳述"),
        ("今天天氣如何？", 0, "正常問題"),
    ]
    
    results = []
    for query, expected, description in test_cases:
        print(f"\n{'─'*70}")
        print(f"📝 測試查詢: {query}")
        print(f"🎯 預期結果: {expected} ({['正確', '不正確'][expected]})")
        print(f"📌 描述: {description}")
        
        t_start = time.perf_counter()
        result = await detector.detect(query)
        t_end = time.perf_counter()
        
        duration = t_end - t_start
        correct = (result == expected)
        
        print(f"✅ 檢測結果: {result} ({['正確', '不正確'][result]})")
        print(f"⏱️  耗時: {duration:.3f} 秒")
        print(f"📊 狀態: {'✓ 正確' if correct else '✗ 錯誤'}")
        
        results.append({
            "query": query,
            "expected": expected,
            "result": result,
            "duration": duration,
            "correct": correct,
            "description": description
        })
    
    # 總結
    print(f"\n{'='*70}")
    print(f"📊 C 值檢測測試總結")
    print(f"{'='*70}")
    
    total = len(results)
    correct_count = sum(1 for r in results if r["correct"])
    avg_duration = sum(r["duration"] for r in results) / total
    max_duration = max(r["duration"] for r in results)
    min_duration = min(r["duration"] for r in results)
    
    print(f"  總測試數: {total}")
    print(f"  正確數: {correct_count}")
    print(f"  準確率: {correct_count/total*100:.1f}%")
    print(f"  平均耗時: {avg_duration:.3f} 秒")
    print(f"  最大耗時: {max_duration:.3f} 秒")
    print(f"  最小耗時: {min_duration:.3f} 秒")
    
    if max_duration > 5.0:
        print(f"\n⚠️  警告：最大耗時超過 5 秒，可能存在效能問題")
    elif max_duration > 2.0:
        print(f"\n⚠️  注意：最大耗時超過 2 秒，建議進一步優化")
    else:
        print(f"\n✅ 效能良好：所有請求都在 2 秒內完成")
    
    print(f"{'='*70}")
    
    return results

async def test_parallel_execution():
    """測試並行執行效能"""
    print("\n" + "="*70)
    print("🧪 測試並行執行效能")
    print("="*70)
    
    k_detector = KnowledgeDetector()
    c_detector = CorrectnessDetector()
    
    query = "什麼是 IPv4 和 IPv6？"
    print(f"\n📝 測試查詢: {query}")
    
    # 串行執行
    print(f"\n{'─'*70}")
    print(f"🔄 串行執行測試")
    print(f"{'─'*70}")
    
    t_serial_start = time.perf_counter()
    k_result = await k_detector.detect(query)
    c_result = await c_detector.detect(query)
    t_serial_end = time.perf_counter()
    
    serial_duration = t_serial_end - t_serial_start
    print(f"\n⏱️  串行執行總耗時: {serial_duration:.3f} 秒")
    
    # 並行執行
    print(f"\n{'─'*70}")
    print(f"⚡ 並行執行測試")
    print(f"{'─'*70}")
    
    t_parallel_start = time.perf_counter()
    k_result, c_result = await asyncio.gather(
        k_detector.detect(query),
        c_detector.detect(query)
    )
    t_parallel_end = time.perf_counter()
    
    parallel_duration = t_parallel_end - t_parallel_start
    print(f"\n⏱️  並行執行總耗時: {parallel_duration:.3f} 秒")
    
    # 分析
    print(f"\n{'='*70}")
    print(f"📊 並行執行效能分析")
    print(f"{'='*70}")
    
    speedup = serial_duration / parallel_duration
    efficiency = (serial_duration - parallel_duration) / serial_duration * 100
    
    print(f"  串行耗時: {serial_duration:.3f} 秒")
    print(f"  並行耗時: {parallel_duration:.3f} 秒")
    print(f"  加速比: {speedup:.2f}x")
    print(f"  效率提升: {efficiency:.1f}%")
    
    if speedup > 1.5:
        print(f"\n✅ 並行效能優秀：加速比 > 1.5x")
    elif speedup > 1.2:
        print(f"\n✅ 並行效能良好：加速比 > 1.2x")
    else:
        print(f"\n⚠️  並行效能不佳：加速比 < 1.2x，可能存在瓶頸")
    
    print(f"{'='*70}")

async def main():
    """主函數"""
    print("\n" + "="*70)
    print("🚀 優化效果測試工具")
    print("="*70)
    
    # 驗證模型配置
    Config.verify_model_config()
    
    # 1. 測試知識點檢測
    k_results = await test_knowledge_detection()
    
    # 2. 測試 C 值檢測
    c_results = await test_correctness_detection()
    
    # 3. 測試並行執行
    await test_parallel_execution()
    
    print("\n" + "="*70)
    print("✅ 所有測試完成")
    print("="*70)
    
    # 最終總結
    print(f"\n{'='*70}")
    print(f"📈 最終總結")
    print(f"{'='*70}")
    
    k_success_rate = sum(1 for r in k_results if r["success"]) / len(k_results) * 100
    c_accuracy = sum(1 for r in c_results if r["correct"]) / len(c_results) * 100
    k_avg_time = sum(r["duration"] for r in k_results) / len(k_results)
    c_avg_time = sum(r["duration"] for r in c_results) / len(c_results)
    
    print(f"  知識點檢測成功率: {k_success_rate:.1f}%")
    print(f"  C 值檢測準確率: {c_accuracy:.1f}%")
    print(f"  知識點檢測平均耗時: {k_avg_time:.3f} 秒")
    print(f"  C 值檢測平均耗時: {c_avg_time:.3f} 秒")
    
    if k_success_rate >= 80 and c_accuracy >= 80:
        print(f"\n✅ 優化效果良好：準確率都達到 80% 以上")
    else:
        print(f"\n⚠️  需要進一步優化：準確率未達標")
    
    if c_avg_time < 2.0:
        print(f"✅ C 值檢測效能優秀：平均耗時 < 2 秒")
    elif c_avg_time < 5.0:
        print(f"⚠️  C 值檢測效能尚可：平均耗時 < 5 秒")
    else:
        print(f"❌ C 值檢測效能不佳：平均耗時 > 5 秒")
    
    print(f"{'='*70}\n")

if __name__ == "__main__":
    asyncio.run(main())
