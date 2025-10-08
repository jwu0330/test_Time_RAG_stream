"""
核心模組包
包含所有核心功能模組
"""

__version__ = "1.0.0"

# 導入核心類別以便於使用
from .vector_store import VectorStore, cosine_similarity
from .rag_module import RAGRetriever, RAGCache
from .scenario_module import DimensionClassifier, ScenarioClassifier, ScenarioInjector
from .scenario_matcher import ScenarioMatcher
from .history_manager import HistoryManager, QueryHistory
from .timer_utils import Timer, TimerRecord, TimerReport

__all__ = [
    'VectorStore',
    'cosine_similarity',
    'RAGRetriever',
    'RAGCache',
    'DimensionClassifier',
    'ScenarioClassifier',
    'ScenarioInjector',
    'ScenarioMatcher',
    'HistoryManager',
    'QueryHistory',
    'Timer',
    'TimerRecord',
    'TimerReport',
]
