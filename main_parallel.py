"""
主程序 - 並行處理版本
支持多線程並行分析四向度
"""
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from openai import OpenAI

from vector_store import VectorStore
from rag_module import RAGRetriever, RAGCache
from scenario_module import DimensionClassifier
from scenario_matcher import ScenarioMatcher
from timer_utils import Timer
from config import Config


class ParallelRAGSystem:
    """並行處理的 RAG 流式系統"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化系統
        
        Args:
            api_key: OpenAI API Key
        """
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        
        # 初始化各模組
        self.vector_store = VectorStore(api_key=api_key)
        self.rag_retriever = RAGRetriever(self.vector_store)
        self.rag_cache = RAGCache()
        self.dimension_classifier = DimensionClassifier(api_key=api_key)
        self.scenario_matcher = ScenarioMatcher()
        
        # 計時器
        self.timer = Timer()
        
        print("🚀 並行 RAG 流式系統已初始化")
    
    async def initialize_documents(self, docs_dir: str = None):
        """
        初始化文件向量化
        
        Args:
            docs_dir: 文件目錄
        """
        docs_dir = docs_dir or Config.DOCS_DIR
        
        print(f"\n📚 開始向量化文件...")
        self.timer.start_stage("向量化")
        
        # 檢查是否已有向量文件
        if self.vector_store.load():
            self.timer.stop_stage("向量化")
            print("✅ 使用已儲存的向量")
            return
        
        # 讀取並向量化文件
        if not os.path.exists(docs_dir):
            print(f"⚠️  文件目錄不存在: {docs_dir}")
            self.timer.stop_stage("向量化")
            return
        
        documents = []
        for filename in os.listdir(docs_dir):
            filepath = os.path.join(docs_dir, filename)
            if os.path.isfile(filepath) and filename.endswith('.txt'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append({
                        "id": filename,
                        "content": content,
                        "metadata": {"filename": filename}
                    })
                    print(f"  📄 載入: {filename} ({len(content)} 字)")
        
        if documents:
            await self.vector_store.batch_add_documents(documents)
            self.vector_store.save()
            self.vector_store.export_to_json()
        
        self.timer.stop_stage("向量化")
    
    async def rag_retrieval(self, query: str) -> Dict:
        """
        RAG 檢索（線程 1）
        
        Args:
            query: 用戶查詢
            
        Returns:
            檢索結果
        """
        retrieved_docs = await self.rag_retriever.retrieve(query, top_k=3)
        context = self.rag_retriever.format_context(retrieved_docs)
        matched_doc_ids = self.rag_retriever.get_matched_doc_ids(retrieved_docs)
        
        # 提取知識點
        knowledge_points = []
        for doc_id in matched_doc_ids:
            if doc_id in Config.KNOWLEDGE_POINTS:
                knowledge_points.append(Config.KNOWLEDGE_POINTS[doc_id])
        
        return {
            "context": context,
            "matched_docs": matched_doc_ids,
            "knowledge_points": knowledge_points,
            "retrieved_docs": retrieved_docs
        }
    
    async def analyze_d2(self, query: str) -> str:
        """
        D2 分析：表達錯誤（線程 2）
        
        Args:
            query: 用戶查詢
            
        Returns:
            D2 結果
        """
        return await self.dimension_classifier._classify_d2(query)
    
    async def analyze_d3(self, query: str) -> str:
        """
        D3 分析：表達詳細度（線程 3）
        
        Args:
            query: 用戶查詢
            
        Returns:
            D3 結果
        """
        return await self.dimension_classifier._classify_d3(query)
    
    async def analyze_d4(self, query: str, knowledge_points: List[str]) -> str:
        """
        D4 分析：重複詢問（線程 4）
        
        Args:
            query: 用戶查詢
            knowledge_points: 知識點列表
            
        Returns:
            D4 結果
        """
        return await self.dimension_classifier._classify_d4(query, knowledge_points)
    
    def analyze_d1(self, knowledge_points: List[str]) -> str:
        """
        D1 分析：知識點數量（需要 RAG 結果）
        
        Args:
            knowledge_points: 知識點列表
            
        Returns:
            D1 結果
        """
        return self.dimension_classifier._classify_d1(knowledge_points)
    
    async def process_query_parallel(self, query: str) -> Dict:
        """
        並行處理查詢
        
        Args:
            query: 用戶查詢
            
        Returns:
            完整結果
        """
        print("\n" + "="*60)
        print(f"🔍 處理查詢: {query}")
        print("="*60)
        
        # 重置計時器
        self.timer = Timer()
        self.timer.start_stage("總流程")
        
        # ============ 階段 1：並行分析 ============
        print("\n🚀 階段 1：啟動並行分析...")
        self.timer.start_stage("並行分析")
        
        # 啟動並行任務
        # 注意：D2, D3 可以立即開始，D4 需要知識點但可以先準備
        rag_task = self.rag_retrieval(query)
        d2_task = self.analyze_d2(query)
        d3_task = self.analyze_d3(query)
        
        # 等待 RAG 和 D2, D3 完成
        rag_result, d2_result, d3_result = await asyncio.gather(
            rag_task,
            d2_task,
            d3_task
        )
        
        print(f"  ✅ RAG 檢索完成：找到 {len(rag_result['matched_docs'])} 個文件")
        print(f"  ✅ D2 分析完成：{d2_result}")
        print(f"  ✅ D3 分析完成：{d3_result}")
        
        # D1 需要 RAG 結果
        d1_result = self.analyze_d1(rag_result['knowledge_points'])
        print(f"  ✅ D1 分析完成：{d1_result}")
        
        # D4 需要知識點
        d4_result = await self.analyze_d4(query, rag_result['knowledge_points'])
        print(f"  ✅ D4 分析完成：{d4_result}")
        
        self.timer.stop_stage("並行分析")
        
        # ============ 階段 2：情境判定 ============
        print("\n🎯 階段 2：判定情境...")
        self.timer.start_stage("情境判定")
        
        dimensions = {
            "D1": d1_result,
            "D2": d2_result,
            "D3": d3_result,
            "D4": d4_result
        }
        
        scenario = self.scenario_matcher.match_scenario(dimensions)
        
        if scenario:
            scenario_number = scenario['scenario_number']
            print(f"  ✅ 判定為第 {scenario_number} 個情境：{scenario['name']}")
        else:
            print(f"  ⚠️  未找到匹配的情境，使用默認處理")
            scenario = self._get_default_scenario()
            scenario_number = 0
        
        self.timer.stop_stage("情境判定")
        
        # ============ 階段 3：合併到主線程 ============
        print("\n🔗 階段 3：合併數據到主線程...")
        self.timer.start_stage("數據合併")
        
        merged_context = self.merge_to_main_thread(
            rag_result=rag_result,
            dimensions=dimensions,
            scenario_data=scenario,
            query=query
        )
        
        print(f"  ✅ 數據合併完成")
        print(f"     - RAG 上下文：{len(merged_context['rag_context'])} 字")
        print(f"     - 知識點：{', '.join(merged_context['knowledge_points'])}")
        print(f"     - 情境數據：已載入")
        
        self.timer.stop_stage("數據合併")
        
        # ============ 階段 4：主線程處理 ============
        print("\n⚙️  階段 4：主線程處理...")
        self.timer.start_stage("主線程處理")
        
        final_answer = await self.main_thread_process(merged_context)
        
        self.timer.stop_stage("主線程處理")
        
        # 記錄到歷史
        self.dimension_classifier.history_manager.add_query(
            query,
            rag_result['matched_docs'],
            dimensions
        )
        
        self.timer.stop_stage("總流程")
        
        # ============ 返回結果 ============
        result = {
            "query": query,
            "final_answer": final_answer,
            "scenario_number": scenario_number,
            "scenario_name": scenario['name'],
            "dimensions": dimensions,
            "dimension_details": self.dimension_classifier.get_dimension_details(dimensions),
            "matched_docs": rag_result['matched_docs'],
            "knowledge_points": rag_result['knowledge_points'],
            "time_report": self.timer.get_report()
        }
        
        return result
    
    def merge_to_main_thread(
        self,
        rag_result: Dict,
        dimensions: Dict,
        scenario_data: Dict,
        query: str
    ) -> Dict:
        """
        將所有數據合併到主線程
        
        Args:
            rag_result: RAG 檢索結果
            dimensions: 四向度分析結果
            scenario_data: 情境 JSON 數據
            query: 用戶問題
            
        Returns:
            合併後的上下文
        """
        merged = {
            "query": query,
            "rag_context": rag_result['context'],
            "knowledge_points": rag_result['knowledge_points'],
            "matched_docs": rag_result['matched_docs'],
            "dimensions": dimensions,
            "scenario": scenario_data,
            "response_strategy": scenario_data.get('response_strategy', {}),
            "prompt_template": scenario_data.get('prompt_template', ''),
            "timestamp": datetime.now().isoformat()
        }
        
        # 如果涉及多個知識點，添加關聯信息
        if dimensions['D1'] == "多個":
            relations = self.scenario_matcher._get_knowledge_relations_text(
                rag_result['knowledge_points']
            )
            merged['knowledge_relations'] = relations
        
        return merged
    
    async def main_thread_process(self, context: Dict) -> str:
        """
        主線程處理
        
        Args:
            context: 合併後的完整上下文
            
        Returns:
            最終答案
        """
        # 構建提示詞
        prompt = self.build_prompt_from_context(context)
        
        # 調用 LLM 生成
        print("\n💬 生成最終答案...")
        print("-" * 50)
        
        response = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是一個專業的知識助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=Config.LLM_TEMPERATURE,
            max_tokens=Config.LLM_FINAL_MAX_TOKENS,
            stream=True
        )
        
        final_answer = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                final_answer += content
        
        print("\n" + "-" * 50)
        
        return final_answer
    
    def build_prompt_from_context(self, context: Dict) -> str:
        """
        根據合併的上下文構建提示詞
        
        Args:
            context: 完整上下文
            
        Returns:
            提示詞
        """
        scenario = context['scenario']
        strategy = context.get('response_strategy', {})
        
        prompt_parts = []
        
        # 情境信息
        prompt_parts.append(f"【情境】第 {scenario.get('scenario_number', 0)} 個情境")
        prompt_parts.append(f"情境名稱：{scenario.get('name', '未知')}")
        prompt_parts.append(f"情境描述：{scenario.get('description', '')}")
        
        # 回答策略
        if strategy:
            prompt_parts.append(f"\n【回答策略】")
            prompt_parts.append(f"語氣：{strategy.get('tone', '友好、專業')}")
            prompt_parts.append(f"長度：{strategy.get('length', '適中')}")
            if 'structure' in strategy:
                prompt_parts.append(f"結構要點：{', '.join(strategy['structure'])}")
            if 'emphasis' in strategy:
                prompt_parts.append(f"強調重點：{', '.join(strategy['emphasis'])}")
        
        # RAG 檢索內容
        prompt_parts.append(f"\n【檢索到的教材內容】")
        prompt_parts.append(context['rag_context'])
        
        # 知識點關聯
        if 'knowledge_relations' in context:
            prompt_parts.append(f"\n【知識點關聯】")
            prompt_parts.append(context['knowledge_relations'])
        
        # 用戶問題
        prompt_parts.append(f"\n【用戶問題】")
        prompt_parts.append(context['query'])
        
        # 情境的提示詞模板
        if context.get('prompt_template'):
            prompt_parts.append(f"\n【具體指引】")
            prompt_parts.append(context['prompt_template'])
        
        prompt_parts.append("\n請根據以上情境和內容，生成適當的回答：")
        
        return "\n".join(prompt_parts)
    
    def _get_default_scenario(self) -> Dict:
        """獲取默認情境"""
        return {
            "id": "default",
            "scenario_number": 0,
            "name": "默認情境",
            "description": "未匹配到特定情境，使用默認處理",
            "response_strategy": {
                "tone": "友好、專業",
                "structure": ["直接回答問題"],
                "emphasis": ["提供準確信息"],
                "length": "適中"
            }
        }
    
    def print_summary(self, result: Dict):
        """打印結果摘要"""
        print("\n" + "="*60)
        print("📊 處理結果摘要")
        print("="*60)
        print(f"查詢：{result['query']}")
        print(f"\n情境：第 {result['scenario_number']} 個 - {result['scenario_name']}")
        print(f"\n四向度：")
        for dim, value in result['dimensions'].items():
            detail = result['dimension_details'][dim]
            print(f"  {dim} ({detail['name']}): {value}")
        print(f"\n知識點：{', '.join(result['knowledge_points']) if result['knowledge_points'] else '無'}")
        print(f"\n時間報告：")
        for stage, duration in result['time_report']['stages'].items():
            print(f"  {stage}: {duration:.3f}s")
        print(f"  總計: {result['time_report']['total_time']:.3f}s")
        print("="*60)


async def main():
    """主函數"""
    print("\n" + "="*60)
    print("🚀 並行 RAG 流式系統")
    print("="*60)
    
    # 初始化系統
    system = ParallelRAGSystem()
    
    # 初始化文件
    await system.initialize_documents()
    
    # 測試查詢
    test_queries = [
        "什麼是機器學習？",
        "機器學習和深度學習有什麼區別？請詳細說明。",
    ]
    
    for query in test_queries:
        result = await system.process_query_parallel(query)
        system.print_summary(result)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
