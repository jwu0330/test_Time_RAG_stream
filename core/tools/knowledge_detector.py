"""
知識點檢測工具
使用 OpenAI API 檢測問題涉及的知識點，返回知識點名稱列表
"""
from openai import OpenAI
from typing import List
import json
import os
from config import get_shared_client


class KnowledgeDetector:
    """知識點檢測器"""
    
    def __init__(self, api_key: str = None, timer=None, ontology_content: str = None):
        """
        初始化知識點檢測器
        
        Args:
            api_key: OpenAI API Key
            timer: 計時器（可選）
            ontology_content: 知識本體論內容（包含所有知識點）
        """
        # 使用共享的 OpenAI client
        self.client = get_shared_client(api_key)
        self.timer = timer
        self.ontology_content = ontology_content
        
        # 知識點列表（從 JSON 清單載入）
        self.knowledge_points = self._load_points_from_json()
    
    def _load_points_from_json(self) -> List[str]:
        """從 data/knowledge_points.json 載入知識點清單（中文名稱）"""
        try:
            # 使用相對路徑，與 Config.DOCS_DIR 一致
            json_path = 'data/knowledge_points.json'
            
            # 如果相對路徑不存在，嘗試絕對路徑
            if not os.path.exists(json_path):
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                json_path = os.path.join(base_dir, 'data', 'knowledge_points.json')
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            nodes = data.get('nodes', [])
            # 僅保留非空字串
            valid_nodes = [str(n).strip() for n in nodes if isinstance(n, str) and str(n).strip()]
            print(f"✅ 知識點檢測器：成功載入 {len(valid_nodes)} 個知識點")
            return valid_nodes
        except Exception as e:
            print(f"⚠️  無法載入 knowledge_points.json，改用空清單: {e}")
            return []
    
    async def detect(self, query: str) -> List[str]:
        """
        檢測問題涉及的知識點
        
        Args:
            query: 用戶問題
            
        Returns:
            List[str]: 知識點名稱列表，例如 ["機器學習基礎", "深度學習"]
        """
        import time
        t_start = time.perf_counter()
        
        # 構建知識點列表字串
        knowledge_list = "\n".join([f"- {kp}" for kp in self.knowledge_points])
        
        # 優化提示詞：語義相似度匹配（80%以上）
        prompt = f"""問題：「{query}」

知識點列表：
{knowledge_list}

任務：分析問題涉及哪些知識點。

匹配規則：
1. 直接匹配：問題中明確提到知識點名稱（如「IPv4」、「DNS」）
2. 語義匹配：問題明顯討論某個知識點的內容，相似度 ≥ 80%
   - 例如：「IP 位址有哪些版本？」→ 匹配「IPv4」和「IPv6」
   - 例如：「網域名稱如何解析？」→ 匹配「DNS」
3. 只返回高度相關的知識點，不要過度推測
4. 若無明確相關知識點，返回空陣列

請返回所有相關的知識點名稱。"""
        
        # 定義 Function Call
        functions = [
            {
                "name": "return_knowledge_points",
                "description": "返回這句話直接涉及的知識點，如果不涉及任何知識點則返回空列表",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "knowledge_points": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "知識點名稱列表，例如 ['機器學習基礎']，如果不涉及則為空列表 []"
                        }
                    },
                    "required": ["knowledge_points"]
                }
            }
        ]
        
        # 調用 API（添加日誌）
        print(f"🔍 知識點檢測：開始分析查詢...")
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是知識點分析專家。根據問題內容，識別涉及的知識點。支援直接匹配和語義匹配（相似度≥80%）。"},
                {"role": "user", "content": prompt}
            ],
            functions=functions,
            function_call={"name": "return_knowledge_points"},
            temperature=0,
            max_tokens=300  # 增加到 300 避免截斷
        )
        
        t_end = time.perf_counter()
        self._last_timing = t_end - t_start
        
        # 解析結果（健壯處理 + 詳細日誌）
        function_call = response.choices[0].message.function_call
        if not function_call:
            print(f"⚠️  知識點檢測：API 未返回 function_call")
            return []

        raw_args = function_call.arguments or ""
        print(f"📥 知識點檢測：API 回應長度 {len(raw_args)} 字元")
        
        try:
            arguments = json.loads(raw_args)
        except Exception as e:
            # 嘗試簡單修復：截斷到最後一個 '}'
            print(f"⚠️  知識點檢測：JSON 解析失敗，嘗試修復...")
            try:
                if isinstance(raw_args, str) and '}' in raw_args:
                    fixed = raw_args[: raw_args.rfind('}') + 1]
                    arguments = json.loads(fixed)
                    print(f"✅ 知識點檢測：JSON 修復成功")
                else:
                    print(f"❌ 知識點檢測：無法修復 JSON（長度 {len(raw_args)}）")
                    print(f"   原始內容: {raw_args[:200]}...")
                    return []
            except Exception as e2:
                print(f"❌ 知識點檢測：JSON 修復失敗 - {e2}")
                return []

        knowledge_points = arguments.get("knowledge_points", [])
        print(f"🎯 知識點檢測：API 返回 {len(knowledge_points)} 個知識點: {knowledge_points}")
        
        # 驗證返回的知識點是否在清單中
        valid_points = [kp for kp in knowledge_points if kp in self.knowledge_points]
        invalid_points = [kp for kp in knowledge_points if kp not in self.knowledge_points]
        
        if invalid_points:
            print(f"⚠️  知識點檢測：過濾掉 {len(invalid_points)} 個無效知識點: {invalid_points}")
        
        print(f"✅ 知識點檢測：最終返回 {len(valid_points)} 個有效知識點: {valid_points}")
        print(f"⏱️  知識點檢測耗時: {self._last_timing:.3f} 秒")
        
        return valid_points
    
    def calculate_k_value(self, knowledge_points: List[str]) -> int:
        """
        從知識點列表計算 K 值
        
        Args:
            knowledge_points: 知識點名稱列表
            
        Returns:
            int: K 值（0=零個, 1=一個, 2=多個）
        """
        count = len(knowledge_points)
        
        if count == 0:
            return 0  # 零個知識點
        elif count == 1:
            return 1  # 一個知識點
        else:
            return 2  # 多個知識點
