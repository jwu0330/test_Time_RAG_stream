"""
情境判定模組（更新版）
負責分析情境並進行四向度分類 (D1-D4)
基於正確的向度定義和歷史紀錄
"""
import json
import os
from typing import Dict, List, Optional
from openai import OpenAI
from config import Config
from .history_manager import HistoryManager


class DimensionClassifier:
    """四向度分類器"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = None):
        """
        初始化分類器
        
        Args:
            api_key: OpenAI API Key
            model: 使用的模型（默認從配置讀取）
        """
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.model = model or Config.CLASSIFIER_MODEL
        self.history_manager = HistoryManager()
    
    async def classify(
        self, 
        query: str, 
        matched_docs: List[str],
        context: str = ""
    ) -> Dict[str, str]:
        """
        對查詢進行四向度分類
        
        Args:
            query: 用戶查詢
            matched_docs: 匹配的文件列表
            context: RAG 檢索到的上下文
            
        Returns:
            四向度分類結果
        """
        # 提取知識點
        knowledge_points = self._extract_knowledge_points(matched_docs)
        
        # D1: 知識點數量（通過 RAG 匹配判斷）
        d1_value = self._classify_d1(knowledge_points)
        
        # D2: 表達錯誤（由 AI 判斷）
        d2_value = await self._classify_d2(query)
        
        # D3: 表達詳細度（由 AI 判斷）
        d3_value = await self._classify_d3(query)
        
        # D4: 重複詢問（由 AI 分析歷史記錄判斷）
        d4_value = await self._classify_d4(query, knowledge_points)
        
        dimensions = {
            "D1": d1_value,
            "D2": d2_value,
            "D3": d3_value,
            "D4": d4_value
        }
        
        # 記錄到歷史
        self.history_manager.add_query(query, matched_docs, dimensions)
        
        return dimensions
    
    def _extract_knowledge_points(self, matched_docs: List[str]) -> List[str]:
        """提取知識點"""
        knowledge_points = []
        for doc in matched_docs:
            if doc in Config.KNOWLEDGE_POINTS:
                knowledge_points.append(Config.KNOWLEDGE_POINTS[doc])
        return knowledge_points
    
    def _classify_d1(self, knowledge_points: List[str]) -> str:
        """
        D1: 知識點數量
        
        Returns:
            "零個", "一個", 或 "多個"
        """
        count = len(knowledge_points)
        if count == 0:
            return "零個"
        elif count == 1:
            return "一個"
        else:
            return "多個"
    
    async def _classify_d2(self, query: str) -> str:
        """
        D2: 表達錯誤
        
        Returns:
            "有錯誤" 或 "無錯誤"
        """
        prompt = f"""
請判斷以下問題的表達是否有錯誤（語法錯誤、邏輯錯誤、用詞不當等）。

問題：{query}

請只回答「有錯誤」或「無錯誤」，不需要其他說明。
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一個專業的語言分析助手，專門判斷問題表達是否有錯誤。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        
        # 確保返回值符合規範
        if "有錯誤" in result:
            return "有錯誤"
        else:
            return "無錯誤"
    
    async def _classify_d3(self, query: str) -> str:
        """
        D3: 表達詳細度
        
        Returns:
            "非常詳細", "粗略", 或 "未談及重點"
        """
        prompt = f"""
請判斷以下問題的表達詳細程度。

問題：{query}

評判標準：
- 非常詳細：問題描述清楚、具體，包含足夠的上下文和細節
- 粗略：問題表達簡單，缺少具體細節，但方向明確
- 未談及重點：問題表達模糊，不清楚真正想問什麼

請只回答「非常詳細」、「粗略」或「未談及重點」，不需要其他說明。
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一個專業的問題分析助手，專門判斷問題的詳細程度。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=20
        )
        
        result = response.choices[0].message.content.strip()
        
        # 確保返回值符合規範
        if "非常詳細" in result:
            return "非常詳細"
        elif "未談及重點" in result:
            return "未談及重點"
        else:
            return "粗略"
    
    async def _classify_d4(self, query: str, knowledge_points: List[str]) -> str:
        """
        D4: 重複詢問
        通過 AI 分析當前問題和歷史記錄，判斷是否真的在重複詢問
        
        Args:
            query: 當前查詢
            knowledge_points: 當前匹配的知識點
        
        Returns:
            "重複狀態" 或 "正常狀態"
        """
        if not knowledge_points:
            return "正常狀態"
        
        # 獲取歷史記錄
        recent_history = self.history_manager.get_recent_history(n=5)
        
        # 如果歷史記錄少於 3 條，不可能重複
        if len(recent_history) < Config.REPETITION_THRESHOLD:
            return "正常狀態"
        
        # 構建歷史對話上下文
        history_context = self._format_history_for_ai(recent_history)
        
        # 構建提示詞，讓 AI 判斷
        prompt = f"""
請分析用戶是否在重複詢問同一個知識點。

當前問題：
{query}

當前涉及的知識點：
{', '.join(knowledge_points)}

最近的歷史對話記錄：
{history_context}

判斷標準：
- 如果用戶連續多次（3次以上）詢問同一個知識點的相同或相似問題，判定為「重複狀態」
- 如果用戶雖然涉及相同知識點，但問題角度不同、深入程度不同，判定為「正常狀態」
- 如果用戶在不同知識點之間切換，判定為「正常狀態」

