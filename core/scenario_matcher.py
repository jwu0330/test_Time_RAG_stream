"""
情境匹配器
快速匹配四向度組合並調用對應的情境
"""
import json
import os
from typing import Dict, Optional, List


class ScenarioMatcher:
    """情境匹配器 - 根據四向度快速找到對應情境"""
    
    def __init__(self, scenarios_dir: str = "data/scenarios"):
        """
        初始化匹配器
        
        Args:
            scenarios_dir: 情境文件目錄
        """
        self.scenarios_dir = scenarios_dir
        self.scenarios = {}
        self.scenario_index = {}
        self.knowledge_relations = {}
        
        # 載入情境
        self._load_scenarios()
        
        # 載入知識點關聯
        self._load_knowledge_relations()
    
    def _load_scenarios(self):
        """載入所有情境文件"""
        if not os.path.exists(self.scenarios_dir):
            print(f"⚠️  情境目錄不存在: {self.scenarios_dir}")
            return
        
        # 載入索引
        index_file = os.path.join(self.scenarios_dir, "index.json")
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                print(f"✅ 載入情境索引: {index_data['total_scenarios']} 個情境")
        
        # 載入所有情境文件
        for filename in os.listdir(self.scenarios_dir):
            if filename.endswith('.json') and filename != 'index.json':
                filepath = os.path.join(self.scenarios_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    scenario = json.load(f)
                    scenario_id = scenario['id']
                    self.scenarios[scenario_id] = scenario
                    
                    # 建立維度索引（用於快速查找）
                    dims = scenario['dimensions']
                    key = self._make_dimension_key(
                        dims['D1'], dims['D2'], dims['D3'], dims['D4']
                    )
                    self.scenario_index[key] = scenario_id
        
        print(f"✅ 已載入 {len(self.scenarios)} 個情境")
    
    def _load_knowledge_relations(self):
        """載入知識點關聯關係"""
        relations_file = "knowledge_relations.json"
        if os.path.exists(relations_file):
            with open(relations_file, 'r', encoding='utf-8') as f:
                self.knowledge_relations = json.load(f)
            print(f"✅ 已載入知識點關聯關係")
    
    def _make_dimension_key(self, d1: str, d2: str, d3: str, d4: str) -> str:
        """
        創建維度組合的鍵
        
        Args:
            d1-d4: 四個向度的值
            
        Returns:
            組合鍵
        """
        return f"{d1}|{d2}|{d3}|{d4}"
    
    def match_scenario(self, dimensions: Dict[str, str]) -> Optional[Dict]:
        """
        根據四向度匹配情境
        
        Args:
            dimensions: 四向度字典，例如 {"D1": "一個", "D2": "無錯誤", ...}
            
        Returns:
            匹配的情境，如果沒有匹配則返回 None
        """
        key = self._make_dimension_key(
            dimensions['D1'],
            dimensions['D2'],
            dimensions['D3'],
            dimensions['D4']
        )
        
        scenario_id = self.scenario_index.get(key)
        if scenario_id:
            return self.scenarios[scenario_id]
        
        return None
    
    def get_scenario_by_number(self, number: int) -> Optional[Dict]:
        """
        根據情境編號獲取情境
        
        Args:
            number: 情境編號（1-24）
            
        Returns:
            情境字典
        """
        scenario_id = f"scenario_{number:02d}"
        return self.scenarios.get(scenario_id)
    
    def get_prompt(
        self, 
        dimensions: Dict[str, str],
        query: str,
        context: str,
        knowledge_points: List[str]
    ) -> str:
        """
        獲取完整的提示詞
        
        Args:
            dimensions: 四向度
            query: 用戶問題
            context: RAG 檢索到的上下文
            knowledge_points: 知識點列表
            
        Returns:
            完整的提示詞
        """
        # 匹配情境
        scenario = self.match_scenario(dimensions)
        
        if not scenario:
            print(f"⚠️  未找到匹配的情境: {dimensions}")
            return self._get_default_prompt(query, context)
        
        # 獲取提示詞模板
        template = scenario['prompt_template']
        
        # 準備知識點關聯信息
        knowledge_relations_text = self._get_knowledge_relations_text(knowledge_points)
        
        # 填充模板
        prompt = template.format(
            query=query,
            context=context,
            knowledge_points=', '.join(knowledge_points) if knowledge_points else '無',
            knowledge_relations=knowledge_relations_text
        )
        
        return prompt
    
    def _get_knowledge_relations_text(self, knowledge_points: List[str]) -> str:
        """
        獲取知識點關聯關係的文本描述
        
        Args:
            knowledge_points: 知識點列表
            
        Returns:
            關聯關係文本
        """
        if not knowledge_points or len(knowledge_points) <= 1:
            return "（單一知識點，無需說明關聯）"
        
        # 映射知識點名稱到 ID
        kp_map = {
            "機器學習基礎": "ml_basics",
            "深度學習": "deep_learning",
            "自然語言處理": "nlp"
        }
        
        kp_ids = [kp_map.get(kp, kp) for kp in knowledge_points]
        
        # 如果是三個知識點
        if len(kp_ids) == 3:
            all_three = self.knowledge_relations.get('relations', {}).get('all_three', {})
            if all_three:
                return self._format_relation(all_three)
        
        # 如果是兩個知識點
        if len(kp_ids) == 2:
            relation_key = f"{kp_ids[0]}_to_{kp_ids[1]}"
            relation = self.knowledge_relations.get('relations', {}).get(relation_key)
            
            if not relation:
                # 嘗試反向
                relation_key = f"{kp_ids[1]}_to_{kp_ids[0]}"
                relation = self.knowledge_relations.get('relations', {}).get(relation_key)
            
            if relation:
                return self._format_relation(relation)
        
        return "（請說明這些知識點之間的關聯）"
    
    def _format_relation(self, relation: Dict) -> str:
        """格式化關聯關係"""
        parts = []
        
        if 'description' in relation:
            parts.append(f"關係概述：{relation['description']}")
        
        if 'key_connections' in relation:
            parts.append("\n關鍵聯繫：")
            for i, conn in enumerate(relation['key_connections'], 1):
                parts.append(f"{i}. {conn}")
        
        if 'differences' in relation:
            parts.append("\n主要區別：")
            for i, diff in enumerate(relation['differences'], 1):
                parts.append(f"{i}. {diff}")
        
        if 'learning_path' in relation:
            parts.append("\n學習路徑：")
            for step in relation['learning_path']:
                parts.append(f"  {step}")
        
        return "\n".join(parts)
    
    def _get_default_prompt(self, query: str, context: str) -> str:
        """獲取默認提示詞"""
        return f"""
你是一個專業的知識助手。

【檢索到的相關內容】
{context}

【用戶問題】
{query}

請根據以上內容回答用戶的問題。
"""
    
    def print_scenario_info(self, dimensions: Dict[str, str]):
        """
        打印情境信息
        
        Args:
            dimensions: 四向度
        """
        scenario = self.match_scenario(dimensions)
        
        if not scenario:
            print("❌ 未找到匹配的情境")
            return
        
        print("\n" + "="*60)
        print(f"📋 情境信息")
        print("="*60)
        print(f"編號: {scenario['scenario_number']}")
        print(f"ID: {scenario['id']}")
        print(f"名稱: {scenario['name']}")
        print(f"\n描述: {scenario['description']}")
        print(f"\n四向度:")
        for dim, value in scenario['dimensions'].items():
            print(f"  {dim}: {value}")
        print(f"\n回答策略:")
        strategy = scenario['response_strategy']
        print(f"  語氣: {strategy['tone']}")
        print(f"  長度: {strategy['length']}")
        print(f"  結構:")
        for item in strategy['structure']:
            print(f"    - {item}")
        print(f"  重點:")
        for item in strategy['emphasis']:
            print(f"    - {item}")
        print("="*60)
    
    def list_all_scenarios(self):
        """列出所有情境"""
        print("\n" + "="*60)
        print("📚 所有情境列表")
        print("="*60)
        
        scenarios = sorted(self.scenarios.values(), key=lambda x: x['scenario_number'])
        
        for scenario in scenarios:
            print(f"\n{scenario['scenario_number']:2d}. {scenario['id']}")
            print(f"    {scenario['name']}")
            dims = scenario['dimensions']
            print(f"    D1={dims['D1']}, D2={dims['D2']}, D3={dims['D3']}, D4={dims['D4']}")
        
        print("\n" + "="*60)
        print(f"總計: {len(scenarios)} 個情境")
        print("="*60)


def test_matcher():
    """測試匹配器"""
    print("🧪 測試情境匹配器\n")
    
    matcher = ScenarioMatcher()
    
    # 測試案例
    test_cases = [
        {
            "name": "案例 1：單一知識點，無錯誤，粗略，正常",
            "dimensions": {
                "D1": "一個",
                "D2": "無錯誤",
                "D3": "粗略",
                "D4": "正常狀態"
            }
        },
        {
            "name": "案例 2：多個知識點，無錯誤，非常詳細，正常",
            "dimensions": {
                "D1": "多個",
                "D2": "無錯誤",
                "D3": "非常詳細",
                "D4": "正常狀態"
            }
        },
        {
            "name": "案例 3：一個知識點，有錯誤，粗略，重複",
            "dimensions": {
                "D1": "一個",
                "D2": "有錯誤",
                "D3": "粗略",
                "D4": "重複狀態"
            }
        }
    ]
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"測試: {test['name']}")
        print(f"{'='*60}")
        
        scenario = matcher.match_scenario(test['dimensions'])
        
        if scenario:
            print(f"✅ 匹配成功！")
            print(f"情境編號: {scenario['scenario_number']}")
            print(f"情境 ID: {scenario['id']}")
            print(f"情境名稱: {scenario['name']}")
        else:
            print(f"❌ 匹配失敗")
    
    # 測試獲取提示詞
    print(f"\n{'='*60}")
    print("測試: 獲取完整提示詞")
    print(f"{'='*60}")
    
    prompt = matcher.get_prompt(
        dimensions={"D1": "多個", "D2": "無錯誤", "D3": "非常詳細", "D4": "正常狀態"},
        query="機器學習和深度學習有什麼區別？",
        context="[RAG 檢索到的內容...]",
        knowledge_points=["機器學習基礎", "深度學習"]
    )
    
    print("\n生成的提示詞:")
    print("-"*60)
    print(prompt)
    print("-"*60)


if __name__ == "__main__":
    test_matcher()
