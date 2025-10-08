"""
RAG 檢索模組
負責向量比對和文件檢索
"""
from typing import List, Dict, Tuple
from vector_store import VectorStore, cosine_similarity


class RAGRetriever:
    """RAG 檢索器"""
    
    def __init__(self, vector_store: VectorStore):
        """
        初始化檢索器
        
        Args:
            vector_store: 向量儲存實例
        """
        self.vector_store = vector_store
    
    async def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        檢索最相關的文件
        
        Args:
            query: 查詢文本
            top_k: 返回前 K 個最相關文件
            
        Returns:
            相關文件列表，包含 doc_id, content, score
        """
        # 生成查詢向量
        query_embedding = await self.vector_store.create_embedding(query)
        
        # 計算所有文件的相似度
        similarities = []
        for doc_id, doc_data in self.vector_store.get_all_documents().items():
            doc_embedding = doc_data["embedding"]
            score = cosine_similarity(query_embedding, doc_embedding)
            
            similarities.append({
                "doc_id": doc_id,
                "content": doc_data["content"],
                "metadata": doc_data.get("metadata", {}),
                "score": score
            })
        
        # 排序並返回 top_k
        similarities.sort(key=lambda x: x["score"], reverse=True)
        return similarities[:top_k]
    
    async def retrieve_with_threshold(
        self, 
        query: str, 
        threshold: float = 0.7,
        top_k: int = 5
    ) -> List[Dict]:
        """
        檢索相似度超過閾值的文件
        
        Args:
            query: 查詢文本
            threshold: 相似度閾值
            top_k: 最多返回數量
            
        Returns:
            符合條件的文件列表
        """
        results = await self.retrieve(query, top_k=top_k)
        return [doc for doc in results if doc["score"] >= threshold]
    
    def format_context(self, retrieved_docs: List[Dict]) -> str:
        """
        格式化檢索到的文件為上下文
        
        Args:
            retrieved_docs: 檢索結果
            
        Returns:
            格式化的上下文字符串
        """
        if not retrieved_docs:
            return "無相關文件"
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(
                f"[文件 {i}: {doc['doc_id']}] (相似度: {doc['score']:.3f})\n"
                f"{doc['content']}\n"
            )
        
        return "\n".join(context_parts)
    
    def get_matched_doc_ids(self, retrieved_docs: List[Dict]) -> List[str]:
        """
        獲取匹配的文件 ID 列表
        
        Args:
            retrieved_docs: 檢索結果
            
        Returns:
            文件 ID 列表
        """
        return [doc["doc_id"] for doc in retrieved_docs]


class RAGCache:
    """RAG 快取管理"""
    
    def __init__(self, max_size: int = 100):
        """
        初始化快取
        
        Args:
            max_size: 最大快取數量
        """
        self.cache: Dict[str, List[Dict]] = {}
        self.max_size = max_size
        self.hit_count = 0
        self.miss_count = 0
    
    def get(self, query: str) -> List[Dict] | None:
        """
        從快取獲取結果
        
        Args:
            query: 查詢文本
            
        Returns:
            快取的結果或 None
        """
        if query in self.cache:
            self.hit_count += 1
            return self.cache[query]
        
        self.miss_count += 1
        return None
    
    def put(self, query: str, results: List[Dict]):
        """
        將結果放入快取
        
        Args:
            query: 查詢文本
            results: 檢索結果
        """
        if len(self.cache) >= self.max_size:
            # 簡單的 FIFO 策略
            first_key = next(iter(self.cache))
            del self.cache[first_key]
        
        self.cache[query] = results
    
    def clear(self):
        """清空快取"""
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0
    
    def get_stats(self) -> Dict:
        """獲取快取統計"""
        total = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total if total > 0 else 0
        
        return {
            "hits": self.hit_count,
            "misses": self.miss_count,
            "hit_rate": round(hit_rate, 3),
            "cache_size": len(self.cache)
        }
