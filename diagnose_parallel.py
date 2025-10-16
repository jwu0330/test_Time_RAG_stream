#!/usr/bin/env python3
"""
並行執行診斷腳本
用於驗證執行緒獨立性和檢測問題
"""
import asyncio
import time
import json
from core.tools.knowledge_detector import KnowledgeDetector
from core.tools.correctness_detector import CorrectnessDetector
from config import Config

async def test_knowledge_detector():
    """測試知識點檢測器"""
    print("\n" + "="*70)
    print("🧪 測試知識點檢測器")
    print("="*70)
    
    detector = KnowledgeDetector()
    
    # 1. 檢查知識點列表是否正確載入
    print(f"\n📋 已載入知識點數量: {len(detector.knowledge_points)}")
    print(f"📝 前 10 個知識點: {detector.knowledge_points[:10]}")
    
    # 2. 測試檢測功能
    test_query = "什麼是 IPv4 和 IPv6？"
    print(f"\n🔍 測試查詢: {test_query}")
    
    t_start = time.perf_counter()
    result = await detector.detect(test_query)
    t_end = time.perf_counter()
    
    print(f"✅ 檢測結果: {result}")
    print(f"⏱️  耗時: {t_end - t_start:.3f} 秒")
    
    # 3. 計算 K 值
    k_value = detector.calculate_k_value(result)
    print(f"📊 K 值: {k_value} ({['零個', '一個', '多個'][k_value]})")
    
    return result

async def test_correctness_detector():
    """測試正確性檢測器"""
    print("\n" + "="*70)
    print("🧪 測試正確性檢測器")
    print("="*70)
    
    detector = CorrectnessDetector()
    
    test_queries = [
        "什麼是 IPv4 和 IPv6？",
        "IPv4 比 IPv6 更先進",  # 錯誤陳述
        "今天天氣如何？"  # 正常問題
    ]
    
    for query in test_queries:
        print(f"\n🔍 測試查詢: {query}")
        
        t_start = time.perf_counter()
        result = await detector.detect(query)
        t_end = time.perf_counter()
        
        print(f"✅ 檢測結果: {result} ({['正確', '不正確'][result]})")
        print(f"⏱️  耗時: {t_end - t_start:.3f} 秒")

async def test_parallel_execution():
    """測試並行執行"""
    print("\n" + "="*70)
    print("🧪 測試並行執行獨立性")
    print("="*70)
    
    k_detector = KnowledgeDetector()
    c_detector = CorrectnessDetector()
    
    test_query = "什麼是 IPv4 和 IPv6？"
    print(f"\n🔍 測試查詢: {test_query}")
    
    # 記錄每個任務的開始和結束時間
    times = {}
    
    async def task_with_timing(name, coro):
        times[f"{name}_start"] = time.perf_counter()
        result = await coro
        times[f"{name}_end"] = time.perf_counter()
        return result
    
    # 並行執行
    print("\n⏱️  開始並行執行...")
    t_parallel_start = time.perf_counter()
    
    k_result, c_result = await asyncio.gather(
        task_with_timing("knowledge", k_detector.detect(test_query)),
        task_with_timing("correctness", c_detector.detect(test_query))
    )
    
    t_parallel_end = time.perf_counter()
    
    # 分析結果
    print("\n📊 並行執行分析:")
    print(f"  知識點檢測: {k_result}")
    print(f"  正確性檢測: {c_result}")
    
    k_duration = times["knowledge_end"] - times["knowledge_start"]
    c_duration = times["correctness_end"] - times["correctness_start"]
    parallel_duration = t_parallel_end - t_parallel_start
    
    print(f"\n⏱️  時間分析:")
    print(f"  知識點檢測耗時: {k_duration:.3f} 秒")
    print(f"  正確性檢測耗時: {c_duration:.3f} 秒")
    print(f"  並行執行總時間: {parallel_duration:.3f} 秒")
    print(f"  理論最大時間: {max(k_duration, c_duration):.3f} 秒")
    
    # 驗證並行性
    max_sequential = k_duration + c_duration
    efficiency = (max_sequential - parallel_duration) / max_sequential * 100
    
    print(f"\n✅ 並行效率分析:")
    print(f"  串行執行預計時間: {max_sequential:.3f} 秒")
    print(f"  並行執行實際時間: {parallel_duration:.3f} 秒")
    print(f"  節省時間: {max_sequential - parallel_duration:.3f} 秒")
    print(f"  效率提升: {efficiency:.1f}%")
    
    # 檢查是否真正並行
    k_start = times["knowledge_start"]
    c_start = times["correctness_start"]
    start_diff = abs(k_start - c_start)
    
    print(f"\n🔍 並行啟動驗證:")
    print(f"  兩個任務啟動時間差: {start_diff*1000:.2f} 毫秒")
    
    if start_diff < 0.01:  # 小於 10 毫秒
        print(f"  ✅ 確認為真正的並行執行")
    else:
        print(f"  ⚠️  可能存在串行等待")

