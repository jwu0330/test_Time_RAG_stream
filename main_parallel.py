"""
主程序 - 使用 Responses API 的雙回合流程
實現：
1. 判定回合：並行執行 RAG 檢索 + Responses API function call（返回情境編號）
2. 最終回合：告訴 AI 當前情境，結合 RAG + 本體論，生成流式答案
"""
import asyncio
import os
import time
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


class ResponsesRAGSystem:
    """使用 Responses API 的雙回合 RAG 系統"""
    
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
        
        # 將計時器注入到 scenario_classifier
        self.scenario_classifier.set_timer(self.timer)
        
        print("🚀 Responses API 雙回合 RAG 系統已初始化（五個並行分支）")
    
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
        主線（Thread A）：RAG 檢索（不生成草稿）
        
        Args:
            query: 用戶查詢
            
        Returns:
            RAG 檢索結果
        """
        self.timer.start_stage("RAG檢索", thread='A')
        
        # RAG 檢索
        retrieved_docs = await self.rag_retriever.retrieve(query, top_k=3)
        context = self.rag_retriever.format_context(retrieved_docs)
        matched_doc_ids = self.rag_retriever.get_matched_doc_ids(retrieved_docs)
        
        # 提取知識點
        knowledge_points = []
        for doc_id in matched_doc_ids:
            if doc_id in Config.KNOWLEDGE_POINTS:
                knowledge_points.append(Config.KNOWLEDGE_POINTS[doc_id])
        
        self.timer.stop_stage("RAG檢索", thread='A')
        
        return {
            "context": context,
            "matched_docs": matched_doc_ids,
            "knowledge_points": knowledge_points,
            "retrieved_docs": retrieved_docs
        }
    
    async def parallel_dimension_classification(self, query: str, matched_docs: List[str]) -> Dict:
        """
        並行執行四個向度判定（Thread B, C, D, E）
        
        Args:
            query: 用戶查詢
            matched_docs: RAG 匹配到的文檔 ID
            
        Returns:
            情境判定結果
        """
        # 獲取歷史對話（只有 D4 需要）
        history = self.history_manager.get_recent_history(5)
        history_list = [h.to_dict() for h in history]
        
        # 並行執行四個向度判定，傳入 RAG 結果
        result = await self.scenario_classifier.classify(query, history_list, matched_docs)
        
        return result
    
    async def final_round_generate(
        self, 
        rag_result: Dict, 
        scenario_result: Dict, 
        query: str
    ) -> str:
        """
        最終回合：簡單告訴 AI 當前情境，結合 RAG + 本體論生成答案
        
        Args:
            rag_result: 主線的 RAG 結果
            scenario_result: 分支的情境判定結果
            query: 用戶問題
            
        Returns:
            最終答案
        """
        print("\n【最終回合】整合 RAG + 本體論生成答案...")
        
        # 提取結果
        context = rag_result['context']
        knowledge_points = rag_result['knowledge_points']
        
        scenario_number = scenario_result['scenario_number']
        dimensions = scenario_result['dimensions']
        
        # 構建情境說明文字（簡單明瞭）
        scenario_text = f"現在為第 {scenario_number} 種情境，代表 D1={dimensions['D1']}, D2={dimensions['D2']}, D3={dimensions['D3']}, D4={dimensions['D4']}"
        
        # 載入本體論
        ontology_content = self.ontology_manager.get_ontology_content()
        
        # 構建最終提示詞（簡化版，不使用複雜模板）
        final_prompt = f"""
請回答以下問題。

【當前情境】
{scenario_text}

【RAG 檢索到的教材片段】
{context}

【知識本體論】
{ontology_content}

【匹配的知識點】
{', '.join(knowledge_points) if knowledge_points else '無'}

【用戶問題】
{query}

請根據上述資訊生成回答。在回答開頭簡要說明：「{scenario_text}」

