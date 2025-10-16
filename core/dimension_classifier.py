"""
維度分類器（集中管理器）
協調 K, C, R 三個維度的檢測工具，並行執行 API 調用
"""
import asyncio
from typing import Dict, List
from core.tools.correctness_detector import CorrectnessDetector
from core.tools.knowledge_detector import KnowledgeDetector
from core.tools.repetition_checker import RepetitionChecker
from core.scenario_calculator import ScenarioCalculator


class DimensionClassifier:
    """維度分類器（集中管理器）"""
    
    def __init__(self, api_key: str = None, timer=None):
        """
        初始化集中管理器
        
        Args:
            api_key: OpenAI API Key
            timer: 計時器（可選）
        """
        # 初始化 3 個工具
        self.correctness_detector = CorrectnessDetector(api_key, timer)
        self.knowledge_detector = KnowledgeDetector(api_key, timer)
        self.repetition_checker = RepetitionChecker()
        
        # 情境計算器
        self.scenario_calculator = ScenarioCalculator()
        
        self.timer = timer
    
    async def classify_all(self, query: str) -> Dict:
        """
        執行完整的維度分類流程
        
        流程：
        1. 並行執行 2 次 API 調用（C 值和知識點檢測）
        2. 從知識點檢測結果計算 K 值（本地計算）
        3. 檢測 R 值並更新歷史記錄（本地計算）
        4. 計算情境編號
        
        Args:
            query: 用戶問題
            
        Returns:
            Dict: {
                "K": 0/1/2,                    # 知識點數量
                "C": 0/1,                      # 正確性
                "R": 0/1,                      # 重複性
                "knowledge_points": List[str], # 知識點名稱列表
                "scenario_number": int         # 情境編號 1-12
            }
        """
        # 並行執行 2 次 API 調用
        c_value, knowledge_points = await asyncio.gather(
            self.correctness_detector.detect(query),
            self.knowledge_detector.detect(query)
        )
        
        # 本地計算 K 值（從知識點列表）
        k_value = self.knowledge_detector.calculate_k_value(knowledge_points)
        
        # 檢測 R 值並更新歷史記錄
        r_value = self.repetition_checker.check_and_update(knowledge_points)
        
        # 計算情境編號
        scenario_number = self.scenario_calculator.calculate(k_value, c_value, r_value)
        
        # 打印結果
        print(f"\n🔍 維度分類結果：")
        print(f"  K (知識點數量): {k_value} ({['零個', '一個', '多個'][k_value]})")
        print(f"  C (正確性): {c_value} ({['正確', '不正確'][c_value]})")
        print(f"  R (重複性): {r_value} ({['正常', '重複'][r_value]})")
        print(f"  知識點: {knowledge_points if knowledge_points else '無'}")
        print(f"✅ 計算得出情境編號：{scenario_number}")
        
        return {
            "K": k_value,
            "C": c_value,
            "R": r_value,
            "knowledge_points": knowledge_points,
            "scenario_number": scenario_number
        }
