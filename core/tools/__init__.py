"""
維度檢測工具模組
包含 C (正確性)、K (知識點)、R (重複) 三個維度的檢測工具
"""

from .correctness_detector import CorrectnessDetector
from .knowledge_detector import KnowledgeDetector
from .repetition_checker import RepetitionChecker

__all__ = [
    'CorrectnessDetector',
    'KnowledgeDetector',
    'RepetitionChecker'
]
