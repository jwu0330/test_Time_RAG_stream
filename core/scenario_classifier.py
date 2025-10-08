"""
情境分類器
使用 OpenAI Function Calling 判定 24 種情境
"""
import json
from pathlib import Path
from typing import Dict, Optional, List
from openai import OpenAI


class ScenarioClassifier:
    """情境分類器 - 判定 24 種情境"""
    
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
    
    def classify(self, query: str, history: List[Dict] = None) -> Dict:
        """
        判定情境（使用 OpenAI Function Calling）
        
        Args:
            query: 用戶查詢
            history: 歷史對話記錄
            
        Returns:
            情境判定結果
        """
        # 準備歷史記錄文本
        history_text = ""
        if history:
            history_items = []
            for h in history[-5:]:  # 只取最近5條
                if isinstance(h, dict):
                    query = h.get('query', '')
                    kps = h.get('knowledge_points', [])
                    dims = h.get('dimensions', {})
                    history_items.append(f"Q: {query}\n知識點: {', '.join(kps)}\n向度: {dims}")
                else:
                    # QueryHistory 對象
                    history_items.append(f"Q: {h.query}\n知識點: {', '.join(h.knowledge_points)}\n向度: {h.dimensions}")
            history_text = "\n\n".join(history_items)
        
        # 構建提示詞
        prompt = f"""
請分析以下用戶問題，並判定四個向度：

【知識本體論】
{self.ontology_content}

【歷史對話】
{history_text if history_text else "（無歷史記錄）"}

【當前問題】
{query}

請判定以下四個向度：
1. D1（知識點數量）：這個問題涉及幾個知識點？（零個/一個/多個）
2. D2（表達錯誤）：問題的表達是否有錯誤？（有錯誤/無錯誤）
3. D3（表達詳細度）：問題的表達是否詳細？（粗略/非常詳細）
4. D4（重複詢問）：是否在重複詢問同一知識點？（重複狀態/正常狀態）
"""
        
        # 定義 Function
        functions = [{
            "name": "classify_dimensions",
            "description": "判定用戶問題的四個向度",
            "parameters": {
                "type": "object",
                "properties": {
                    "D1": {
                        "type": "string",
                        "enum": ["零個", "一個", "多個"],
                        "description": "知識點數量"
                    },
                    "D2": {
                        "type": "string",
                        "enum": ["有錯誤", "無錯誤"],
                        "description": "表達是否有錯誤"
                    },
                    "D3": {
                        "type": "string",
                        "enum": ["粗略", "非常詳細"],
                        "description": "表達詳細度"
                    },
                    "D4": {
                        "type": "string",
                        "enum": ["重複狀態", "正常狀態"],
                        "description": "是否重複詢問"
                    }
                },
                "required": ["D1", "D2", "D3", "D4"]
            }
        }]
        
        try:
            # 呼叫 OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一個專業的教育情境分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                functions=functions,
                function_call={"name": "classify_dimensions"},
                temperature=0.3
            )
            
            # 解析 Function Call 結果
            function_call = response.choices[0].message.function_call
            dimensions = json.loads(function_call.arguments)
            
            print(f"✅ API 判定結果：{dimensions}")
            
            # 根據四向度查找對應的情境
            scenario = self.get_scenario_by_dimensions(dimensions)
            
            if scenario:
                result = {
                    "scenario_number": scenario['scenario_number'],
                    "dimensions": dimensions,
                    "description": scenario['description'],
                    "display_text": self._format_display_text(dimensions, scenario['scenario_number'])
                }
                return result
            else:
                return {
                    "scenario_number": 0,
                    "dimensions": dimensions,
                    "description": "未找到對應情境",
                    "display_text": f"無法匹配情境：{dimensions}"
                }
                
        except Exception as e:
            print(f"❌ API 呼叫失敗: {e}")
            # 降級處理：返回預設情境
            return {
                "scenario_number": 0,
                "dimensions": {},
                "description": "API 呼叫失敗",
                "display_text": f"錯誤：{str(e)}"
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
    
    def get_scenario_by_dimensions(self, dimensions: Dict[str, str]) -> Optional[Dict]:
        """
        根據四向度獲取情境
        
        Args:
            dimensions: 四向度字典，例如 {"D1": "一個", "D2": "無錯誤", ...}
            
        Returns:
            情境資料
        """
        for scenario in self.scenarios_list:
            if scenario['dimensions'] == dimensions:
                return scenario
        return None
    
    def _format_display_text(self, dimensions: Dict[str, str], scenario_number: int) -> str:
        """
        格式化顯示文字
        
        Args:
            dimensions: 四向度
            scenario_number: 情境編號
            
        Returns:
            格式化的文字
        """
        d1 = dimensions.get('D1', '未知')
        d2 = dimensions.get('D2', '未知')
        d3 = dimensions.get('D3', '未知')
        d4 = dimensions.get('D4', '未知')
        
        text = f"當前情境：D1={d1}, D2={d2}, D3={d3}, D4={d4} → 第 {scenario_number} 種情境"
        return text
    
    def list_all_scenarios(self):
        """列出所有情境"""
        print("\n" + "="*70)
        print("📚 24 種情境列表")
        print("="*70)
        
        for scenario in self.scenarios_list:
            num = scenario['scenario_number']
            dims = scenario['dimensions']
            print(f"\n情境 {num:2d}: {dims['D1']:4s} + {dims['D2']:6s} + {dims['D3']:8s} + {dims['D4']:8s}")
        
        print("\n" + "="*70)
        print(f"總計: {len(self.scenarios_list)} 種情境")
        print("="*70)


# 測試函數
def test_scenario_classifier():
    """測試情境分類器"""
    print("🧪 測試情境分類器\n")
    
    classifier = ScenarioClassifier()
    
    # 測試 1：列出所有情境
    print("\n測試 1：列出所有情境")
    classifier.list_all_scenarios()
    
    # 測試 2：判定情境（目前返回固定值）
    print("\n測試 2：判定情境")
    print("-" * 70)
    result = classifier.classify("什麼是機器學習？")
    print(f"判定結果：{result['display_text']}")
    print(f"詳細資訊：{result['description']}")
    
    # 測試 3：根據編號獲取情境
    print("\n測試 3：獲取特定情境")
    print("-" * 70)
    for num in [1, 12, 24]:
        scenario = classifier.get_scenario_by_number(num)
        if scenario:
            print(f"情境 {num}: {scenario['description']}")
    
    # 測試 4：根據四向度獲取情境
    print("\n測試 4：根據四向度查找情境")
    print("-" * 70)
    dims = {"D1": "多個", "D2": "無錯誤", "D3": "非常詳細", "D4": "正常狀態"}
    scenario = classifier.get_scenario_by_dimensions(dims)
    if scenario:
        print(f"找到情境 {scenario['scenario_number']}: {scenario['description']}")


if __name__ == "__main__":
    test_scenario_classifier()
