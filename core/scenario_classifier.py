"""
情境分類器
使用 OpenAI Responses API 的 function/tool call 判定 24 種情境
"""
import json
from pathlib import Path
from typing import Dict, Optional, List
from openai import OpenAI
from config import Config


class ScenarioClassifier:
    """情境分類器 - 使用 Responses API 判定 24 種情境"""
    
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
            scenarios_file = base_dir / "data" / "scenarios" / "scenarios_24.json"
        
        self.scenarios_file = Path(scenarios_file)
        self.scenarios_data = {}
        self.scenarios_list = []
        
        # 初始化 OpenAI client
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        
        # 載入情境
        self._load_scenarios()
        
        # 載入本體論
        self._load_ontology()
        
        # 載入四個獨立分類器（稍後會注入 timer）
        from core.dimension_classifiers import DimensionClassifiers
        self.dimension_classifiers = DimensionClassifiers(api_key=api_key)
    
    def set_timer(self, timer):
        """設置計時器"""
        self.dimension_classifiers.timer = timer
    
    def _load_scenarios(self):
        """載入 24 種情境"""
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
    
    async def classify(self, query: str, history: List[Dict] = None, matched_docs: List[str] = None) -> Dict:
        """
        判定情境（使用四個獨立 API 並行判定，精準判定）
        
        Args:
            query: 用戶查詢
            history: 歷史對話記錄
            
        Returns:
            情境判定結果，包含 scenario_number (1-24)
        """
        try:
            print(f"\n🔍 開始四向度並行判定...")
            
            # 使用四個獨立 API 並行判定（返回數字）
            dimensions_num = await self.dimension_classifiers.classify_all_parallel(query, history, matched_docs)
            
            # 數字映射到文字（僅用於顯示）
            d1_map = {0: "零個", 1: "一個", 2: "多個"}
            d2_map = {0: "無錯誤", 1: "有錯誤"}
            d3_map = {0: "粗略", 1: "非常詳細"}
            d4_map = {0: "正常狀態", 1: "重複狀態"}
            
            dimensions_text = {
                "D1": d1_map.get(dimensions_num['D1'], "一個"),
                "D2": d2_map.get(dimensions_num['D2'], "無錯誤"),
                "D3": d3_map.get(dimensions_num['D3'], "粗略"),
                "D4": d4_map.get(dimensions_num['D4'], "正常狀態")
            }
            
            print(f"  D1 (知識點數量): {dimensions_num['D1']} = {dimensions_text['D1']}")
            print(f"  D2 (表達錯誤): {dimensions_num['D2']} = {dimensions_text['D2']}")
            print(f"  D3 (表達詳細度): {dimensions_num['D3']} = {dimensions_text['D3']}")
            print(f"  D4 (重複詢問): {dimensions_num['D4']} = {dimensions_text['D4']}")
            
            # 後端自行計算情境編號（使用數字）
            scenario_id = self.dimension_classifiers.dimensions_to_scenario_number(dimensions_num)
            
            print(f"✅ 計算得出情境編號：{scenario_id}")
            
            # 根據情境編號獲取詳細信息
            scenario = self.get_scenario_by_number(scenario_id)
            
            if scenario:
                result = {
                    "scenario_number": scenario_id,
                    "dimensions": dimensions_text,  # 返回文字版本（用於顯示）
                    "dimensions_num": dimensions_num,  # 返回數字版本（用於計算）
                    "label": scenario.get('label', ''),
                    "role": scenario.get('role', ''),
                    "prompt": scenario.get('prompt', ''),
                    "display_text": self._format_display_text(dimensions_text, scenario_id)
                }
                return result
            else:
                # 降級處理
                return self._get_default_result()
                
        except Exception as e:
            print(f"❌ 四向度判定失敗: {e}")
            import traceback
            traceback.print_exc()
            # 降級處理：返回預設情境
            return self._get_default_result()
    
    def _get_default_result(self) -> Dict:
        """獲取默認結果（情境 14）"""
        scenario = self.get_scenario_by_number(14) or {}
        return {
            "scenario_number": 14,
            "dimensions": {"D1": "一個", "D2": "無錯誤", "D3": "粗略", "D4": "正常狀態"},
            "label": scenario.get('label', '一個知識點&無錯誤&粗略&正常'),
            "role": scenario.get('role', '基礎講解'),
            "prompt": scenario.get('prompt', '你是教學講解者。解釋核心定義與關鍵特點。'),
            "display_text": "情境 14"
        }
    
    def get_scenario_by_number(self, number: int) -> Optional[Dict]:
        """
        根據編號獲取情境
        
        Args:
            number: 情境編號 (1-24)
            
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
        print("\n📚 24 種情境列表")
        for scenario in self.scenarios_list:
            print(f"情境 {scenario['scenario_number']:2d}: {scenario.get('label', '')} - {scenario.get('role', '')}")
        print(f"\n總計: {len(self.scenarios_list)} 種情境")


if __name__ == "__main__":
    # 簡單測試
    classifier = ScenarioClassifier()
    classifier.list_all_scenarios()
