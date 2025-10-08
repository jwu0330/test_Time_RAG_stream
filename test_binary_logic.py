#!/usr/bin/env python3
"""
知識點重複判定系統 - 簡化版

核心功能：
1. 使用二進制字符串表示知識點（例如："1010" 表示涉及第1和第3個知識點）
2. 檢測最近3筆對話是否有連續重複（某個位置連續3次都是"1"）
3. 計算涉及的知識點數量

主要函數：
- add_conversation_record(history_list, binary_str): 添加對話紀錄
- detect_repetition(history_list): 檢測是否觸發重複
- count_knowledge_points(binary_str): 計算涉及的知識點數量
"""


# ============================================================================
# 核心函數：3個主要函數（簡化版）
# ============================================================================

def add_conversation_record(history_list, binary_str):
    """
    函數1：添加對話紀錄到歷史列表
    
    Args:
        history_list: 歷史對話列表（會被直接修改）
        binary_str: 二進制字符串，例如 "1011" 表示涉及第1、3、4個知識點
    
    Returns:
        None（直接修改 history_list）
    
    Example:
        history = []
        add_conversation_record(history, "1000")
        add_conversation_record(history, "1000")
        # history 現在包含兩筆紀錄
    
    Note:
        - 自動限制最多保留10筆紀錄
        - 超過10筆時，自動刪除最舊的
    """
    history_list.append(binary_str)
    
    # 限制最多保留10筆
    if len(history_list) > 10:
        history_list.pop(0)


def detect_repetition(history_list):
    """
    函數2：檢測是否觸發重複（檢查最近3筆）
    
    判定規則：
    - 檢查最近3筆對話
    - 如果某個位置連續3次都是"1"，則觸發重複
    - 返回 1 表示重複，0 表示正常
    
    Args:
        history_list: 歷史對話列表（二進制字符串列表）
    
    Returns:
        int: 0=正常狀態, 1=重複狀態
    
    Example:
        history = ["1000", "1000", "1000"]
        result = detect_repetition(history)
        # result == 1（第1個位置連續3次都是"1"）
        
        history = ["1000", "0100", "0010"]
        result = detect_repetition(history)
        # result == 0（沒有任何位置連續3次都是"1"）
    """
    # 需要至少3筆紀錄才能判定
    if len(history_list) < 3:
        return 0
    
    # 取最近3筆對話
    recent_3 = history_list[-3:]
    
    # 檢查每個位置是否連續3次都是"1"
    repeated_positions = []
    binary_length = len(recent_3[0]) if recent_3 else 4
    
    for pos in range(binary_length):
        # 檢查這個位置在最近3次是否都是"1"
        if all(binary[pos] == '1' for binary in recent_3):
            repeated_positions.append(pos)
    
    # 只要有任何位置重複，就返回1
    return 1 if len(repeated_positions) >= 1 else 0


def count_knowledge_points(binary_str):
    """
    函數3：計算二進制字符串中涉及的知識點數量
    
    Args:
        binary_str: 二進制字符串，例如 "1011"
    
    Returns:
        int: 涉及的知識點總數（"1"的個數）
    
    Example:
        count_knowledge_points("1011") -> 3
        count_knowledge_points("0000") -> 0
        count_knowledge_points("1000") -> 1
    
    Note:
        - 可用於判斷 D1（知識點數量）
        - 0 = 零個知識點
        - 1 = 一個知識點
        - >= 2 = 多個知識點
    """
    return binary_str.count('1')


# ============================================================================
# 測試函數
# ============================================================================

def test_basic_functions():
    """測試基本函數功能"""
    print("=" * 80)
    print("測試 1: 基本函數功能")
    print("=" * 80)
    
    # 測試 count_knowledge_points
    print("\n[測試 count_knowledge_points]")
    test_cases = [
        ("0000", 0),
        ("1000", 1),
        ("1010", 2),
        ("1111", 4),
        ("0101", 2),
    ]
    for binary, expected in test_cases:
        result = count_knowledge_points(binary)
        status = "✓" if result == expected else "✗"
        print(f"  {binary} -> {result} 個知識點 (預期: {expected}) {status}")
    
    # 測試 add_conversation_record
    print("\n[測試 add_conversation_record]")
    history = []
    add_conversation_record(history, "1000")
    add_conversation_record(history, "0100")
    add_conversation_record(history, "1010")
    print(f"  添加3筆紀錄後，歷史長度: {len(history)} (預期: 3) {'✓' if len(history) == 3 else '✗'}")
    print(f"  紀錄內容: {history}")
    
    # 測試最多10筆限制
    print("\n[測試歷史紀錄限制（最多10筆）]")
    history = []
    for i in range(15):
        add_conversation_record(history, "1000")
    print(f"  添加15筆後，歷史長度: {len(history)} (預期: 10) {'✓' if len(history) == 10 else '✗'}")


