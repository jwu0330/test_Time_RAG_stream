"""
主程序 - 雙回合流程
實現：
1. 判定回合：並行執行 RAG 檢索 + K/C/R 維度判定（返回情境編號）
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
from config import Config, get_shared_client


class ResponsesRAGSystem:
    """使用 Responses API 的雙回合 RAG 系統"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化系統
        
        Args:
            api_key: OpenAI API Key
        """
        self.api_key = api_key
        # 使用共享的 OpenAI client
        self.client = get_shared_client(api_key)
        
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
        
        print("🚀 RAG 系統已初始化（K, C, R 三維度分類）")
    
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
        主線（Thread 1）：RAG 檢索（不生成草稿）
        
        Args:
            query: 用戶查詢
            
        Returns:
            RAG 檢索結果
        """
        import time
        t_start = time.perf_counter()
        
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
        
        t_end = time.perf_counter()
        rag_total_time = t_end - t_start
        
        # 獲取 RAG 內部計時
        rag_timing = getattr(self.rag_retriever, '_last_timing', {})
        
        return {
            "context": context,
            "matched_docs": matched_doc_ids,
            "knowledge_points": knowledge_points,
            "retrieved_docs": retrieved_docs,
            "timing": {
                "total": rag_total_time,
                "embedding_api": rag_timing.get("embedding_api", 0),
                "similarity_calc": rag_timing.get("similarity_calc", 0)
            }
        }
    
    async def parallel_dimension_classification(self, query: str, matched_docs: List[str]) -> Dict:
        """
        並行執行 K/C/R 三維度判定
        
        Args:
            query: 用戶查詢
            matched_docs: RAG 匹配到的文檔 ID
            
        Returns:
            情境判定結果
        """
        # 使用 ScenarioClassifier 進行分類
        result = await self.scenario_classifier.classify(query)
        
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
        
        # 獲取情境提示詞
        scenario_prompt = scenario_result.get('prompt', '')
        scenario_label = scenario_result.get('label', '')
        
        # 載入本體論
        ontology_content = self.ontology_manager.get_ontology_content()
        
        # 構建最終提示詞（加入當前情境編號 + 測試說明）
        final_prompt = f"""
        【當前是第 {scenario_number} 種情境】

        {scenario_prompt}

        【RAG 檢索到的教材片段】
        {context}

        【知識本體論】
        {ontology_content}

        【匹配的知識點】
        {', '.join(knowledge_points) if knowledge_points else '無'}

        【用戶問題】
        {query}

        ⚠️ 注意：這是測試環境，請將回答控制在約 100 字左右，以便測試系統響應時間。請根據教材內容簡潔回答問題。
        """
        
        print(f"【最終回合】情境 {scenario_number}：{scenario_label}")
        print(f"【最終回合】提示：{scenario_prompt}")
        
        # 使用 Responses API 生成最終答案（流式）
        response = self.client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是專業知識助手。"},
                {"role": "user", "content": final_prompt}
            ],
            temperature=Config.LLM_TEMPERATURE,
            max_tokens=Config.LLM_FINAL_MAX_TOKENS,  # 使用配置中的最大 token 數
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
        處理查詢（3 個獨立並行執行緒 + 最終生成）
        
        第一回合：並行執行 3 個 API
          - Thread 1: RAG Embedding
          - Thread 2: C 值檢測
          - Thread 3: 知識點檢測
        第二回合：整合結果，生成最終答案
        
        Args:
            query: 用戶查詢
            
        Returns:
            處理結果
        """
        print(f"\n{'='*70}")
        print(f"📥 收到查詢: {query}")
        print(f"{'='*70}")
        
        # 第一回合：並行執行 3 個獨立 API
        self.timer.start_stage("並行處理")
        
        import time
        
        # 記錄開始時間
        t_parallel_start = time.perf_counter()
        
        # 3 個獨立的執行緒
        rag_task = self.main_thread_rag(query)  # Thread 1: RAG
        
        t_c_start = time.perf_counter()
        c_task = self.scenario_classifier.dimension_classifier.correctness_detector.detect(query)  # Thread 2: C值
        
        t_k_start = time.perf_counter()
        knowledge_task = self.scenario_classifier.dimension_classifier.knowledge_detector.detect(query)  # Thread 3: 知識點
        
        # 等待 3 個任務都完成
        rag_result, c_value, knowledge_points = await asyncio.gather(
            rag_task,
            c_task,
            knowledge_task
        )
        
        t_parallel_end = time.perf_counter()
        parallel_total_time = t_parallel_end - t_parallel_start
        
        # 本地計算 K 值和 R 值（不需要 API）
        t_local_start = time.perf_counter()
        k_value = self.scenario_classifier.dimension_classifier.knowledge_detector.calculate_k_value(knowledge_points)
        r_value = self.scenario_classifier.dimension_classifier.repetition_checker.check_and_update(knowledge_points)
        
        # 計算情境編號
        scenario_number = self.scenario_classifier.dimension_classifier.scenario_calculator.calculate(k_value, c_value, r_value)
        t_local_end = time.perf_counter()
        local_calc_time = t_local_end - t_local_start
        
        # 記錄情境計算完成時間點
        t_scenario_calc_done = time.perf_counter()
        
        # 打印維度分類結果
        print(f"\n🔍 維度分類結果：")
        print(f"  K (知識點數量): {k_value} ({['零個', '一個', '多個'][k_value]})")
        print(f"  C (正確性): {c_value} ({['正確', '不正確'][c_value]})")
        print(f"  R (重複性): {r_value} ({['正常', '重複'][r_value]})")
        print(f"  知識點: {knowledge_points if knowledge_points else '無'}")
        print(f"✅ 計算得出情境編號：{scenario_number}")
        
        # 獲取情境詳細信息
        scenario = self.scenario_classifier.get_scenario_by_number(scenario_number)
        
        # 構建 scenario_result
        scenario_result = {
            "scenario_number": scenario_number,
            "dimensions": {
                "K": k_value,
                "C": c_value,
                "R": r_value
            },
            "knowledge_points": knowledge_points,
            "label": scenario.get('label', '') if scenario else '',
            "role": scenario.get('role', '') if scenario else '',
            "prompt": scenario.get('prompt', '') if scenario else ''
        }
        
        # 記錄整合準備完成時間
        t_integration_done = time.perf_counter()
        integration_time = t_integration_done - t_scenario_calc_done
        
        self.timer.stop_stage("並行處理")
        
        # 收集所有計時信息
        rag_timing = rag_result.get("timing", {})
        c_timing = getattr(self.scenario_classifier.dimension_classifier.correctness_detector, '_last_timing', 0)
        k_timing = getattr(self.scenario_classifier.dimension_classifier.knowledge_detector, '_last_timing', 0)
        
        # 第二回合：生成答案
        self.timer.start_stage("最終回合生成")
        t_final_start = time.perf_counter()
        
        final_answer = await self.final_round_generate(rag_result, scenario_result, query)
        
        t_final_end = time.perf_counter()
        final_generation_time = t_final_end - t_final_start
        
        self.timer.stop_stage("最終回合生成")
        self.timer.stop_stage("總流程")
        
        # 打印詳細計時報告（包含並行執行詳情）
        print(f"\n{'='*70}")
        print(f"⏱️  詳細時間分析報告（3 個並行執行緒）")
        print(f"{'='*70}\n")
        
        print(f"【並行執行詳情】")
        print(f"  Thread 1 - RAG 檢索:")
        print(f"    ├─ Embedding API 調用: {rag_timing.get('embedding_api', 0):.3f}s")
        print(f"    ├─ 相似度計算: {rag_timing.get('similarity_calc', 0):.3f}s")
        print(f"    └─ 總耗時: {rag_timing.get('total', 0):.3f}s")
        print(f"")
        print(f"  Thread 2 - C 值檢測:")
        print(f"    └─ API 調用耗時: {c_timing:.3f}s")
        print(f"")
        print(f"  Thread 3 - 知識點檢測:")
        print(f"    └─ API 調用耗時: {k_timing:.3f}s")
        print(f"")
        print(f"  本地計算 (K/R 值):")
        print(f"    └─ 計算耗時: {local_calc_time:.6f}s")
        print(f"")
        print(f"  並行執行總時間: {parallel_total_time:.3f}s")
        print(f"  理論最大時間: {max(rag_timing.get('total', 0), c_timing, k_timing):.3f}s")
        print(f"  並行效率: {(1 - parallel_total_time / (rag_timing.get('total', 0) + c_timing + k_timing)) * 100:.1f}%")
        print(f"")
        print(f"【後處理階段】")
        print(f"  情境計算 + 結果整合: {integration_time:.3f}s")
        print(f"  最終答案生成: {final_generation_time:.3f}s")
        print(f"  後處理總時間: {integration_time + final_generation_time:.3f}s")
        print(f"\n{'='*70}\n")
        
        # 舊版時間報告已移除，僅保留上方新版「詳細時間分析報告（3 個並行執行緒）」
        
        # 記錄到歷史（簡化版，只記錄基本信息）
        dimensions_dict = {
            "K": scenario_result['dimensions']['K'],
            "C": scenario_result['dimensions']['C'],
            "R": scenario_result['dimensions']['R']
        }
        
        self.history_manager.add_query(
            query,
            rag_result['matched_docs'],
            dimensions_dict,
            scenario_result.get('knowledge_points', [])
        )
        
        # ============ 返回結果 ============
        result = {
            "query": query,
            "final_answer": final_answer,
            "scenario_number": scenario_result['scenario_number'],
            "scenario_label": scenario_result.get('label', ''),
            "scenario_role": scenario_result.get('role', ''),
            "scenario_prompt": scenario_result.get('prompt', ''),
            "dimensions": scenario_result['dimensions'],
            "matched_docs": rag_result['matched_docs'],
            "knowledge_points": rag_result['knowledge_points'],
            "time_report": self.timer.get_report().to_dict()
        }
        
        return result
    
    def print_summary(self, result: Dict):
        """打印結果摘要"""
        print("\n" + "="*70)
        print("📊 RAG 系統處理結果摘要")
        print("="*70)
        print(f"查詢：{result['query']}")
        print(f"\n🎯 情境判定：第 {result['scenario_number']} 種情境")
        print(f"   標籤：{result['scenario_label']}")
        print(f"   角色：{result['scenario_role']}")
        print(f"\n📐 三維度分析：")
        k_map = {0: "零個", 1: "一個", 2: "多個"}
        c_map = {0: "正確", 1: "不正確"}
        r_map = {0: "正常", 1: "重複"}
        dims = result['dimensions']
        print(f"   K (知識點數量): {k_map.get(dims['K'], dims['K'])}")
        print(f"   C (正確性): {c_map.get(dims['C'], dims['C'])}")
        print(f"   R (重複性): {r_map.get(dims['R'], dims['R'])}")
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
    print("🚀 RAG 教學問答系統 (K/C/R 三維度分類)")
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
