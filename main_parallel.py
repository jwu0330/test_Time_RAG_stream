"""
主程序 - 雙線程版本
實現主線（RAG教材生成）和分支（情境判定）並行處理
"""
import asyncio
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from openai import OpenAI

from core.vector_store import VectorStore
from core.rag_module import RAGRetriever, RAGCache
from core.scenario_classifier import ScenarioClassifier
from core.ontology_manager import OntologyManager
from core.history_manager import HistoryManager
from core.timer_utils import Timer
from config import Config


class ParallelRAGSystem:
    """雙線程並行處理的 RAG 系統"""
    
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
        self.scenario_classifier = ScenarioClassifier(api_key=api_key)
        self.ontology_manager = OntologyManager()
        self.history_manager = HistoryManager()
        
        # 計時器
        self.timer = Timer()
        
        print("🚀 雙線程 RAG 系統已初始化")
    
    async def initialize_documents(self, docs_dir: str = None):
        """
        初始化文件向量化
        
        Args:
            docs_dir: 文件目錄
        """
        docs_dir = docs_dir or Config.DOCS_DIR
        
        print(f"\n📚 初始化文件向量...")
        self.timer.start_stage("向量化")
        
        # 檢查是否已有向量文件
        if self.vector_store.load():
            self.timer.stop_stage("向量化")
            print("✅ 使用已儲存的向量（快速啟動）")
            return
        
        # 第一次啟動，需要向量化
        print("⚠️  首次啟動，需要調用 OpenAI API 生成向量")
        print("⏳ 預計需要 10-15 秒，請稍候...")
        
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
    
    async def main_thread_rag(self, query: str) -> Dict:
        """
        主線：RAG 檢索 + 教材生成
        
        Args:
            query: 用戶查詢
            
        Returns:
            RAG 檢索結果和草稿答案
        """
        print("【主線】開始 RAG 檢索...")
        
        # RAG 檢索
        retrieved_docs = await self.rag_retriever.retrieve(query, top_k=3)
        context = self.rag_retriever.format_context(retrieved_docs)
        matched_doc_ids = self.rag_retriever.get_matched_doc_ids(retrieved_docs)
        
        # 提取知識點
        knowledge_points = []
        for doc_id in matched_doc_ids:
            if doc_id in Config.KNOWLEDGE_POINTS:
                knowledge_points.append(Config.KNOWLEDGE_POINTS[doc_id])
        
        # 生成草稿答案
        draft_prompt = f"""
根據以下教材內容回答問題。

【教材內容】
{context}

【問題】
{query}

請提供初步答案：
"""
        
        response = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是一個專業的知識助手。"},
                {"role": "user", "content": draft_prompt}
            ],
            temperature=Config.LLM_TEMPERATURE,
            max_tokens=Config.LLM_MAX_TOKENS
        )
        
        draft_answer = response.choices[0].message.content
        
        print("【主線】RAG 檢索完成")
        
        return {
            "draft_answer": draft_answer,
            "context": context,
            "matched_docs": matched_doc_ids,
            "knowledge_points": knowledge_points,
            "retrieved_docs": retrieved_docs
        }
    
    async def branch_thread_scenario(self, query: str) -> Dict:
        """
        分支：情境判定
        
        Args:
            query: 用戶查詢
            
        Returns:
            情境判定結果
        """
        print("【分支】開始情境判定...")
        
        # 獲取歷史記錄
        history = self.history_manager.get_recent_history(n=5)
        
        # 呼叫 API 進行四向度判定
        result = self.scenario_classifier.classify(query, history=history)
        
        print("【分支】情境判定完成")
        
        return result
    
    async def merge_and_generate(
        self, 
        rag_result: Dict, 
        scenario_result: Dict, 
        query: str
    ) -> str:
        """
        會診：合併兩條線的結果並生成最終答案
        
        Args:
            rag_result: 主線的 RAG 結果
            scenario_result: 分支的情境判定結果
            query: 用戶問題
            
        Returns:
            最終答案
        """
        print("\n【會診】合併兩條線的結果...")
        
        # 提取結果
        draft_answer = rag_result['draft_answer']
        context = rag_result['context']
        knowledge_points = rag_result['knowledge_points']
        
        scenario_number = scenario_result['scenario_number']
        dimensions = scenario_result['dimensions']
        
        # 構建情境說明文字
        scenario_text = f"現在為第 {scenario_number} 種情境，分別代表 D1={dimensions['D1']}, D2={dimensions['D2']}, D3={dimensions['D3']}, D4={dimensions['D4']}"
        
        # 載入本體論（作為教材的一部分）
        ontology_content = self.ontology_manager.get_ontology_content()
        
        # 構建最終提示詞
        final_prompt = f"""
【初步答案】
{draft_answer}

【情境資訊】
{scenario_text}

【知識本體論】
{ontology_content}

【問題】
{query}

請根據以上情境資訊和教材內容，調整並生成最終回答。在回答中加入：「{scenario_text}」
"""
        
        print(f"【會診】情境資訊：{scenario_text}")
        
        # 生成最終答案
        response = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是一個專業的知識助手。"},
                {"role": "user", "content": final_prompt}
            ],
            temperature=Config.LLM_TEMPERATURE,
            max_tokens=Config.LLM_FINAL_MAX_TOKENS,
            stream=True
        )
        
        print("\n💬 生成最終答案...")
        print("-" * 60)
        
        final_answer = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                final_answer += content
        
        print("\n" + "-" * 60)
        
        return final_answer
    
    async def process_query(self, query: str) -> Dict:
        """
        處理查詢（雙線程版本）
        
        Args:
            query: 用戶查詢
            
        Returns:
            完整結果
        """
        print("\n" + "="*70)
        print(f"🔍 處理查詢: {query}")
        print("="*70)
        
        # 重置計時器
        self.timer = Timer()
        self.timer.start_stage("總流程")
        
        # ============ 雙線程並行處理 ============
        print("\n🚀 啟動雙線程並行處理...\n")
        self.timer.start_stage("並行處理")
        
        # 同時啟動兩條線
        main_task = self.main_thread_rag(query)
        branch_task = self.branch_thread_scenario(query)
        
        # 等待兩條線都完成
        rag_result, scenario_result = await asyncio.gather(main_task, branch_task)
        
        self.timer.stop_stage("並行處理")
        print("\n✅ 兩條線都已完成\n")
        
        # ============ 會診：合併結果 ============
        self.timer.start_stage("會診生成")
        
        final_answer = await self.merge_and_generate(rag_result, scenario_result, query)
        
        self.timer.stop_stage("會診生成")
        self.timer.stop_stage("總流程")
        
        # 記錄到歷史
        dimensions_dict = {
            "D1": "一個",  # TODO: 從 RAG 結果計算
            "D2": scenario_result['dimensions']['D2'],
            "D3": scenario_result['dimensions']['D3'],
            "D4": scenario_result['dimensions']['D4']
        }
        
        self.history_manager.add_query(
            query,
            rag_result['matched_docs'],
            dimensions_dict
        )
        
        # ============ 返回結果 ============
        result = {
            "query": query,
            "final_answer": final_answer,
            "scenario_number": scenario_result['scenario_number'],
            "scenario_description": scenario_result['description'],
            "dimensions": scenario_result['dimensions'],
            "matched_docs": rag_result['matched_docs'],
            "knowledge_points": rag_result['knowledge_points'],
            "time_report": self.timer.get_report().to_dict()
        }
        
        return result
    
    def print_summary(self, result: Dict):
        """打印結果摘要"""
        print("\n" + "="*70)
        print("📊 處理結果摘要")
        print("="*70)
        print(f"查詢：{result['query']}")
        print(f"\n情境：第 {result['scenario_number']} 種")
        print(f"描述：{result['scenario_description']}")
        print(f"\n四向度：")
        for dim, value in result['dimensions'].items():
            print(f"  {dim}: {value}")
        print(f"\n知識點：{', '.join(result['knowledge_points']) if result['knowledge_points'] else '無'}")
        print(f"\n時間報告：")
        for stage, duration in result['time_report']['stages'].items():
            print(f"  {stage}: {duration:.3f}s")
        print(f"  總計: {result['time_report']['total_time']:.3f}s")
        print("="*70)


async def main():
    """主函數"""
    print("\n" + "="*70)
    print("🚀 雙線程 RAG 系統")
    print("="*70)
    
    # 初始化系統
    system = ParallelRAGSystem()
    
    # 初始化文件
    await system.initialize_documents()
    
    # 測試查詢
    test_queries = [
        "什麼是機器學習？",
        "機器學習和深度學習有什麼區別？"
    ]
    
    for query in test_queries:
        result = await system.process_query(query)
        system.print_summary(result)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
