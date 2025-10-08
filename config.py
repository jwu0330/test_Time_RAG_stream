"""
系統配置文件
用於設定模型和系統參數
"""

class Config:
    """系統配置類"""
    
    # ==================== 模型配置 ====================
    
    # Embedding 模型
    # 選項: "text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"
    EMBEDDING_MODEL = "text-embedding-3-small"
    
    # 主要 LLM 模型（用於生成草稿和最終答案）
    # 選項: "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"
    LLM_MODEL = "gpt-4o-mini"
    
    # 情境分類模型（用於四向度判定）
    # 選項: "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o-mini"
    # 使用 gpt-4o-mini 獲得更快的響應速度
    CLASSIFIER_MODEL = "gpt-4o-mini"
    
    # ==================== 系統參數 ====================
    
    # 歷史紀錄保存數量
    HISTORY_SIZE = 10
    
    # 重複詢問閾值（連續詢問同一知識點超過此次數視為重複）
    REPETITION_THRESHOLD = 3
    
    # RAG 檢索參數
    RAG_TOP_K = 3  # 返回前 K 個最相關文件
    RAG_SIMILARITY_THRESHOLD = 0.7  # 相似度閾值
    
    # LLM 生成參數
    LLM_TEMPERATURE = 0.7  # 溫度參數（0-1，越高越隨機）
    LLM_MAX_TOKENS = 500  # 草稿最大 token 數
    LLM_FINAL_MAX_TOKENS = 1000  # 最終答案最大 token 數
    
    # ==================== 儲存路徑 ====================
    
    # 向量儲存路徑
    VECTOR_STORAGE_PATH = "vectors.pkl"
    
    # 歷史紀錄儲存路徑
    HISTORY_STORAGE_PATH = "history.json"
    
    # 結果輸出目錄
    RESULTS_DIR = "results"
    
    # 文件目錄
    DOCS_DIR = "data/docs"
    
    # 情境目錄
    SCENARIOS_DIR = "data/scenarios"
    
    # ==================== 四向度定義 ====================
    
    DIMENSIONS = {
        "D1": {
            "name": "知識點數量",
            "description": "這句話牽涉到的知識點數量",
            "values": ["零個", "一個", "多個"]
        },
        "D2": {
            "name": "表達錯誤",
            "description": "這句話的表達是否有錯誤",
            "values": ["有錯誤", "無錯誤"]
        },
        "D3": {
            "name": "表達詳細度",
            "description": "這句話的表達是否詳細",
            "values": ["粗略", "非常詳細"]
        },
        "D4": {
            "name": "重複詢問",
            "description": "是否在同一知識點上重複詢問多次",
            "values": ["重複狀態", "正常狀態"],
            "threshold": REPETITION_THRESHOLD
        }
    }
    
    # ==================== 知識點映射 ====================
    
    # 文件到知識點的映射（根據您上傳的 3 份文件）
    KNOWLEDGE_POINTS = {
        "ml_basics.txt": "機器學習基礎",
        "deep_learning.txt": "深度學習",
        "nlp_intro.txt": "自然語言處理"
    }
    
    # ==================== Web 界面配置 ====================
    
    # API 服務器配置
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # CORS 設定
    CORS_ORIGINS = ["*"]  # 生產環境應該設定具體域名
    
    # 是否啟用流式輸出
    ENABLE_STREAMING = True


# 創建全局配置實例
config = Config()


def update_config(**kwargs):
    """
    動態更新配置
    
    Args:
        **kwargs: 要更新的配置項
    
    Example:
        update_config(LLM_MODEL="gpt-4", RAG_TOP_K=5)
    """
    for key, value in kwargs.items():
        if hasattr(Config, key):
            setattr(Config, key, value)
        else:
            raise ValueError(f"未知的配置項: {key}")


def get_config_summary() -> dict:
    """
    獲取配置摘要
    
    Returns:
        配置摘要字典
    """
    return {
        "models": {
            "embedding": Config.EMBEDDING_MODEL,
            "llm": Config.LLM_MODEL,
            "classifier": Config.CLASSIFIER_MODEL
        },
        "parameters": {
            "history_size": Config.HISTORY_SIZE,
            "repetition_threshold": Config.REPETITION_THRESHOLD,
            "rag_top_k": Config.RAG_TOP_K,
            "temperature": Config.LLM_TEMPERATURE
        },
        "paths": {
            "vectors": Config.VECTOR_STORAGE_PATH,
            "history": Config.HISTORY_STORAGE_PATH,
            "results": Config.RESULTS_DIR
        }
    }
