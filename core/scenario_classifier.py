"""
情境分類器
使用維度分類器判定 12 種情境
"""
import json
from pathlib import Path
from typing import Dict, Optional, List
from openai import OpenAI
from config import Config, get_shared_client


class ScenarioClassifier:
    """情境分類器 - 判定 12 種情境"""
    
    def __init__(self, scenarios_file: str = None, api_key: str = None):
        """
        初始化分類器
        
        Args:
            scenarios_file: 情境索引文件路徑
            api_key: OpenAI API Key
        """
        # 使用絕對路徑
        if scenarios_file is None:
            base_dir = Path(__file__).parent.parent
            scenarios_file = base_dir / "data" / "scenarios" / "scenarios_12.json"
        
        self.scenarios_file = Path(scenarios_file)
        self.scenarios_data = {}
        self.scenarios_list = []
        
        # 使用共享的 OpenAI client
        self.client = get_shared_client(api_key)
        
        # 載入情境
        self._load_scenarios()
        
        # 載入本體論
        self._load_ontology()
        
        # 載入維度分類器
        from core.dimension_classifier import DimensionClassifier
        self.dimension_classifier = DimensionClassifier(api_key=api_key)
    
    def set_timer(self, timer):
        """設置計時器"""
        self.dimension_classifier.timer = timer
    
    def _load_scenarios(self):
        """載入 12 種情境"""
        try:
            if self.scenarios_file.exists():
                with open(self.scenarios_file, 'r', encoding='utf-8') as f:
                    self.scenarios_data = json.load(f)
                    self.scenarios_list = self.scenarios_data.get('scenarios', [])
                print(f"✅ 已載入 {len(self.scenarios_list)} 種情境")
            else:
                print(f"⚠️  情境文件不存在: {self.scenarios_file}")
        except Exception as e:
            print(f"⚠️  載入情境時發生錯誤: {e}")
    
    def _load_ontology(self):
        """載入本體論內容"""
        try:
            base_dir = Path(__file__).parent.parent
            ontology_file = base_dir / "data" / "ontology" / "knowledge_ontology.txt"
            
            if ontology_file.exists():
                with open(ontology_file, 'r', encoding='utf-8') as f:
                    self.ontology_content = f.read()
                print(f"✅ 已載入知識本體論")
            else:
                self.ontology_content = ""
                print(f"⚠️  本體論文件不存在")
        except Exception as e:
            self.ontology_content = ""
            print(f"⚠️  載入本體論時發生錯誤: {e}")
    
    async def classify(self, query: str) -> Dict:
        """
        判定情境（使用 K, C, R 三個維度）
        
        Args:
            query: 用戶查詢
            
        Returns:
            情境判定結果，包含 scenario_number (1-12)
        """
        try:
            # 使用 DimensionClassifier 進行分類
            result = await self.dimension_classifier.classify_all(query)
            
            # 獲取情境編號
            scenario_id = result['scenario_number']
            
            # 根據情境編號獲取詳細信息
            scenario = self.get_scenario_by_number(scenario_id)
            
            if scenario:
                # 構建返回結果
                return {
                    "scenario_number": scenario_id,
                    "dimensions": {
                        "K": result['K'],
                        "C": result['C'],
                        "R": result['R']
                    },
                    "knowledge_points": result['knowledge_points'],
                    "label": scenario.get('label', ''),
                    "role": scenario.get('role', ''),
                    "prompt": scenario.get('prompt', ''),
                    "display_text": f"情境 {scenario_id}"
                }
            else:
                # 降級處理
                return self._get_default_result()
                
        except Exception as e:
            print(f"❌ 情境判定失敗: {e}")
            import traceback
            traceback.print_exc()
            # 降級處理：返回預設情境
            return self._get_default_result()
    
    def _get_default_result(self) -> Dict:
        """獲取默認結果（情境 5：一個知識點 & 正確 & 正常）"""
        scenario = self.get_scenario_by_number(5) or {}
        return {
            "scenario_number": 5,
            "dimensions": {"K": 1, "C": 0, "R": 0},
            "knowledge_points": [],
            "label": scenario.get('label', '一個知識點 & 正確 & 正常'),
            "role": scenario.get('role', '基礎講解'),
            "prompt": scenario.get('prompt', '你是教學講解者。解釋核心定義與關鍵特點。'),
            "display_text": "情境 5"
        }
    
    def get_scenario_by_number(self, number: int) -> Optional[Dict]:
        """
        根據編號獲取情境
        
        Args:
            number: 情境編號 (1-12)
            
        Returns:
            情境資料
        """
        for scenario in self.scenarios_list:
            if scenario['scenario_number'] == number:
                return scenario
        return None
    
    
    def _format_display_text(self, dimensions: Dict[str, str], scenario_number: int) -> str:
        """格式化顯示文字"""
        return f"情境 {scenario_number}"
    
    def list_all_scenarios(self):
        """列出所有情境"""
        print("\n📚 12 種情境列表")
        for scenario in self.scenarios_list:
            print(f"情境 {scenario['scenario_number']:2d}: {scenario.get('label', '')} - {scenario.get('role', '')}")
        print(f"\n總計: {len(self.scenarios_list)} 種情境")


if __name__ == "__main__":
    # 簡單測試
    classifier = ScenarioClassifier()
    classifier.list_all_scenarios()