async def test_api_response_format():
    """測試 API 回應格式"""
    print("\n" + "="*70)
    print("🧪 測試 API 回應格式（詳細除錯）")
    print("="*70)
    
    from openai import OpenAI
    from config import get_shared_client
    
    client = get_shared_client()
    
    # 載入知識點列表
    try:
        with open('data/knowledge_points.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        knowledge_points = data.get('nodes', [])
        print(f"✅ 成功載入 {len(knowledge_points)} 個知識點")
    except Exception as e:
        print(f"❌ 載入失敗: {e}")
        return
    
    # 構建提示詞
    knowledge_list = "\n".join([f"- {kp}" for kp in knowledge_points])
    query = "什麼是 IPv4 和 IPv6？"
    
    prompt = f"""問題：「{query}」

知識點列表（名稱即唯一關鍵詞，請嚴格字面匹配）：
{knowledge_list}

規則：
1. 僅當問題文本中「完整出現相同字串」時，才返回該知識點名稱。
2. 不要推測，不要使用同義詞、英文或縮寫，不要延伸推理。
3. 返回順序不限，若無匹配請返回空陣列。"""
    
    # 定義 Function Call
    functions = [
        {
            "name": "return_knowledge_points",
            "description": "返回這句話直接涉及的知識點，如果不涉及任何知識點則返回空列表",
            "parameters": {
                "type": "object",
                "properties": {
                    "knowledge_points": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "知識點名稱列表"
                    }
                },
                "required": ["knowledge_points"]
            }
        }
    ]
    
    print(f"\n📤 發送請求...")
    print(f"  模型: gpt-4o-mini")
    print(f"  max_tokens: 100")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "只做嚴格中文字面匹配"},
            {"role": "user", "content": prompt}
        ],
        functions=functions,
        function_call={"name": "return_knowledge_points"},
        temperature=0,
        max_tokens=100
    )
    
    # 分析回應
    function_call = response.choices[0].message.function_call
    
    if function_call:
        raw_args = function_call.arguments or ""
        print(f"\n📥 API 回應:")
        print(f"  函數名稱: {function_call.name}")
        print(f"  參數長度: {len(raw_args)} 字元")
        print(f"  原始參數: {raw_args}")
        
        # 嘗試解析
        try:
            arguments = json.loads(raw_args)
            print(f"\n✅ JSON 解析成功:")
            print(f"  {json.dumps(arguments, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"\n❌ JSON 解析失敗: {e}")
            print(f"  錯誤類型: {type(e).__name__}")
            
            # 嘗試修復
            if '}' in raw_args:
                fixed = raw_args[: raw_args.rfind('}') + 1]
                print(f"\n🔧 嘗試修復（截斷到最後一個 }}）:")
                print(f"  修復後: {fixed}")
                try:
                    arguments = json.loads(fixed)
                    print(f"  ✅ 修復成功: {arguments}")
                except Exception as e2:
                    print(f"  ❌ 修復失敗: {e2}")
    else:
        print(f"\n❌ 沒有 function_call")

async def main():
    """主函數"""
    print("\n" + "="*70)
    print("🚀 並行執行診斷工具")
    print("="*70)
    
    # 1. 測試知識點檢測器
    await test_knowledge_detector()
    
    # 2. 測試正確性檢測器
    await test_correctness_detector()
    
    # 3. 測試並行執行
    await test_parallel_execution()
    
    # 4. 測試 API 回應格式
    await test_api_response_format()
    
    print("\n" + "="*70)
    print("✅ 診斷完成")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
