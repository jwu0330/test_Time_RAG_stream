"""
歷史紀錄管理模組
負責追蹤查詢歷史和知識點訪問記錄
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from collections import deque, Counter
from config import Config


class QueryHistory:
    """單次查詢歷史記錄"""
    
    def __init__(
        self,
        query: str,
        matched_docs: List[str],
        knowledge_points: List[str],
        dimensions: Dict[str, str],
        timestamp: str
    ):
        self.query = query
        self.matched_docs = matched_docs
        self.knowledge_points = knowledge_points
        self.dimensions = dimensions
        self.timestamp = timestamp
    
    def to_dict(self) -> dict:
        """轉換為字典"""
        return {
            "query": self.query,
            "matched_docs": self.matched_docs,
            "knowledge_points": self.knowledge_points,
            "dimensions": self.dimensions,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """從字典創建"""
        return cls(
            query=data["query"],
            matched_docs=data["matched_docs"],
            knowledge_points=data["knowledge_points"],
            dimensions=data["dimensions"],
            timestamp=data["timestamp"]
        )


class HistoryManager:
    """歷史紀錄管理器"""
    
    def __init__(self, max_size: int = None, storage_path: str = None):
        """
        初始化歷史管理器
        
        Args:
            max_size: 最大保存記錄數（默認從配置讀取）
            storage_path: 儲存路徑（默認從配置讀取）
        """
        self.max_size = max_size or Config.HISTORY_SIZE
        self.storage_path = storage_path or Config.HISTORY_STORAGE_PATH
        
        # 使用 deque 實現固定大小的歷史記錄
        self.history: deque = deque(maxlen=self.max_size)
        
        # 知識點訪問計數器
        self.knowledge_point_counter = Counter()
        
        # 連續訪問追蹤（用於檢測重複）
        self.consecutive_access: deque = deque(maxlen=10)
        
        # 載入已存在的歷史
        self.load()
    
    def add_query(
        self,
        query: str,
        matched_docs: List[str],
        dimensions: Dict[str, str]
    ) -> QueryHistory:
        """
        添加查詢記錄
        
        Args:
            query: 查詢內容
            matched_docs: 匹配的文件列表
            dimensions: 四向度判定結果
            
        Returns:
            查詢歷史記錄
        """
        # 從匹配的文件中提取知識點
        knowledge_points = self._extract_knowledge_points(matched_docs)
        
        # 創建歷史記錄
        record = QueryHistory(
            query=query,
            matched_docs=matched_docs,
            knowledge_points=knowledge_points,
            dimensions=dimensions,
            timestamp=datetime.now().isoformat()
        )
        
        # 添加到歷史
        self.history.append(record)
        
        # 更新知識點計數
        for kp in knowledge_points:
            self.knowledge_point_counter[kp] += 1
        
        # 更新連續訪問記錄
        self.consecutive_access.extend(knowledge_points)
        
        # 自動儲存
        self.save()
        
        return record
    
    def _extract_knowledge_points(self, matched_docs: List[str]) -> List[str]:
        """
        從匹配的文件中提取知識點
        
        Args:
            matched_docs: 文件列表
            
        Returns:
            知識點列表
        """
        knowledge_points = []
        for doc in matched_docs:
            if doc in Config.KNOWLEDGE_POINTS:
                knowledge_points.append(Config.KNOWLEDGE_POINTS[doc])
        return knowledge_points
    
    def check_repetition(self, knowledge_point: str) -> bool:
        """
        檢查是否連續重複詢問同一知識點
        
        Args:
            knowledge_point: 知識點名稱
            
        Returns:
            是否處於重複狀態
        """
        if len(self.consecutive_access) < Config.REPETITION_THRESHOLD:
            return False
        
        # 檢查最近的 N 次訪問
        recent = list(self.consecutive_access)[-Config.REPETITION_THRESHOLD:]
        
        # 如果最近 N 次都是同一個知識點，則判定為重複
        return all(kp == knowledge_point for kp in recent)
    
    def get_recent_history(self, n: int = None) -> List[QueryHistory]:
        """
        獲取最近的 N 條歷史記錄
        
        Args:
            n: 記錄數量（默認全部）
            
        Returns:
            歷史記錄列表
        """
        if n is None:
            return list(self.history)
        return list(self.history)[-n:]
    
    def get_knowledge_point_stats(self) -> Dict[str, int]:
        """
        獲取知識點訪問統計
        
        Returns:
            知識點訪問次數字典
        """
        return dict(self.knowledge_point_counter)
    
    def get_dimension_stats(self) -> Dict[str, Counter]:
        """
        獲取四向度統計
        
        Returns:
            各向度的值分布統計
        """
        stats = {
            "D1": Counter(),
            "D2": Counter(),
            "D3": Counter(),
            "D4": Counter()
        }
        
        for record in self.history:
            for dim, value in record.dimensions.items():
                stats[dim][value] += 1
        
        return stats
    
    def clear(self):
        """清空歷史記錄"""
        self.history.clear()
        self.knowledge_point_counter.clear()
        self.consecutive_access.clear()
        self.save()
    
    def save(self):
        """儲存歷史記錄到文件"""
        data = {
            "history": [record.to_dict() for record in self.history],
            "knowledge_point_counter": dict(self.knowledge_point_counter),
            "consecutive_access": list(self.consecutive_access)
        }
        
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self) -> bool:
        """
        從文件載入歷史記錄
        
        Returns:
            是否成功載入
        """
        if not os.path.exists(self.storage_path):
            return False
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 載入歷史記錄
            self.history = deque(
                [QueryHistory.from_dict(record) for record in data.get("history", [])],
                maxlen=self.max_size
            )
            
            # 載入知識點計數
            self.knowledge_point_counter = Counter(data.get("knowledge_point_counter", {}))
            
            # 載入連續訪問記錄
            self.consecutive_access = deque(
                data.get("consecutive_access", []),
                maxlen=10
            )
            
            return True
        except Exception as e:
            print(f"⚠️  載入歷史記錄失敗: {e}")
            return False
    
    def get_summary(self) -> dict:
        """
        獲取歷史記錄摘要
        
        Returns:
            摘要字典
        """
        return {
            "total_queries": len(self.history),
            "max_size": self.max_size,
            "knowledge_points": self.get_knowledge_point_stats(),
            "dimension_stats": {
                dim: dict(counter) 
                for dim, counter in self.get_dimension_stats().items()
            },
            "recent_access": list(self.consecutive_access)[-5:]  # 最近5次
        }
    
    def print_summary(self):
        """打印歷史記錄摘要"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("📊 歷史紀錄摘要")
        print("="*60)
        print(f"總查詢次數: {summary['total_queries']}/{summary['max_size']}")
        
        print("\n知識點訪問統計:")
        for kp, count in summary['knowledge_points'].items():
            print(f"  {kp}: {count} 次")
        
        print("\n四向度分布:")
        for dim, stats in summary['dimension_stats'].items():
            dim_name = Config.DIMENSIONS[dim]['name']
            print(f"  {dim} ({dim_name}):")
            for value, count in stats.items():
                print(f"    {value}: {count} 次")
        
        print("\n最近訪問的知識點:")
        print(f"  {' → '.join(summary['recent_access'])}")
        
        print("="*60 + "\n")
