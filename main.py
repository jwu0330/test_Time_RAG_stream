"""
主程序 - RAG 流式中斷與續寫系統
支援向量儲存、情境注入、時間分析
"""
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from openai import OpenAI

from vector_store import VectorStore
from rag_module import RAGRetriever, RAGCache
from scenario_module import ScenarioClassifier, ScenarioInjector
from timer_utils import Timer


class RAGStreamSystem:
    """RAG 流式系統主類"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化系統
        
        Args:
            api_key: OpenAI API Key (如果不提供，將從環境變量讀取)
        """
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        
        # 初始化各模組
        self.vector_store = VectorStore(api_key=api_key)
        self.rag_retriever = RAGRetriever(self.vector_store)
        self.rag_cache = RAGCache()
        self.scenario_classifier = ScenarioClassifier(api_key=api_key)
        self.scenario_injector = ScenarioInjector(self.scenario_classifier)
        
        # 系統狀態
        self.draft_response = ""
        self.timer = Timer()
        
        print("🚀 RAG 流式系統已初始化")
    
    async def initialize_documents(self, docs_dir: str = "docs"):
        """
        初始化文件向量化
        
        Args:
            docs_dir: 文件目錄
        """
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
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append({
                        "id": filename,
                        "content": content,
                        "metadata": {"filename": filename}
                    })
        
        if documents:
            await self.vector_store.batch_add_documents(documents)
            self.vector_store.save()
            self.vector_store.export_to_json()
        
        self.timer.stop_stage("向量化")
    
    async def load_scenarios(self, scenarios_dir: str = "scenarios"):
        """
        載入情境文件
        
        Args:
            scenarios_dir: 情境目錄
        """
        print(f"\n🎭 載入情境...")
        self.scenario_classifier.load_scenarios_from_dir(scenarios_dir)
    
    async def generate_draft(self, query: str, context: str) -> str:
        """
        生成通用草稿（不輸出，僅內部保存）
        
        Args:
            query: 用戶查詢
            context: RAG 檢索到的上下文
            
        Returns:
            草稿內容
        """
        print("\n📝 生成通用草稿...")
        self.timer.start_stage("LLM草稿生成")
        
        prompt = f"""
基於以下檢索到的相關文件，回答用戶的問題。
這是一個初步草稿，稍後會根據具體情境進行調整。

相關文件：
{context}

用戶問題：
{query}

請提供一個結構化的初步回答。
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個專業的知識助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        draft = response.choices[0].message.content
        self.draft_response = draft
        
        self.timer.stop_stage("LLM草稿生成")
        print("✅ 草稿已生成（暫存中）")
        
        return draft
    
    async def resume_with_scenario(
        self, 
        query: str,
        scenario_ids: List[str]
    ) -> str:
        """
        根據情境續寫最終答案
        
        Args:
            query: 原始查詢
            scenario_ids: 情境 ID 列表
            
        Returns:
            最終答案
        """
        print(f"\n🎯 注入情境並續寫: {', '.join(scenario_ids)}")
        self.timer.start_stage("情境注入與續寫")
        
        # 獲取情境內容
        scenario_context = self.scenario_classifier.format_scenario_context(scenario_ids)
        
        # 創建注入提示
        injection_prompt = self.scenario_injector.create_injection_prompt(
            draft_response=self.draft_response,
            scenario_context=scenario_context,
            original_query=query
        )
        
        # 流式生成最終答案
        print("\n💬 最終回答：")
        print("-" * 50)
        
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個專業的知識助手。"},
                {"role": "user", "content": injection_prompt}
            ],
            temperature=0.7,
            stream=True
        )
        
        final_answer = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                final_answer += content
        
        print("\n" + "-" * 50)
        
        self.timer.stop_stage("情境注入與續寫")
        
        return final_answer
    
    async def process_query(
        self, 
        query: str,
        scenario_ids: Optional[List[str]] = None,
        auto_classify: bool = True
    ) -> Dict:
        """
        處理完整查詢流程
        
        Args:
            query: 用戶查詢
            scenario_ids: 指定的情境 ID（如果為 None 則自動分類）
            auto_classify: 是否自動進行情境分類
            
        Returns:
            完整結果字典
        """
        print("\n" + "="*60)
        print(f"🔍 處理查詢: {query}")
        print("="*60)
        
        # 重置計時器
        self.timer = Timer()
        
        # Step 1: RAG 檢索
        print("\n📊 Step 1: RAG 檢索")
        self.timer.start_stage("RAG檢索")
        
        retrieved_docs = await self.rag_retriever.retrieve(query, top_k=3)
        context = self.rag_retriever.format_context(retrieved_docs)
        matched_doc_ids = self.rag_retriever.get_matched_doc_ids(retrieved_docs)
        
        self.timer.stop_stage("RAG檢索")
        print(f"✅ 找到 {len(retrieved_docs)} 個相關文件")
        
        # Step 2: 情境分類（如果需要）
        if auto_classify and not scenario_ids:
            print("\n🎯 Step 2: 情境分類")
            self.timer.start_stage("情境分類")
            
            classification = await self.scenario_classifier.classify_scenario(
                query=query,
                context=context
            )
            scenario_ids = self.scenario_classifier.get_scenario_by_dimensions(classification)
            
            self.timer.stop_stage("情境分類")
            print(f"✅ 推薦情境: {', '.join(scenario_ids) if scenario_ids else '無'}")
        
        # Step 3: 生成草稿
        print("\n📝 Step 3: 生成通用草稿")
        draft = await self.generate_draft(query, context)
        
        # Step 4: 模擬暫停（stream interruption）
        print("\n⏸️  Step 4: 流式暫停（等待情境注入）")
        await asyncio.sleep(0.5)  # 模擬暫停
        
        # Step 5: 情境注入與續寫
        print("\n▶️  Step 5: 情境注入與續寫")
        if not scenario_ids:
            scenario_ids = []
        
        final_answer = await self.resume_with_scenario(query, scenario_ids)
        
        # Step 6: 背景任務模擬
        print("\n🔄 Step 6: 執行背景任務")
        await self.run_background_tasks()
        
        # 生成報告
        report = self.timer.get_report()
        
        result = {
            "query": query,
            "final_answer": final_answer,
            "scenario_used": "+".join(scenario_ids) if scenario_ids else "無",
            "matched_docs": matched_doc_ids,
            "time_report": report.to_dict()
        }
        
        return result
    
    async def run_background_tasks(self):
        """執行背景任務（模擬）"""
        self.timer.start_stage("背景任務")
        
        tasks = [
            self.update_color_tags(),
            self.save_cache_annotations(),
            self.log_activity()
        ]
        
        await asyncio.gather(*tasks)
        
        self.timer.stop_stage("背景任務")
        print("✅ 背景任務完成")
    
    async def update_color_tags(self):
        """更新顏色標籤（模擬）"""
        await asyncio.sleep(0.2)
        print("  🎨 顏色標籤已更新")
    
    async def save_cache_annotations(self):
        """儲存快取標註（模擬）"""
        await asyncio.sleep(0.3)
        print("  💾 快取標註已儲存")
    
    async def log_activity(self):
        """記錄活動日誌（模擬）"""
        await asyncio.sleep(0.1)
        print("  📋 活動日誌已記錄")
    
    def save_result(self, result: Dict, output_dir: str = "results"):
        """
        儲存結果到文件
        
        Args:
            result: 結果字典
            output_dir: 輸出目錄
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"result_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 結果已儲存至: {filepath}")
    
    def print_summary(self, result: Dict):
        """打印結果摘要"""
        print("\n" + "="*60)
        print("📊 執行摘要")
        print("="*60)
        print(f"查詢: {result['query']}")
        print(f"使用情境: {result['scenario_used']}")
        print(f"匹配文件: {', '.join(result['matched_docs'])}")
        print(f"\n⏱️  時間分析:")
        for stage, duration in result['time_report']['stages'].items():
            print(f"  {stage:20s}: {duration:6.3f}s")
        print(f"  {'總計':20s}: {result['time_report']['total_time']:6.3f}s")
        print("="*60)


