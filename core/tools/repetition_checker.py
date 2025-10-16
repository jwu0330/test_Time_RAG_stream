"""
重複性檢測工具
檢查當前知識點是否與前兩次歷史記錄重複
"""
from typing import List
from collections import deque


class RepetitionChecker:
    """重複性檢測器"""
    
    def __init__(self):
        """初始化重複性檢測器"""
        # 只記錄最近兩次的知識點集合
        self.history = deque(maxlen=2)
    
    def check_and_update(self, current_kps: List[str]) -> int:
        """
        檢查是否重複，然後更新歷史記錄
        
        邏輯：
        1. 檢查當前知識點是否與前兩次共同出現的知識點重疊
        2. 若有重疊 → 重複（返回1）
        3. 若無重疊 → 正常（返回0）
        4. 將當前知識點加入佇列（自動維持僅兩筆記錄）
        
        Args:
            current_kps: 當前知識點列表，例如 ["深度學習", "機器學習基礎"]
            
        Returns:
            int: 0=正常, 1=重複
        """
        # 如果歷史記錄少於2筆，返回正常
        if len(self.history) < 2:
            self.history.append(set(current_kps))
            return 0
        
        # 找出前兩次共同出現的知識點
        common = set(self.history[0]) & set(self.history[1])
        
        # 檢查當前知識點是否與共同知識點重疊
        current_set = set(current_kps)
        if current_set & common:
            # 有重疊 → 重複
            self.history.append(current_set)
            return 1
        
        # 無重疊 → 正常
        self.history.append(current_set)
        return 0
