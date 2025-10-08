#!/usr/bin/env python3
"""
測試優化後的 D4 重複判定邏輯
"""

def test_optimized_d4():
    """測試優化後的 D4 重複判定"""
    print("=" * 80)
    print("測試優化後的 D4 重複判定邏輯")
    print("=" * 80)
    
    # 模擬優化後的邏輯
    def classify_d4_repetition(current_binary: str, history_binaries: list) -> int:
        """優化版本：只檢查當前觸及的知識點"""
        if len(history_binaries) < 2:
            return 0
        
        recent_2 = history_binaries[-2:]
        
        for pos in range(len(current_binary)):
            if current_binary[pos] == '1':
                if all(history[pos] == '1' for history in recent_2):
                    return 1
        return 0
    
    # 測試案例1：單知識點重複
    print("\n【案例1：單知識點重複】")
    current = "1000"
    history = ["1000", "1000"]
    result = classify_d4_repetition(current, history)
    print(f"當前: {current} (第0位為1)")
    print(f"歷史: {history}")
    print(f"檢查第0位: 當前=1, 歷史=[1,1] → 連續3次為1")
    print(f"結果: D4={result} {'✅' if result == 1 else '❌'}")
    
    # 測試案例2：多知識點重複
    print("\n【案例2：多知識點重複】")
    current = "1100"
    history = ["1100", "1100"]
    result = classify_d4_repetition(current, history)
    print(f"當前: {current} (第0,1位為1)")
    print(f"歷史: {history}")
    print(f"檢查第0位: 當前=1, 歷史=[1,1] → 連續3次為1 ✓")
    print(f"結果: D4={result} {'✅' if result == 1 else '❌'}")
    
    # 測試案例3：部分重疊（優化效果明顯）
    print("\n【案例3：部分重疊 - 優化效果明顯】")
    current = "1011"
    history = ["1010", "1001"]
    result = classify_d4_repetition(current, history)
    print(f"當前: {current} (第0,2,3位為1)")
    print(f"歷史: {history}")
    print(f"只檢查當前為1的位置：")
    print(f"  第0位: 當前=1, 歷史=[1,1] → 連續3次為1 ✓")
    print(f"  第2位: 當前=1, 歷史=[1,0] → 不連續 (跳過)")
    print(f"  第3位: 當前=1, 歷史=[0,1] → 不連續 (跳過)")
    print(f"  第1位: 當前=0 → 不檢查 (節省時間)")
    print(f"結果: D4={result} {'✅' if result == 1 else '❌'}")
    
    # 測試案例4：不重複
    print("\n【案例4：不重複】")
    current = "0010"
    history = ["1000", "0100"]
    result = classify_d4_repetition(current, history)
    print(f"當前: {current} (第2位為1)")
    print(f"歷史: {history}")
    print(f"檢查第2位: 當前=1, 歷史=[0,1] → 不連續")
    print(f"結果: D4={result} {'✅' if result == 0 else '❌'}")
    
    # 測試案例5：歷史不足
    print("\n【案例5：歷史不足】")
    current = "1000"
    history = ["1000"]
    result = classify_d4_repetition(current, history)
    print(f"當前: {current}")
    print(f"歷史: {history} (只有1筆)")
    print(f"結果: D4={result} (歷史不足，返回0) {'✅' if result == 0 else '❌'}")
    
    # 測試案例6：當前沒有觸及任何知識點
    print("\n【案例6：當前沒有觸及任何知識點】")
    current = "0000"
    history = ["1000", "1000"]
    result = classify_d4_repetition(current, history)
    print(f"當前: {current} (沒有任何位置為1)")
    print(f"歷史: {history}")
    print(f"不需要檢查任何位置 (節省時間)")
    print(f"結果: D4={result} {'✅' if result == 0 else '❌'}")
    
    print("\n" + "=" * 80)
    print("✅ 優化測試完成")
    print("=" * 80)
    print("\n🚀 優化效果：")
    print("  ✓ 只檢查當前觸及的知識點（值為1的位置）")
    print("  ✓ 避免檢查所有4個位置，節省計算時間")
    print("  ✓ 邏輯更清晰：只關注當前相關的知識點")
    print("  ✓ 如果當前為 '0000'，完全不需要檢查")
    print("  ✓ 如果當前為 '1000'，只檢查1個位置（而非4個）")


if __name__ == "__main__":
    test_optimized_d4()
