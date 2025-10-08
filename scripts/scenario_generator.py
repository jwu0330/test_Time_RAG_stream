"""
情境生成器
自動生成 24 種情境組合（方案 A）
"""
import json
import os
import sys
from typing import Dict, List

# 添加父目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config


class ScenarioGenerator:
    """24 種情境組合生成器"""
    
    def __init__(self):
        """初始化生成器"""
        # 四向度的所有可能值
        self.dimension_values = {
            "D1": ["零個", "一個", "多個"],
            "D2": ["有錯誤", "無錯誤"],
            "D3": ["非常詳細", "粗略", "未談及重點"],
            "D4": ["重複狀態", "正常狀態"]
        }
        
        # 載入知識點關聯
        self.knowledge_relations = self._load_knowledge_relations()
    
    def _load_knowledge_relations(self) -> dict:
        """載入知識點關聯關係"""
        relations_file = "knowledge_relations.json"
        if os.path.exists(relations_file):
            with open(relations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_all_scenarios(self) -> List[Dict]:
        """
        生成所有 24 種情境組合
        
        Returns:
            情境列表
        """
        scenarios = []
        scenario_id = 1
        
        # 遍歷所有組合
        for d1 in self.dimension_values["D1"]:
            for d2 in self.dimension_values["D2"]:
                for d3 in self.dimension_values["D3"]:
                    for d4 in self.dimension_values["D4"]:
                        scenario = self._create_scenario(
                            scenario_id, d1, d2, d3, d4
                        )
                        scenarios.append(scenario)
                        scenario_id += 1
        
        return scenarios
    
    def _create_scenario(
        self, 
        scenario_id: int,
        d1: str, 
        d2: str, 
        d3: str, 
        d4: str
    ) -> Dict:
        """
        創建單個情境
        
        Args:
            scenario_id: 情境編號
            d1-d4: 四個向度的值
            
        Returns:
            情境字典
        """
        # 生成情境名稱
        name = f"{d1}+{d2}+{d3}+{d4}"
        
        # 生成情境描述
        description = self._generate_description(d1, d2, d3, d4)
        
        # 生成回答策略
        response_strategy = self._generate_response_strategy(d1, d2, d3, d4)
        
        # 生成提示詞模板
        prompt_template = self._generate_prompt_template(d1, d2, d3, d4)
        
        scenario = {
            "id": f"scenario_{scenario_id:02d}",
            "scenario_number": scenario_id,
            "name": name,
            "dimensions": {
                "D1": d1,
                "D2": d2,
                "D3": d3,
                "D4": d4
            },
            "description": description,
            "response_strategy": response_strategy,
            "prompt_template": prompt_template,
            "metadata": {
                "created_by": "auto_generator",
                "version": "1.0"
            }
        }
        
        return scenario
    
    def _generate_description(self, d1: str, d2: str, d3: str, d4: str) -> str:
        """生成情境描述"""
        parts = []
        
        # D1 描述
        if d1 == "零個":
            parts.append("用戶問題未匹配到知識點")
        elif d1 == "一個":
            parts.append("用戶問題涉及單一知識點")
        else:
            parts.append("用戶問題涉及多個知識點")
        
        # D2 描述
        if d2 == "有錯誤":
            parts.append("問題表達存在錯誤")
        else:
            parts.append("問題表達正確")
        
        # D3 描述
        if d3 == "非常詳細":
            parts.append("問題描述非常詳細")
        elif d3 == "粗略":
            parts.append("問題描述較為粗略")
        else:
            parts.append("問題未談及重點")
        
        # D4 描述
        if d4 == "重複狀態":
            parts.append("用戶重複詢問相同內容")
        else:
            parts.append("這是新的問題")
        
        return "，".join(parts) + "。"
    
    def _generate_response_strategy(
        self, 
        d1: str, 
        d2: str, 
        d3: str, 
        d4: str
    ) -> Dict:
        """生成回答策略"""
        strategy = {
            "tone": "友好、專業",
            "structure": [],
            "emphasis": [],
            "length": "適中"
        }
        
        # 根據 D1 調整策略
        if d1 == "零個":
            strategy["structure"].append("引導用戶回到相關主題")
            strategy["emphasis"].append("說明當前問題可能超出知識庫範圍")
        elif d1 == "一個":
            strategy["structure"].append("專注於單一知識點的深入解釋")
            strategy["emphasis"].append("提供該知識點的核心概念和應用")
        else:  # 多個
            strategy["structure"].append("說明多個知識點之間的關聯")
            strategy["emphasis"].append("整合不同知識點，展示完整圖景")
        
        # 根據 D2 調整策略
        if d2 == "有錯誤":
            strategy["structure"].insert(0, "先澄清問題中的錯誤")
            strategy["emphasis"].append("溫和地指出錯誤並給出正確表達")
            strategy["tone"] = "耐心、引導性"
        
        # 根據 D3 調整策略
        if d3 == "非常詳細":
            strategy["structure"].append("針對具體問題給出詳細回答")
            strategy["length"] = "詳細"
        elif d3 == "粗略":
            strategy["structure"].append("提供全面的概述")
            strategy["length"] = "適中"
        else:  # 未談及重點
            strategy["structure"].insert(0, "先確認用戶的真實需求")
            strategy["emphasis"].append("提供相關的背景信息")
        
        # 根據 D4 調整策略
        if d4 == "重複狀態":
            strategy["structure"].append("換個角度或方式解釋")
            strategy["emphasis"].append("提供更多實例或不同視角")
            strategy["tone"] = "耐心、變換方式"
        
        return strategy
    
    def _generate_prompt_template(
        self, 
        d1: str, 
        d2: str, 
        d3: str, 
        d4: str
    ) -> str:
        """生成提示詞模板"""
        template_parts = []
        
        # 基礎指示
        template_parts.append("你是一個專業的知識助手。請根據以下情境回答用戶的問題：\n")
        
        # D1 相關指示
        if d1 == "零個":
            template_parts.append("【知識點匹配】用戶的問題沒有匹配到知識庫中的內容。")
            template_parts.append("請禮貌地說明這個問題可能超出當前知識庫的範圍，並嘗試引導用戶提出相關問題。\n")
        elif d1 == "一個":
            template_parts.append("【知識點匹配】用戶的問題涉及單一知識點：{knowledge_points}")
            template_parts.append("請專注於這個知識點進行深入解釋。\n")
        else:  # 多個
            template_parts.append("【知識點匹配】用戶的問題涉及多個知識點：{knowledge_points}")
            template_parts.append("請說明這些知識點之間的關聯關係：")
            template_parts.append("{knowledge_relations}\n")
        
        # D2 相關指示
        if d2 == "有錯誤":
            template_parts.append("【表達問題】用戶的問題表達存在錯誤。")
            template_parts.append("請先溫和地指出錯誤所在，給出正確的表達方式，然後再回答問題。\n")
        else:
            template_parts.append("【表達問題】用戶的問題表達正確，可以直接回答。\n")
        
        # D3 相關指示
        if d3 == "非常詳細":
            template_parts.append("【問題詳細度】用戶的問題非常具體詳細。")
            template_parts.append("請針對用戶的具體問題給出詳細、深入的回答。\n")
        elif d3 == "粗略":
            template_parts.append("【問題詳細度】用戶的問題較為籠統。")
            template_parts.append("請提供全面的概述，涵蓋該主題的主要方面。\n")
        else:  # 未談及重點
            template_parts.append("【問題詳細度】用戶的問題不夠明確。")
            template_parts.append("請先確認用戶的真實需求，然後提供相關的背景信息和指引。\n")
        
        # D4 相關指示
        if d4 == "重複狀態":
            template_parts.append("【重複詢問】用戶正在重複詢問類似的問題。")
            template_parts.append("請換一個角度或方式來解釋，提供更多實例或不同的視角，幫助用戶更好地理解。\n")
        else:
            template_parts.append("【重複詢問】這是用戶的新問題，按常規方式回答即可。\n")
        
        # 添加上下文和問題
        template_parts.append("\n【檢索到的相關內容】\n{context}\n")
        template_parts.append("\n【用戶問題】\n{query}\n")
        template_parts.append("\n請根據以上情境和內容，給出適當的回答：")
        
        return "\n".join(template_parts)
    
    def save_scenarios(self, output_dir: str = "scenarios_24"):
        """
        保存所有情境到文件
        
        Args:
            output_dir: 輸出目錄
        """
        # 創建目錄
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成所有情境
        scenarios = self.generate_all_scenarios()
        
        # 保存每個情境
        for scenario in scenarios:
            filename = f"{scenario['id']}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(scenario, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 已生成: {filename} - {scenario['name']}")
        
        # 保存索引文件
        index = {
            "total_scenarios": len(scenarios),
            "scenarios": [
                {
                    "id": s["id"],
                    "number": s["scenario_number"],
                    "name": s["name"],
                    "dimensions": s["dimensions"]
                }
                for s in scenarios
            ]
        }
        
        index_file = os.path.join(output_dir, "index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 共生成 {len(scenarios)} 個情境")
        print(f"✅ 索引文件: {index_file}")
        
        return scenarios
    
    def print_scenario_summary(self):
        """打印情境組合摘要"""
        print("\n" + "="*60)
        print("📊 24 種情境組合摘要")
        print("="*60)
        
        scenarios = self.generate_all_scenarios()
        
        for scenario in scenarios:
            print(f"\n{scenario['scenario_number']:2d}. {scenario['id']}")
            print(f"    名稱: {scenario['name']}")
            print(f"    描述: {scenario['description']}")
        
        print("\n" + "="*60)
        print(f"總計: {len(scenarios)} 種情境")
        print("="*60)


def main():
    """主函數"""
    print("🚀 情境生成器")
    print("="*60)
    
    generator = ScenarioGenerator()
    
    # 打印摘要
    generator.print_scenario_summary()
    
    # 生成並保存情境
    print("\n開始生成情境文件...")
    scenarios = generator.save_scenarios()
    
    print("\n✅ 完成！")
    print(f"情境文件已保存到: scenarios_24/")
    print(f"您可以編輯這些文件，擴展提示詞內容到約 5000 字。")


if __name__ == "__main__":
    main()
