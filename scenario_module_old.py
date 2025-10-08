"""
情境判定模組
負責分析情境並進行四向度分類 (D1-D4)
"""
import json
import os
from typing import Dict, List, Optional
from openai import OpenAI


class ScenarioClassifier:
    """情境分類器"""
    
    # 四向度定義
    DIMENSIONS = {
        "D1": "時間敏感性 (Time Sensitivity)",
        "D2": "情境複雜度 (Context Complexity)", 
        "D3": "專業領域 (Domain Expertise)",
        "D4": "互動模式 (Interaction Mode)"
    }
    
    def __init__(self, api_key: Optional[str] = None, use_small_model: bool = True):
        """
        初始化情境分類器
        
        Args:
            api_key: OpenAI API Key
            use_small_model: 是否使用小模型 (gpt-3.5-turbo)
        """
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.model = "gpt-3.5-turbo" if use_small_model else "gpt-4"
        self.scenarios: Dict[str, dict] = {}
    
    def load_scenarios_from_dir(self, scenarios_dir: str = "scenarios"):
        """
        從目錄載入所有情境文件
        
        Args:
            scenarios_dir: 情境文件目錄
        """
        if not os.path.exists(scenarios_dir):
            print(f"⚠️  情境目錄不存在: {scenarios_dir}")
            return
        
        for filename in os.listdir(scenarios_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(scenarios_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    scenario_data = json.load(f)
                    scenario_id = filename.replace('.json', '')
                    self.scenarios[scenario_id] = scenario_data
                    print(f"✅ 已載入情境: {scenario_id}")
            elif filename.endswith('.txt'):
                filepath = os.path.join(scenarios_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    scenario_id = filename.replace('.txt', '')
                    self.scenarios[scenario_id] = {"content": content}
                    print(f"✅ 已載入情境: {scenario_id}")
    
    async def classify_scenario(self, query: str, context: str = "") -> Dict[str, any]:
        """
        對查詢進行四向度分類
        
        Args:
            query: 用戶查詢
            context: 額外上下文
            
        Returns:
            分類結果，包含各向度的評分和建議
        """
        prompt = f"""
請分析以下查詢，並根據四個向度進行評分 (1-5分)：

查詢: {query}
上下文: {context}

向度說明：
- D1 (時間敏感性): 是否需要即時回應或有時間限制
- D2 (情境複雜度): 問題的複雜程度和需要的上下文量
- D3 (專業領域): 是否涉及專業知識或特定領域
- D4 (互動模式): 需要的互動類型 (單次/多輪/協作)

請以 JSON 格式回應：
{{
  "D1": {{"score": 1-5, "reason": "原因"}},
  "D2": {{"score": 1-5, "reason": "原因"}},
  "D3": {{"score": 1-5, "reason": "原因"}},
  "D4": {{"score": 1-5, "reason": "原因"}},
  "recommended_scenarios": ["scenario_id1", "scenario_id2"]
}}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一個專業的情境分析助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    def get_scenario_by_dimensions(self, classification: Dict) -> List[str]:
        """
        根據分類結果推薦情境
        
        Args:
            classification: 分類結果
            
        Returns:
            推薦的情境 ID 列表
        """
        # 簡單的規則匹配
        recommended = []
        
        # 提取各向度分數
        scores = {
            dim: classification.get(dim, {}).get("score", 0)
            for dim in ["D1", "D2", "D3", "D4"]
        }
        
        # 根據分數推薦情境
        for scenario_id, scenario_data in self.scenarios.items():
            if "dimensions" in scenario_data:
                match_score = sum(
                    1 for dim, score in scores.items()
                    if abs(score - scenario_data["dimensions"].get(dim, 0)) <= 1
                )
                if match_score >= 2:  # 至少匹配兩個向度
                    recommended.append(scenario_id)
        
        return recommended[:3]  # 返回最多3個
    
    def get_scenario_content(self, scenario_id: str) -> str:
        """
        獲取情境內容
        
        Args:
            scenario_id: 情境 ID
            
        Returns:
            情境內容文本
        """
        if scenario_id not in self.scenarios:
            return ""
        
        scenario = self.scenarios[scenario_id]
        if "content" in scenario:
            return scenario["content"]
        
        # 如果是結構化數據，轉換為文本
        return json.dumps(scenario, ensure_ascii=False, indent=2)
    
    def format_scenario_context(self, scenario_ids: List[str]) -> str:
        """
        格式化多個情境為上下文
        
        Args:
            scenario_ids: 情境 ID 列表
            
        Returns:
            格式化的情境上下文
        """
        if not scenario_ids:
            return ""
        
        parts = []
        for sid in scenario_ids:
            content = self.get_scenario_content(sid)
            if content:
                parts.append(f"[情境 {sid}]\n{content}\n")
        
        return "\n".join(parts)


class ScenarioInjector:
    """情境注入器 - 用於流式續寫"""
    
    def __init__(self, classifier: ScenarioClassifier):
        """
        初始化注入器
        
        Args:
            classifier: 情境分類器實例
        """
        self.classifier = classifier
    
    def create_injection_prompt(
        self, 
        draft_response: str,
        scenario_context: str,
        original_query: str
    ) -> str:
        """
        創建情境注入提示詞
        
        Args:
            draft_response: 初始草稿回應
            scenario_context: 情境上下文
            original_query: 原始查詢
            
        Returns:
            注入提示詞
        """
        prompt = f"""
你之前生成了一個初步回答的草稿。現在需要根據新的情境信息來完善這個回答。

原始問題：
{original_query}

初步草稿：
{draft_response}

情境信息：
{scenario_context}

請基於以上情境信息，完善並輸出最終的完整回答。確保回答：
1. 整合了情境中的關鍵信息
2. 保持連貫性和專業性
3. 直接給出最終答案，不需要重複草稿內容
"""
        return prompt
