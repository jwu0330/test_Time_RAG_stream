"""
四向度獨立分類器
每個向度使用獨立的 API 調用，確保精準判定
"""
from openai import OpenAI
from typing import List, Dict, Optional
from config import Config


class DimensionClassifiers:
    """四向度獨立分類器"""
    
    def __init__(self, api_key: str = None, timer=None):
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.timer = timer  # 外部傳入的計時器
    
    # 移除：不再使用 RAG 匹配結果生成二進制編碼
    # D4 API 會直接判定知識點並返回二進制編碼
    
    # 移除：D1 不再從 RAG 計算，改為從 D4 API 返回的二進制編碼計算
    
    # 移除：不再需要檢查指代詞，因為 D1 完全從 D4 計算
    
    # 移除：D1 不再使用 API，完全從 D4 的二進制編碼計算
    
    async def classify_d2_has_error(self, query: str) -> int:
        """
        D2: 表達錯誤判定（不需要歷史）
        
        Args:
            query: 當前問題
            
        Returns:
            int: 0=無錯誤, 1=有錯誤
        """
        if self.timer:
            self.timer.start_stage("D2 API 調用", thread='C')
        
        prompt = f"""問題: {query}

是否有錯誤或矛盾？返回 JSON: {{"error": 0}} 或 {{"error": 1}}
0=無錯誤, 1=有錯誤"""
        
        response = self.client.chat.completions.create(
            model=Config.CLASSIFIER_MODEL,
            messages=[
                {"role": "system", "content": "只返回 JSON: {\"error\": 0} 或 {\"error\": 1}"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0,
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        
        if self.timer:
            self.timer.stop_stage("D2 API 調用", thread='C')
        
        # 解析 JSON，直接返回數字
        import json
        try:
            data = json.loads(result)
            return data.get("error", 0)  # 直接返回 0/1
        except:
            return 0  # 默認值
    
    async def classify_d3_detail_level(self, query: str) -> int:
        """
        D3: 表達詳細度判定（不需要歷史）
        
        Args:
            query: 當前問題
            
        Returns:
            int: 0=粗略, 1=非常詳細
        """
        if self.timer:
            self.timer.start_stage("D3 API 調用", thread='D')
        
        prompt = f"""問題: {query}

表達是否詳細？返回 JSON: {{"detail": 0}} 或 {{"detail": 1}}
0=粗略, 1=非常詳細"""
        
        response = self.client.chat.completions.create(
            model=Config.CLASSIFIER_MODEL,
            messages=[
                {"role": "system", "content": "只返回 JSON: {\"detail\": 0} 或 {\"detail\": 1}"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0,
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        
        if self.timer:
            self.timer.stop_stage("D3 API 調用", thread='D')
        
        # 解析 JSON，直接返回數字
        import json
        try:
            data = json.loads(result)
            return data.get("detail", 0)  # 直接返回 0/1
        except:
            return 0  # 默認值
    
    # 移除：改用 test_binary_logic.count_knowledge_points()
    
    async def classify_d4_knowledge_detection(self, query: str) -> str:
        """
        D4 API: 判定當前問題觸及了哪些知識點（返回二進制編碼）
        
        Args:
            query: 當前問題
            
        Returns:
            str: 四位二進制字串，例如 "1011"
                 位置 0: 機器學習基礎
                 位置 1: 深度學習
                 位置 2: 自然語言處理
                 位置 3: 保留
        """
        if self.timer:
            self.timer.start_stage("D4 API 調用（知識點檢測）", thread='E')
        
        prompt = f"""問題: {query}

知識點列表：
1. 機器學習基礎 (ml_basics)
2. 深度學習 (deep_learning)
3. 自然語言處理 (nlp)

這個問題涉及哪些知識點？返回 JSON: {{"binary": "1010"}}
其中每一位代表是否涉及該知識點（1=涉及，0=不涉及）
例如："1010" 表示涉及第1和第3個知識點"""
        
        response = self.client.chat.completions.create(
            model=Config.CLASSIFIER_MODEL,
            messages=[
                {"role": "system", "content": "只返回 JSON: {\"binary\": \"0000\"} 格式，四位二進制字串"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0,
            max_tokens=20
        )
        
        result = response.choices[0].message.content.strip()
        
        if self.timer:
            self.timer.stop_stage("D4 API 調用（知識點檢測）", thread='E')
        
        # 解析 JSON
        import json
        try:
            data = json.loads(result)
            binary = data.get("binary", "0000")
            # 確保是4位字串
            if len(binary) == 4 and all(c in '01' for c in binary):
                return binary
            return "0000"
        except:
            return "0000"
    
    def classify_d4_repetition_from_history(self, current_binary: str, history_binaries: List[str]) -> int:
        """
        D4 重複判定：只檢查當前觸及的知識點（值為1的位置）是否在歷史中也連續為1
        
        優化邏輯（避免浪費時間）：
        1. 找出當前二進制中值為"1"的位置（這些是當前觸及的知識點）
        2. 對每個值為"1"的位置，檢查歷史最近2筆該位置是否也都為"1"
        3. 如果任何一個位置連續3次為"1"，則返回 1（重複）
        
        Args:
            current_binary: 當前問題的二進制編碼（從 D4 API 獲得）
            history_binaries: 歷史二進制編碼列表（不包含當前）
            
        Returns:
            int: 0=正常狀態, 1=重複狀態
            
        Example:
            current_binary = "1011"              # 第0,2,3位為1
            history_binaries = ["1010", "1001"]  # 歷史最近2筆
            
            檢查第0位: 當前=1, 歷史=[1,1] → 連續3次為1 ✓
            檢查第2位: 當前=1, 歷史=[1,0] → 不連續
            檢查第3位: 當前=1, 歷史=[0,1] → 不連續
            → 返回 1（重複）
        """
        # 需要至少2筆歷史才能判定（歷史2筆 + 當前1筆 = 3筆）
        if len(history_binaries) < 2:
            return 0
        
        # 取最近2筆歷史
        recent_2 = history_binaries[-2:]
        
        # 找出當前觸及的知識點（值為"1"的位置）
        for pos in range(len(current_binary)):
            if current_binary[pos] == '1':
                # 檢查這個位置在歷史最近2筆是否也都為"1"
                if all(history[pos] == '1' for history in recent_2):
                    # 該位置連續3次為"1"（歷史2次 + 當前1次）
                    return 1  # 觸發重複
        
        # 沒有任何位置連續3次為"1"
        return 0
    
    async def classify_all_parallel(self, query: str, history: List[Dict] = None, matched_docs: List[str] = None) -> Dict[str, int]:
        """
        並行執行 3 個 API 調用（D2, D3, D4）+ D1 本地計算
        
        流程：
        1. 並行調用 D2, D3, D4 API
        2. D4 API 返回二進制編碼（例如 "1011"）
        3. D1 從 D4 的二進制編碼計算知識點數量
        4. D4 重複判定從歷史二進制編碼判斷
        
        Args:
            query: 當前問題
            history: 歷史對話（包含 'knowledge_binary' 欄位）
            matched_docs: 不再使用（保留參數以兼容舊代碼）
            
        Returns:
            Dict[str, int]: 四向度判定結果
            {
                "D1": 0/1/2,  # 從 D4 的二進制編碼計算
                "D2": 0/1,    # API 調用
                "D3": 0/1,    # API 調用
                "D4": 0/1,    # 從歷史判定重複
                "knowledge_binary": str  # D4 API 返回的二進制編碼
            }
        """
        import asyncio
        from test_binary_logic import count_knowledge_points
        
        # 並行執行 3 個 API 調用：D2, D3, D4
        results = await asyncio.gather(
            self.classify_d2_has_error(query),
            self.classify_d3_detail_level(query),
            self.classify_d4_knowledge_detection(query)  # D4 API 返回二進制編碼
        )
        
        d2 = results[0]  # 0/1
        d3 = results[1]  # 0/1
        current_binary = results[2]  # "1011" (字串格式)
        
        # D1: 從 D4 返回的二進制編碼計算知識點數量（本地計算，不調用 API）
        count = count_knowledge_points(current_binary)
        if count == 0:
            d1 = 0  # 零個
        elif count == 1:
            d1 = 1  # 一個
        else:
            d1 = 2  # 多個（>= 2）
        
        # 提取歷史的二進制編碼
        history_binaries = []
        if history:
            for item in history:
                binary = item.get('knowledge_binary', '0000')
                history_binaries.append(binary)
        
        # D4 重複判定：使用簡化的邏輯（檢查最近3筆是否有連續的"111"）
        d4 = self.classify_d4_repetition_from_history(current_binary, history_binaries)
        
        return {
            "D1": d1,                    # 0/1/2（本地計算）
            "D2": d2,                    # 0/1（API）
            "D3": d3,                    # 0/1（API）
            "D4": d4,                    # 0/1（本地判定）
            "knowledge_binary": current_binary  # 二進制編碼（用於存入歷史）
        }
    
    def dimensions_to_scenario_number(self, dimensions: Dict[str, int]) -> int:
        """
        根據四向度計算情境編號（後端自行計算）
        
        Args:
            dimensions: 四向度數字值
            {
                "D1": 0/1/2,  # 0=零個, 1=一個, 2=多個
                "D2": 0/1,    # 0=有錯誤, 1=無錯誤
                "D3": 0/1,    # 0=粗略, 1=非常詳細
                "D4": 0/1     # 0=重複, 1=正常
            }
            
        Returns:
            情境編號 (1-24)
        """
        # 直接使用數字計算，不需要映射
        d1 = dimensions.get("D1", 1)  # 默認 1=一個
        d2 = dimensions.get("D2", 1)  # 默認 1=無錯誤
        d3 = dimensions.get("D3", 0)  # 默認 0=粗略
        d4 = dimensions.get("D4", 1)  # 默認 1=正常
        
        # 計算情境編號
        scenario_number = d1 * 8 + d2 * 4 + d3 * 2 + d4 + 1
        
        return scenario_number
