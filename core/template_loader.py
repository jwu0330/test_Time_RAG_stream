"""
模板加載器
根據情境編號加載對應的 JSON 模板和回應策略
"""
import json
from pathlib import Path
from typing import Dict, Optional


class TemplateLoader:
    """模板加載器類"""
    
    def __init__(self, scenarios_path: str = "data/scenarios/scenarios_24.json"):
        """
        初始化模板加載器
        
        Args:
            scenarios_path: 情境配置文件路徑
        """
        self.scenarios_path = Path(scenarios_path)
        self.scenarios_data = None
        self.load_scenarios()
    
    def load_scenarios(self):
        """加載情境配置"""
        try:
            with open(self.scenarios_path, 'r', encoding='utf-8') as f:
                self.scenarios_data = json.load(f)
            print(f"✅ 已加載 {self.scenarios_data['total_scenarios']} 種情境配置")
        except Exception as e:
            print(f"❌ 加載情境配置失敗: {e}")
            self.scenarios_data = None
    
    def get_scenario(self, scenario_id: int) -> Optional[Dict]:
        """
        根據情境編號獲取情境配置
        
        Args:
            scenario_id: 情境編號（1-24）
            
        Returns:
            dict: 情境配置，如果不存在則返回 None
        """
        if not self.scenarios_data:
            return None
        
        # 查找對應的情境
        for scenario in self.scenarios_data.get('scenarios', []):
            if scenario.get('scenario_number') == scenario_id:
                return scenario
        
        print(f"⚠️  找不到情境 {scenario_id}，使用默認情境")
        return self.scenarios_data.get('scenarios', [{}])[13]  # 默認使用情境 14
    
    def get_scenario_description(self, scenario_id: int) -> str:
        """
        獲取情境描述
        
        Args:
            scenario_id: 情境編號
            
        Returns:
            str: 情境描述
        """
        scenario = self.get_scenario(scenario_id)
        if scenario:
            return scenario.get('description', '未知情境')
        return '未知情境'
    
    def get_scenario_dimensions(self, scenario_id: int) -> Dict[str, str]:
        """
        獲取情境的四向度值
        
        Args:
            scenario_id: 情境編號
            
        Returns:
            dict: 四向度值
        """
        scenario = self.get_scenario(scenario_id)
        if scenario:
            return scenario.get('dimensions', {})
        return {}
    
    def build_response_strategy(self, scenario_id: int) -> Dict:
        """
        根據情境編號構建回應策略
        
        Args:
            scenario_id: 情境編號
            
        Returns:
            dict: 回應策略配置
        """
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return self._get_default_strategy()
        
        dimensions = scenario.get('dimensions', {})
        
        # 根據四向度構建策略
        strategy = {
            "scenario_id": scenario_id,
            "description": scenario.get('description', ''),
            "dimensions": dimensions,
            "response_style": self._determine_response_style(dimensions),
            "knowledge_integration": self._determine_knowledge_integration(dimensions),
            "error_handling": self._determine_error_handling(dimensions),
            "detail_level": self._determine_detail_level(dimensions)
        }
        
        return strategy
    
    def _determine_response_style(self, dimensions: Dict[str, str]) -> str:
        """根據四向度決定回應風格"""
        d2 = dimensions.get('D2', '無錯誤')
        d3 = dimensions.get('D3', '粗略')
        d4 = dimensions.get('D4', '正常狀態')
        
        if d2 == '有錯誤':
            return "糾錯式：先指出錯誤，再提供正確解釋"
        elif d4 == '重複狀態':
            return "深化式：提供更深入的解釋或不同角度"
        elif d3 == '非常詳細':
            return "詳盡式：提供完整、詳細的解答"
        else:
            return "簡明式：提供清晰、簡潔的解答"
    
    def _determine_knowledge_integration(self, dimensions: Dict[str, str]) -> str:
        """根據四向度決定知識整合方式"""
        d1 = dimensions.get('D1', '一個')
        
        if d1 == '零個':
            return "引導式：引導用戶回到相關主題"
        elif d1 == '一個':
            return "聚焦式：專注於單一知識點的深入講解"
        else:  # 多個
            return "整合式：說明多個知識點之間的關聯"
    
    def _determine_error_handling(self, dimensions: Dict[str, str]) -> str:
        """根據四向度決定錯誤處理方式"""
        d2 = dimensions.get('D2', '無錯誤')
        
        if d2 == '有錯誤':
            return "先糾錯：明確指出錯誤並解釋為什麼是錯的"
        else:
            return "直接回答：問題表達正確，直接提供答案"
    
    def _determine_detail_level(self, dimensions: Dict[str, str]) -> str:
        """根據四向度決定詳細程度"""
        d3 = dimensions.get('D3', '粗略')
        d4 = dimensions.get('D4', '正常狀態')
        
        if d3 == '非常詳細':
            return "高：提供詳細解釋、例子和延伸內容"
        elif d4 == '重複狀態':
            return "中高：比之前更深入，提供新的視角"
        else:
            return "中：提供清晰但簡潔的解釋"
    
    def _get_default_strategy(self) -> Dict:
        """獲取默認策略"""
        return {
            "scenario_id": 14,
            "description": "一個 + 無錯誤 + 粗略 + 正常狀態",
            "dimensions": {
                "D1": "一個",
                "D2": "無錯誤",
                "D3": "粗略",
                "D4": "正常狀態"
            },
            "response_style": "簡明式：提供清晰、簡潔的解答",
            "knowledge_integration": "聚焦式：專注於單一知識點的深入講解",
            "error_handling": "直接回答：問題表達正確，直接提供答案",
            "detail_level": "中：提供清晰但簡潔的解釋"
        }
    
    def format_strategy_for_prompt(self, strategy: Dict) -> str:
        """
        將策略格式化為提示詞
        
        Args:
            strategy: 策略配置
            
        Returns:
            str: 格式化的提示詞
        """
        return f"""
【當前情境】第 {strategy['scenario_id']} 種情境
情境描述：{strategy['description']}

【四向度分析】
- D1 (知識點數量): {strategy['dimensions'].get('D1', '未知')}
- D2 (表達錯誤): {strategy['dimensions'].get('D2', '未知')}
- D3 (表達詳細度): {strategy['dimensions'].get('D3', '未知')}
- D4 (重複詢問): {strategy['dimensions'].get('D4', '未知')}

【回應策略】
- 回應風格: {strategy['response_style']}
- 知識整合: {strategy['knowledge_integration']}
- 錯誤處理: {strategy['error_handling']}
- 詳細程度: {strategy['detail_level']}
"""