async def main():
    """主函數 - 示例使用"""
    
    # 初始化系統
    system = RAGStreamSystem()
    
    # 初始化文件和情境
    await system.initialize_documents()
    await system.load_scenarios()
    
    # 測試查詢
    test_queries = [
        "什麼是機器學習？",
        "如何優化深度學習模型？",
        "解釋一下自然語言處理的基本概念"
    ]
    
    print("\n" + "="*60)
    print("🧪 開始測試回合")
    print("="*60)
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n\n{'='*60}")
        print(f"測試 {i}/{len(test_queries)}")
        print(f"{'='*60}")
        
        result = await system.process_query(query)
        results.append(result)
        
        system.print_summary(result)
        system.save_result(result)
        
        # 間隔
        if i < len(test_queries):
            await asyncio.sleep(1)
    
    # 平均時間分析
    print("\n" + "="*60)
    print("📈 平均效能分析")
    print("="*60)
    
    avg_times = {}
    for result in results:
        for stage, duration in result['time_report']['stages'].items():
            if stage not in avg_times:
                avg_times[stage] = []
            avg_times[stage].append(duration)
    
    for stage, times in avg_times.items():
        avg = sum(times) / len(times)
        print(f"  {stage:20s}: {avg:6.3f}s (平均)")
    
    total_avg = sum(r['time_report']['total_time'] for r in results) / len(results)
    print(f"  {'總計':20s}: {total_avg:6.3f}s (平均)")
    print("="*60)
    
    print("\n✅ 所有測試完成！")


if __name__ == "__main__":
    asyncio.run(main())