請只回答「重複狀態」或「正常狀態」，不需要其他說明。
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一個專業的對話分析助手，專門判斷用戶是否在重複詢問相同問題。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=20
        )
        
        result = response.choices[0].message.content.strip()
        
        # 確保返回值符合規範
        if "重複狀態" in result:
            return "重複狀態"
        else:
            return "正常狀態"
    
    def _format_history_for_ai(self, history: List) -> str:
        """
        格式化歷史記錄供 AI 分析
        
        Args:
            history: 歷史記錄列表
            
        Returns:
            格式化的歷史文本
        """
        if not history:
            return "（無歷史記錄）"
        
        formatted = []
        for i, record in enumerate(history, 1):
            kps = ', '.join(record.knowledge_points) if record.knowledge_points else '無'
            formatted.append(
                f"{i}. 問題：{record.query}\n"
                f"   知識點：{kps}\n"
                f"   時間：{record.timestamp}"
            )
        
        return "\n\n".join(formatted)
    
    def get_dimension_details(self, dimensions: Dict[str, str]) -> Dict[str, dict]:
        """
        獲取向度詳細信息
        
        Args:
            dimensions: 分類結果
            
        Returns:
            包含向度名稱和描述的詳細信息
        """
        details = {}
        for dim_id, value in dimensions.items():
            dim_config = Config.DIMENSIONS[dim_id]
            details[dim_id] = {
                "name": dim_config["name"],
                "description": dim_config["description"],
                "value": value,
                "possible_values": dim_config["values"]
            }
        return details


class ScenarioClassifier:
    """情境分類器（保持向後兼容）"""
    
    def __init__(self, api_key: Optional[str] = None, use_small_model: bool = True):
        """
        初始化情境分類器
        
        Args:
            api_key: OpenAI API Key
            use_small_model: 是否使用小模型（已棄用，從配置讀取）
        """
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.model = Config.CLASSIFIER_MODEL
        self.scenarios: Dict[str, dict] = {}
        self.dimension_classifier = DimensionClassifier(api_key=api_key)
    
    def load_scenarios_from_dir(self, scenarios_dir: str = None):
        """
        從目錄載入所有情境文件
        
        Args:
            scenarios_dir: 情境文件目錄（默認從配置讀取）
        """
        scenarios_dir = scenarios_dir or Config.SCENARIOS_DIR
        
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
    
    async def classify_scenario(
        self, 
        query: str, 
        matched_docs: List[str],
        context: str = ""
    ) -> Dict[str, any]:
        """
        對查詢進行四向度分類
        
        Args:
            query: 用戶查詢
            matched_docs: 匹配的文件列表
            context: 額外上下文
            
        Returns:
            分類結果，包含四向度判定
        """
        # 使用新的分類器
        dimensions = await self.dimension_classifier.classify(query, matched_docs, context)
        
        # 獲取詳細信息
        dimension_details = self.dimension_classifier.get_dimension_details(dimensions)
        
        return {
            "dimensions": dimensions,
            "dimension_details": dimension_details,
            "knowledge_points": self.dimension_classifier._extract_knowledge_points(matched_docs)
        }
    
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
        original_query: str,
        dimensions: Dict[str, str]
    ) -> str:
        """
        創建情境注入提示詞
        
        Args:
            draft_response: 初始草稿回應
            scenario_context: 情境上下文
            original_query: 原始查詢
            dimensions: 四向度分類結果
            
        Returns:
            注入提示詞
        """
        # 根據四向度調整回答風格
        style_guide = self._generate_style_guide(dimensions)
        
        prompt = f"""
你之前生成了一個初步回答的草稿。現在需要根據新的情境信息和用戶特徵來完善這個回答。

原始問題：
{original_query}

初步草稿：
{draft_response}

情境信息：
{scenario_context}

回答風格指引：
{style_guide}

請基於以上信息，完善並輸出最終的完整回答。確保回答：
1. 整合了情境中的關鍵信息
2. 符合用戶的提問特徵
3. 保持連貫性和專業性
4. 直接給出最終答案，不需要重複草稿內容
"""
        return prompt
    
    def _generate_style_guide(self, dimensions: Dict[str, str]) -> str:
        """
        根據四向度生成回答風格指引
        
        Args:
            dimensions: 四向度分類結果
            
        Returns:
            風格指引文本
        """
        guides = []
        
        # D1: 知識點數量
        if dimensions["D1"] == "零個":
            guides.append("- 用戶問題可能偏離主題，需要引導回到相關知識點")
        elif dimensions["D1"] == "一個":
            guides.append("- 專注於單一知識點的深入解釋")
        else:  # 多個
            guides.append("- 需要整合多個知識點，說明它們之間的關聯")
        
        # D2: 表達錯誤
        if dimensions["D2"] == "有錯誤":
            guides.append("- 用戶表達有誤，需要先澄清問題，再給出正確答案")
        else:
            guides.append("- 用戶表達清晰，可以直接回答")
        
        # D3: 表達詳細度
        if dimensions["D3"] == "非常詳細":
            guides.append("- 用戶問題很具體，給出針對性的詳細回答")
        elif dimensions["D3"] == "粗略":
            guides.append("- 用戶問題較籠統，提供全面的概述")
        else:  # 未談及重點
            guides.append("- 用戶問題不明確，需要先確認需求，再提供相關信息")
        
        # D4: 重複詢問
        if dimensions["D4"] == "重複狀態":
            guides.append("- 用戶重複詢問同一主題，可能需要換個角度解釋或提供更多實例")
        else:
            guides.append("- 這是新的問題，按常規方式回答")
        
        return "\n".join(guides)
