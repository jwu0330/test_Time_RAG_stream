"""
向量儲存模組
負責生成、儲存和載入文件的向量表示
"""
import os
import pickle
import json
from typing import List, Dict, Optional
import numpy as np
from openai import OpenAI


class VectorStore:
    """向量儲存管理類"""
    
    def __init__(self, storage_path: str = "vectors.pkl", api_key: Optional[str] = None):
        """
        初始化向量儲存
        
        Args:
            storage_path: 向量儲存路徑
            api_key: OpenAI API Key
        """
        self.storage_path = storage_path
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.vectors: Dict[str, dict] = {}
        self.embedding_model = "text-embedding-3-small"
    
    async def create_embedding(self, text: str) -> List[float]:
        """
        生成文本的向量表示
        
        Args:
            text: 輸入文本
            
        Returns:
            向量列表
        """
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    async def add_document(self, doc_id: str, content: str, metadata: Optional[dict] = None):
        """
        添加文件並生成向量
        
        Args:
            doc_id: 文件ID
            content: 文件內容
            metadata: 額外的元數據
        """
        embedding = await self.create_embedding(content)
        
        self.vectors[doc_id] = {
            "content": content,
            "embedding": embedding,
            "metadata": metadata or {}
        }
        
        print(f"✅ 已向量化文件: {doc_id}")
    
    async def batch_add_documents(self, documents: List[Dict[str, str]]):
        """
        批量添加文件
        
        Args:
            documents: 文件列表，每個包含 id 和 content
        """
        for doc in documents:
            await self.add_document(
                doc_id=doc.get("id", ""),
                content=doc.get("content", ""),
                metadata=doc.get("metadata", {})
            )
    
    def save(self):
        """儲存向量到本地文件"""
        with open(self.storage_path, 'wb') as f:
            pickle.dump(self.vectors, f)
        print(f"💾 向量已儲存至: {self.storage_path}")
    
    def load(self) -> bool:
        """
        從本地文件載入向量
        
        Returns:
            是否成功載入
        """
        if not os.path.exists(self.storage_path):
            print(f"⚠️  向量文件不存在: {self.storage_path}")
            return False
        
        with open(self.storage_path, 'rb') as f:
            self.vectors = pickle.load(f)
        
        print(f"✅ 已載入 {len(self.vectors)} 個向量")
        return True
    
    def export_to_json(self, json_path: str = "vectors.json"):
        """
        導出向量為 JSON 格式（不包含實際向量，僅元數據）
        
        Args:
            json_path: JSON 文件路徑
        """
        export_data = {}
        for doc_id, data in self.vectors.items():
            export_data[doc_id] = {
                "content": data["content"],
                "metadata": data["metadata"],
                "embedding_dim": len(data["embedding"])
            }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"📄 元數據已導出至: {json_path}")
    
    def get_all_documents(self) -> Dict[str, dict]:
        """獲取所有文件"""
        return self.vectors
    
    def get_document(self, doc_id: str) -> Optional[dict]:
        """獲取特定文件"""
        return self.vectors.get(doc_id)
    
    def clear(self):
        """清空所有向量"""
        self.vectors = {}
        print("🗑️  已清空所有向量")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    計算兩個向量的餘弦相似度
    
    Args:
        vec1: 向量1
        vec2: 向量2
        
    Returns:
        相似度分數 (0-1)
    """
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)
    
    dot_product = np.dot(vec1_np, vec2_np)
    norm1 = np.linalg.norm(vec1_np)
    norm2 = np.linalg.norm(vec2_np)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot_product / (norm1 * norm2))
