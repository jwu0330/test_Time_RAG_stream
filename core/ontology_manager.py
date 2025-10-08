"""
知識本體論管理器
負責載入和管理知識圖譜，提供延伸學習建議
"""
import os
from typing import Dict, List, Optional
from pathlib import Path


class OntologyManager:
    """知識本體論管理器（簡化版）"""
    
    def __init__(self, ontology_file: str = None):
        """
        初始化本體論管理器
        
        Args:
            ontology_file: 本體論文件路徑
        """
        # 使用絕對路徑
        if ontology_file is None:
            base_dir = Path(__file__).parent.parent
            ontology_file = base_dir / "data" / "ontology" / "knowledge_ontology.txt"
        
        self.ontology_file = Path(ontology_file)
        self.ontology_content: str = ""
        
        # 載入本體論
        self._load_ontology()
    
    def _load_ontology(self):
        """載入本體論文件"""
        try:
            if self.ontology_file.exists():
                with open(self.ontology_file, 'r', encoding='utf-8') as f:
                    self.ontology_content = f.read()
                print(f"✅ 已載入知識本體論")
            else:
                print(f"⚠️  本體論文件不存在: {self.ontology_file}")
        except Exception as e:
            print(f"⚠️  載入本體論時發生錯誤: {e}")
    
    def get_ontology_content(self) -> str:
        """
        獲取完整的本體論內容
        
        Returns:
            本體論文本
        """
        return self.ontology_content
    
    def get_ontology_context_for_prompt(
        self, 
        knowledge_points: List[str]
    ) -> str:
        """
        為提示詞生成本體論上下文（僅在多個知識點時使用）
        
        Args:
            knowledge_points: 涉及的知識點列表
            
        Returns:
            本體論上下文文本
        """
        # 只有多個知識點時才返回本體論
        if len(knowledge_points) <= 1:
            return ""
        
        # 返回完整的本體論內容
        return f"\n【知識點關係】\n{self.ontology_content}"


# 測試函數
def test_ontology_manager():
    """測試本體論管理器"""
    print("🧪 測試知識本體論管理器\n")
    
    manager = OntologyManager()
    
    # 測試 1：獲取完整內容
    print("\n測試 1：獲取本體論內容")
    print("-" * 60)
    content = manager.get_ontology_content()
    print(content[:300] + "...")
    
    # 測試 2：生成提示詞上下文（單一知識點）
    print("\n測試 2：單一知識點（不應返回本體論）")
    print("-" * 60)
    context = manager.get_ontology_context_for_prompt(["ml_basics"])
    print(f"結果: '{context}' (應為空)")
    
    # 測試 3：生成提示詞上下文（多個知識點）
    print("\n測試 3：多個知識點（應返回本體論）")
    print("-" * 60)
    context = manager.get_ontology_context_for_prompt(
        ["ml_basics", "deep_learning"]
    )
    print(context[:300] + "...")


if __name__ == "__main__":
    test_ontology_manager()