def test_repetition_detection():
    """測試重複判定邏輯"""
    print("\n" + "=" * 80)
    print("測試 2: 重複判定邏輯（detect_repetition）")
    print("=" * 80)
    
    test_cases = [
        {
            "name": "案例1: 單知識點重複（連續3次 '1000'）",
            "history": ["1000", "1000", "1000"],
            "expected": 1
        },
        {
            "name": "案例2: 多知識點重複（連續3次 '1100'）",
            "history": ["1100", "1100", "1100"],
            "expected": 1
        },
        {
            "name": "案例3: 沒有重複（不同知識點）",
            "history": ["1000", "0100", "0010"],
            "expected": 0
        },
        {
            "name": "案例4: 只有2次重複（不觸發）",
            "history": ["1000", "1000"],
            "expected": 0
        },
        {
            "name": "案例5: 部分重疊（只有第1位重複）",
            "history": ["1100", "1010", "1001"],
            "expected": 1
        },
        {
            "name": "案例6: 複雜情況 - '1110' 連續3次",
            "history": ["1110", "1110", "1110"],
            "expected": 1
        },
        {
            "name": "案例7: 部分重疊 - 只有第1位連續3次",
            "history": ["1100", "1100", "1010"],
            "expected": 1
        },
    ]
    
    for case in test_cases:
        result = detect_repetition(case["history"])
        status = "✓" if result == case["expected"] else "✗"
        print(f"\n{status} {case['name']}")
        print(f"  歷史紀錄: {case['history']}")
        print(f"  結果: {result} (預期: {case['expected']})")


def test_complete_workflow():
    """測試完整工作流程"""
    print("\n" + "=" * 80)
    print("測試 3: 完整工作流程模擬")
    print("=" * 80)
    
    print("\n情境：用戶連續詢問關於機器學習的問題\n")
    
    # 初始化歷史紀錄
    history = []
    
    # 模擬對話流程
    conversations = [
        ("什麼是機器學習？", "1000"),
        ("機器學習有哪些應用？", "1000"),
        ("機器學習的基本概念是什麼？", "1000"),  # 第3次，應該觸發重複
        ("深度學習是什麼？", "0100"),
        ("機器學習和深度學習有什麼關係？", "1100"),
        ("機器學習和深度學習的區別？", "1100"),
        ("再問一次機器學習和深度學習？", "1100"),  # 第3次，應該觸發重複
    ]
    
    for i, (question, binary) in enumerate(conversations, 1):
        print(f"\n--- 對話 {i} ---")
        print(f"用戶問題: {question}")
        print(f"AI判定涉及知識點: {binary} ({count_knowledge_points(binary)} 個知識點)")
        
        # 添加到歷史
        add_conversation_record(history, binary)
        
        # 檢測重複
        result = detect_repetition(history)
        
        if result == 1:
            print(f"⚠️  檢測到重複！")
        else:
            print(f"✓ 正常，無重複")
        
        print(f"當前歷史長度: {len(history)}")
        print(f"當前歷史內容: {history}")


if __name__ == "__main__":
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + " " * 25 + "知識點重複判定系統 - 簡化版" + " " * 25 + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    
    test_basic_functions()
    test_repetition_detection()
    test_complete_workflow()
    
    print("\n" + "=" * 80)
    print("✅ 所有測試完成")
    print("=" * 80)
    print("\n📋 使用說明：")
    print("  1. add_conversation_record(history, binary) - 添加對話紀錄（自動限制10筆）")
    print("  2. detect_repetition(history) - 檢測重複（檢查最近3筆）")
    print("  3. count_knowledge_points(binary) - 計算知識點數量")
    print("\n" + "=" * 80 + "\n")