**重要：回答限制在 100 字以內。**
"""
        
        print(f"【最終回合】情境：{scenario_text}")
        
        # 使用 Responses API 生成最終答案（流式）
        response = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是專業知識助手。回答限制在 100 字以內。"},
                {"role": "user", "content": final_prompt}
            ],
            temperature=Config.LLM_TEMPERATURE,
            max_tokens=200,  # 100 字約 200 tokens
            stream=True
        )
        
        print("\n💬 生成最終答案（流式輸出）...")
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
        處理查詢（五個並行分支 + 最終生成）
        
        第一回合：並行執行 RAG 檢索 + 四個向度判定（5個分支）
        第二回合：整合結果，生成最終答案
        
        Args:
            query: 用戶查詢
            
        Returns:
            處理結果
        """
        print(f"\n{'='*70}")
        print(f"📥 收到查詢: {query}")
        print(f"{'='*70}")
        
        # 第一回合：真正的並行執行（RAG + 四個向度判定）
        self.timer.start_stage("並行處理（5個分支）")
        
        # ✅ 真正的並行：同時執行 RAG 和四個向度判定
        # D4 API 不再依賴 RAG 結果，所以可以完全並行
        rag_task = self.main_thread_rag(query)
        scenario_task = self.parallel_dimension_classification(query, None)  # 不傳入 matched_docs
        
        # 等待兩者都完成
        rag_result, scenario_result = await asyncio.gather(rag_task, scenario_task)
        
        self.timer.stop_stage("並行處理（5個分支）")
        print(f"\n✅ 真正的並行完成：RAG + 四個向度判定同時執行\n")
        
        # 第二回合：生成答案
        self.timer.start_stage("最終回合生成")
        
        final_answer = await self.final_round_generate(rag_result, scenario_result, query)
        
        self.timer.stop_stage("最終回合生成")
        self.timer.stop_stage("總流程")
        
        # 打印詳細計時報告
        self.timer.print_report()
        
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
            dimensions_dict,
            scenario_result.get('knowledge_binary', '0000')  # 傳入二進制編碼
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
        print("📊 Responses API 雙回合處理結果摘要")
        print("="*70)
        print(f"查詢：{result['query']}")
        print(f"\n🎯 情境判定：第 {result['scenario_number']} 種情境")
        print(f"   描述：{result['scenario_description']}")
        print(f"\n📐 四向度分析：")
        for dim, value in result['dimensions'].items():
            print(f"   {dim}: {value}")
        print(f"\n📚 匹配知識點：{', '.join(result['knowledge_points']) if result['knowledge_points'] else '無'}")
        print(f"\n⏱️  執行時間分析：")
        time_report = result['time_report']
        
        # 主流程時間
        if 'stages' in time_report:
            print("  ┌─ 【主流程 - 總體時間】")
            for stage, duration in time_report['stages'].items():
                print(f"  │   {stage:30s}: {duration:6.3f}s")
        
        # Thread A 時間（RAG 檢索）
        if 'thread_a' in time_report:
            print(f"  ├─ 【{time_report['thread_a']['thread_name']}】")
            for stage, duration in time_report['thread_a']['stages'].items():
                print(f"  │   {stage:30s}: {duration:6.3f}s")
            print(f"  │   {'─' * 40}")
            print(f"  │   {'主線小計':30s}: {time_report['thread_a']['total_time']:6.3f}s")
        
        # Thread B 時間（Responses API 情境判定）
        if 'thread_b' in time_report:
            print(f"  └─ 【{time_report['thread_b']['thread_name']}】")
            for stage, duration in time_report['thread_b']['stages'].items():
                print(f"      {stage:30s}: {duration:6.3f}s")
            print(f"      {'─' * 40}")
            print(f"      {'支線小計':30s}: {time_report['thread_b']['total_time']:6.3f}s")
        
        print(f"\n  🎯 總計時間: {time_report['total_time']:.3f}s")
        print("="*70)


async def main():
    """主函數"""
    print("\n" + "="*70)
    print("🚀 Responses API 雙回合 RAG 系統")
    print("="*70)
    
    # 初始化系統
    system = ResponsesRAGSystem()
    
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
